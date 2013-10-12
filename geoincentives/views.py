import datetime

from coffin.shortcuts import render_to_response as jinja2_render_to_response
from geoincentives.forms import SignupForm, PaypalSignupForm
import pycurl
import urllib
import StringIO
import json
import hashlib

from django.http import HttpResponseRedirect, HttpResponse
#from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import authenticate, login

from geoincentives.models import User, Event, UserEvent

def home(request):

    context = {}
    context.update(csrf(request))
    context['request'] = request
    context['is_authenticated'] = request.user.is_authenticated()

    return jinja2_render_to_response(
        'home.html', context
    )

@login_required(login_url='/login/')
def history(request):

    history = UserEvent.objects.all().filter(user=request.user).order_by('date')
    #from IPython import embed; embed()

    return jinja2_render_to_response(
        'eventhistory.html', {
            'history': history,
            'request': request,
            'is_authenticated': request.user.is_authenticated()
        }
    )

@login_required(login_url='/login/')
def useraccount(request):

    return jinja2_render_to_response(
        'useraccount.html', {
            'request': request,
            'is_authenticated': request.user.is_authenticated()
        }
    )

@login_required(login_url='/login/')
def redemption(request):
    events = [] #request.user.get_nearby_events()

    return jinja2_render_to_response(
        'redemption.html', {
            'events': events,
            'request': request,
            'is_authenticated': request.user.is_authenticated()
        }
    )

#-121.9227413 37.3768341

@login_required(login_url='/login/')
def ajax_checkin(request):

    event_id = request.GET.get('event')
    event = Event.objects.get(id=event_id)

    row = UserEvent(user=request.user, event=event, date=datetime.datetime.now())
    row.save()

    return HttpResponse('ok')



@login_required(login_url='/login/')
def checkin(request):

    cur_lng = float(-121.9227413)
    cur_lat = float(37.3768341)

    events = Event.objects.raw('select * from geoincentives_event where ((latitude - %(cur_lat)s) * (latitude - %(cur_lat)s)) + ((longitude - %(cur_lng)s * (longitude - %(cur_lng)s)) < 200)' % { 'cur_lat': cur_lat, 'cur_lng': cur_lng})
    #((cur_lat - 37.3768341) * (cur_lat - 37.3768341)) + ((cur_lng - -121.9227413 * (cur_lng - -121.9227413)) < 200)
    #from IPython import embed; embed()

    return jinja2_render_to_response(
        'checkin.html', {
            'events': events,
            'request': request,
            'is_authenticated': request.user.is_authenticated()
        }
    )

def logout(request):
    request.session.clear()
    request.session.flush()
    return HttpResponseRedirect('/')


@csrf_protect
def signup(request, type=None):
    if not type:
        type = 1

    request.session['type'] = int(type)
    context = { 'request': request, 'type': int(type), 'is_authenticated': request.user.is_authenticated() }
    context.update(csrf(request))

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            django_user = DjangoUser.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password'])

            django_user.first_name = form.cleaned_data['first_name']
            django_user.last_name = form.cleaned_data['last_name']
            django_user.save()

            user = User(
                auth_user=django_user,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zipcode=form.cleaned_data['zipcode'],
                school=form.cleaned_data['school'],
                type=type
            )

            if (form.cleaned_data['birthdate']):
                user.birthdate = form.cleaned_data['birthdate']

            user.save()

            return HttpResponseRedirect('/checkin/')

        print form.errors

    context['signup_form'] = SignupForm()

    return jinja2_render_to_response(
        'signup.html', context
    )

@csrf_protect
def complete_signup(request):
    context = { 'request': request, 'is_authenticated': request.user.is_authenticated() }
    context.update(csrf(request))

    if request.method == 'POST':
        form = PaypalSignupForm(request.POST)

        if form.is_valid():
            django_user = authenticate(username=request.session['paypal_user'], password=request.session['paypal_pass'])
            login(request, django_user)
            #django_user = DjangoUser.objects.get(email=request.session['paypal_user'])
            user = User.objects.get(auth_user=django_user)

            if (request.session['type'] == 1):
                user.school = form.cleaned_data['school']
            else:
                user.company = form.cleaned_data['company']

            user.save()


            return HttpResponse(
                '<html><head><script>' +
                'window.onunload = refreshParent;' +
                'function refreshParent() {' +
                'window.opener.location = "/login/";' +
                '} window.opener.location = "/checkin/"; window.close();</script></head></html>')

        print form.errors

    context['signup_form'] = SignupForm()

    return jinja2_render_to_response(
        'signup.html', context
    )

def paypal(request):
    print 'code: %s' % request.GET['code']
    context = { 'request': request, 'is_authenticated': request.user.is_authenticated() }
    curl = pycurl.Curl()
    curl.setopt(pycurl.POST, True)
    postdata = urllib.urlencode({
        'client_id': 'AfaKGBALBiCoGmBD1EXDHASb30sc7iKSwRfgtTq5PXXKP2NzT5AF8WxI4Hl7',
        'client_secret': 'EHyhKxCofRT6AgcxZhcLtE6PafygLbbDngClEoSwlwVG1kkZ5qZExpHnj6fp',
        'grant_type': 'authorization_code',
        'code': request.GET['code']})
    curl.setopt(pycurl.POSTFIELDS, postdata)
    curl.setopt(pycurl.VERBOSE, True)
    curl.setopt(pycurl.URL, str('https://api.sandbox.paypal.com/v1/identity/openidconnect/tokenservice'))
    curl.setopt(pycurl.SSL_VERIFYPEER, False)

    response_header = StringIO.StringIO()
    curl.setopt(pycurl.HEADERFUNCTION, response_header.write)
    response_body = StringIO.StringIO()
    curl.setopt(pycurl.WRITEFUNCTION, response_body.write)

    curl.perform()
    response_code = curl.getinfo(pycurl.HTTP_CODE)
    print response_code

    response_body = response_body.getvalue()
    print response_body
    response_data = json.loads(response_body)


    #$ch = curl_init( "https://api.sandbox.paypal.com/v1/identity/openidconnect/userinfo/?schema=openid&access_token=" . $access_token );
    curl = pycurl.Curl()

    curl.setopt(pycurl.VERBOSE, True)
    curl.setopt(pycurl.URL, str("https://api.sandbox.paypal.com/v1/identity/openidconnect/userinfo/?schema=openid&access_token=%s" % response_data['access_token']))
    curl.setopt(pycurl.SSL_VERIFYPEER, False)

    response_header = StringIO.StringIO()
    curl.setopt(pycurl.HEADERFUNCTION, response_header.write)
    response_body = StringIO.StringIO()
    curl.setopt(pycurl.WRITEFUNCTION, response_body.write)

    curl.perform()
    response_code = curl.getinfo(pycurl.HTTP_CODE)
    print response_code

    response_body = response_body.getvalue()
    print response_body

    #{"family_name":"Weigel","name":"John Weigel","account_type":"PERSONAL","given_name":"John","address":{"postal_code":"95131","locality":"San Jose","region":"CA","country":"US","street_address":"1 Main St"},"verified_account":"true","language":"en_US","zoneinfo":"America/Los_Angeles","locale":"en_US","phone_number":"4089192640","email":"test@geoi.com","account_creation_date":"2013-10-12","age_range":"31-35","birthday":"1982-08-02"}
    response_data = json.loads(response_body)

    try:
        DjangoUser.objects.get(username=response_data['email'])
    except DjangoUser.DoesNotExist:
        print 'Creating account'

        passwd = hashlib.sha224(response_data['email']).hexdigest()

        django_user = DjangoUser.objects.create_user(
            response_data['email'],
            response_data['email'],
            passwd)

        user = User(
            auth_user=django_user,
            address=response_data['address']['street_address'],
            city=response_data['address']['locality'],
            state=response_data['address']['region'],
            zipcode=response_data['address']['postal_code'],
            type=request.session.get('type', 1)
        )
        user.save()
        request.session['paypal_user'] = django_user.email
        request.session['paypal_pass'] = passwd


        context.update(csrf(request))
        context['paypal_signup_form'] = PaypalSignupForm()
        return jinja2_render_to_response(
            'paypal_signup.html', context
        )


    #print request.POST
    return HttpResponse('test')


