from django.contrib import admin

from .models import Category, Food

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
    search_fields = ['name', ]
    list_filter = ['name']

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display= ['title', 'category', 'price_main', 'price_discount', 'inventory', 'created_at',]
    list_filter =['title', 'category', ]
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}