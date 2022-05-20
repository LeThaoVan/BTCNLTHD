from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='categories', viewset=views.CategoryViewset, basename='category')
router.register(prefix='route', viewset=views.RouteViewSet, basename='route')
router.register(prefix='buses', viewset=views.BusesViewSet, basename='buses')
router.register(prefix='comments', viewset=views.CommentViewSet, basename='comment')
router.register(prefix='users', viewset=views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('my-route/', views.MyRouteView.as_view()),
    path('my-route/<int:pk>/', views.MyRouteDetailView.as_view()),
    path('charts/filter-options/', views.get_filter_options, name='chart-filter-options'),
    path('charts/count-buses/<int:year>/', views.count_buses_chart, name='count-buses'),
    path('charts/sales/<int:year>/', views.get_sales_chart, name='chart-sales'),
    path('charts/spend-per-customer/<int:year>/', views.spend_per_customer_chart, name='chart-spend-per-customer'),
    path('charts/sales2/<int:year>/', views.get_sales_chart2, name='chart-sales2'),
]