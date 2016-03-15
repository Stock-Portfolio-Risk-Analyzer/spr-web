from django import forms
from .models import Portfolio, Stock
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