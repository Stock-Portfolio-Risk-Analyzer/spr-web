from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import django.forms as forms

class Stock(models.Model):
    """

    """
    stock_id = models.AutoField(primary_key=True)
    stock_quantity = models.IntegerField(default=0)
    stock_ticker = models.CharField(max_length=8, default="")
    stock_name = models.CharField(max_length=200)
    stock_beta = models.FloatField(default=0.0)
    stock_sector = models.CharField(max_length=200, default="Other")

    def __str__(self):
        return '{} {} {}'.format(self.stock_id, self.stock_ticker, self.stock_beta)


class Risk(models.Model):
    """

    """
    risk_id = models.AutoField(primary_key=True)
    risk_value = models.FloatField(default=0.0)
    risk_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} @ {}'.format(self.risk_value, self.risk_date)


class Portfolio(models.Model):
    """

    """
    portfolio_id = models.AutoField(primary_key=True)
    portfolio_stocks = models.ManyToManyField(Stock)
    portfolio_user = models.ForeignKey(User)
    portfolio_risk = models.ManyToManyField(Risk)

    def __str__(self):
        return '{} {}'.format(self.portfolio_id, self.portfolio_risk)
class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
