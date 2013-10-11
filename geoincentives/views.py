from coffin.shortcuts import render_to_response as jinja2_render_to_response

def home(request):

    return jinja2_render_to_response(
        'home.html', {
        }
    )
