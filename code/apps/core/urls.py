from django.urls import path

from .views import *

app_name = 'core'

urlpatterns = [
    path('items/', ViewItems.as_view(), name='items'),
    path('order', GetOrderId.as_view(), name='get_order_id'),
    path('order/<str:order_id>/', ViewOrder.as_view(), name='order_info'),
    path('item/<int:item_id>/', ViewItemDetail.as_view(), name='item'),
]
