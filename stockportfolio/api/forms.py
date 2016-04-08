import django.forms as forms
from .models import Portfolio, Stock, UserSettings
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from registration.forms import RegistrationForm
from django.core.urlresolvers import reverse

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
    default_portfolio = forms.ModelChoiceField(
        queryset=Portfolio.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'default_portfolio')

    def __init__(self, *args, **kwargs):
        super(UpdateProfile, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_action = reverse('modify_account')

    def clean_username(self):
        return self.cleaned_data.get('username')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).count() > 1:
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = User.objects.get(username=self.cleaned_data["username"])
        user.email = self.cleaned_data['email']
        user_settings = UserSettings.objects.get(user=user)
        user_settings.default_portfolio = self.cleaned_data['default_portfolio']
        user_settings.save()

        if commit:
            user.save()
        return user
