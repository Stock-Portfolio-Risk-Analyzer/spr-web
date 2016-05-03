from django.contrib import admin

import stockportfolio.api.models as models

"""Register Django models in this module"""

# Register your models here.
admin.site.register(models.Stock)
admin.site.register(models.Portfolio)
admin.site.register(models.Risk)
admin.site.register(models.UserSettings)
admin.site.register(models.PortfolioRank)
admin.site.register(models.StockPortfolio)
admin.site.register(models.Price)
