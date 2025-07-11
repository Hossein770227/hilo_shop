from django.urls import path

from . import views

app_name ='shop'

urlpatterns = [
    path("", views.FoodList.as_view(), name='food_list')
]


