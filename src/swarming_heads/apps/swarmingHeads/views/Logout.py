from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def logout_handler(request):
    if request.method == "POST":    
        logout(request)
        return HttpResponseRedirect('/')