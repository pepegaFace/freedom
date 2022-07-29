from django.contrib import admin
from .models import *


@admin.register(Category)
class AdmCategory(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(SubCategory)
class AdmCategory(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')


@admin.register(Product)
class AdmProduct(admin.ModelAdmin):
    list_display = ('id', 'name', 'article')
    filter_horizontal = ('sub_category', )
