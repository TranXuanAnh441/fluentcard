from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(requests):
    return redirect('deck_list')


def help_page(requests):
    return render(requests, 'config/help_page.html', {})


def handler404(request, exception):
    return render(request, 'errors/404.html', {})


def handler500(request):
    return render(request, 'errors/500.html', {})