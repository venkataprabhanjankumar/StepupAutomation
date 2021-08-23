from django.shortcuts import render


def index(request):
    return render(
        request,
        'index.html',
        {}
    )


def handle_redirect(request, template):
    return render(
        request,
        template+'.html',
        {}
    )


def signin(request):
    if request.method == 'POST':
        pass
    else:
        return render(
            request,
            'signin-illustration.html',
            {}
        )
