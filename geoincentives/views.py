from coffin.shortcuts import render_to_response as jinja2_render_to_response
from geoincentives.forms import UserLoginForm

def home(request):

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            encrypted_password = Student().hash_password(form.cleaned_data['password'])


    return jinja2_render_to_response(
        'home.html', {
            'login_form': UserLoginForm()
        }
    )
