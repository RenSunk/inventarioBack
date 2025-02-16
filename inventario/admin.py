from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(ProductVariant)
admin.site.register(ConversionCategory)
admin.site.register(Unit)

admin.site.register(StockUnit)
admin.site.register(ProductUnit)

