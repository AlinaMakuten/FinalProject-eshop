from django.urls import path
from . import views



urlpatterns = [
    path('', views.products, name='knygos'),
    path('kategorija/<category_slug>/', views.products, name='products_by_category'),
    path('kategorija/<category_slug>/<product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
 ]


