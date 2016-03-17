import django.forms as forms
from .models import Portfolio, Stock
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from registration.forms import RegistrationForm

# Used the following as reference
# http://stackoverflow.com/questions/6142025/dynamically-add-field-to-a-form
#

# class StockField(forms.CharField):
#     def __init__(self, user, *args, **kwargs):
#         super(StockField, self).__init__(*args, **kwargs)
#     def clean(self, value):
#         super(StockField, self).clean(value)
#         Stock.object.get()
#
# class PortfolioForm(forms.ModelForm):
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(PortfolioForm, self).__init__(*args, **kwargs)
#         for k, v in args[0].items():
#             if
class UpdateProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','email')

    def __init__ (self, *args, **kwargs):
    	super(UpdateProfile, self).__init__ (*args, **kwargs)
    	self.helper = FormHelper()
    	self.helper.form_method = "post"
        self.helper.form_action = ''

        self.helper.add_input(Submit('submit', 'Submit'))
    def clean_username(self):
    	print "cleaned username"
    	return self.cleaned_data.get('username')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        print "cleaned email"
        return email
    def save(self, commit=True):
        user = User.objects.get(username = self.cleaned_data["username"])
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user