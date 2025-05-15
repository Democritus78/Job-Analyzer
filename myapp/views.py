from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        print(f"Received Name: {name}")
        return HttpResponseRedirect('/')
    
    return render(request, 'myapp/index.html')