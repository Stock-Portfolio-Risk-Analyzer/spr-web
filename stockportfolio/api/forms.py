import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from stockportfolio.api.models import Portfolio, UserSettings

"""Contains the forms for the stockportfolio module"""

class UpdateProfile(forms.ModelForm):
    """
    Form used to update profile. Extends ModelForm

    """
    default_portfolio = forms.ModelChoiceField(
        queryset=Portfolio.objects.all())

    class Meta:
        """
        Specifies which User Fields To Prompt in Form

        """
        model = User
        fields = ('username', 'email', 'default_portfolio')

    def __init__(self, *args, **kwargs):
        """
        Initializes a Form Object, and adds a submit button
        and form action to it.

        :param args: Arguments for overwrittn init function
        :param kwargs: Keyword Arguments for overwrittn init function
        :return: (Form) UpdateProfile Form
        """
        super(UpdateProfile, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_action = reverse('modify_account')

    def clean_username(self):
        """
        Cleans the username input field

        :return: (str) username
        """
        return self.cleaned_data.get('username')

    def clean_email(self):
        """
        Cleans the email input field

        :return: (str) email
        """
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).count() > 1:
            raise forms.ValidationError(
                'This email address is already in use. \
                 Please supply a different email address.')
        return email

    def save(self, commit=True):
        """
        Overwritten Save Function, which generates a new user on
        creation.

        :param commit: True if user needs to be saved,
        False otherwise (just modified).
        :return: (User) Modified User
        """
        user = User.objects.get(username=self.cleaned_data["username"])
        user.email = self.cleaned_data['email']
        user_settings = UserSettings.objects.get(user=user)
        dp = self.cleaned_data['default_portfolio']
        user_settings.default_portfolio = dp
        user_settings.save()

        if commit:
            user.save()
        return user


class PortfolioUploadForm(forms.Form):
    """
    Form used to Upload CSV File into backend file - FileField.
    Extends everything from forms.Form.

    """
    file = forms.FileField()
