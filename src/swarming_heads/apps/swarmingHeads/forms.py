from django import forms
from django.contrib.auth import login
from django.utils.translation import ugettext

# Self contained login module
# Credit: http://djangosnippets.org/snippets/332/

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=32)        
    user = None   # allow access to user object     
    def clean(self):
        # only do further checks if the rest was valid
        if self._errors: return
        
        from django.contrib.auth import login, authenticate
        user = authenticate(username=self.data['username'],
                            password=self.data['password'])
        if user is not None:
            if user.is_active:
                self.user = user                    
            else:
                raise forms.ValidationError(ugettext(
                    'This account is currently inactive. Please contact '
                    'the administrator if you believe this to be in error.'))
        else:
            raise forms.ValidationError(ugettext(
                'The username and password you specified are not valid.'))
    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            return True
        return False