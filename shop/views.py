from django.shortcuts import render
from django.views.generic import TemplateView

class FoodList(TemplateView):
    template_name = 'shop/food_list.html'
