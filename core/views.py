from django.shortcuts import render, redirect

# Create your views here.
def home_view(request):
    # return render(request, 'home.html')
    return redirect('messageboard')