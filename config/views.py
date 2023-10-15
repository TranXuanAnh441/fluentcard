from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(requests):
    return redirect('deck_list')