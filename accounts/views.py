from django.shortcuts import render
from .forms import SignUpForm

from django.http import HttpResponse

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # return redirect('home')
            return HttpResponse('<h3>Account created successfully</h3>')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})