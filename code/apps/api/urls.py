from django.urls import path

from .views import *

app_name = 'api'

urlpatterns = [
    path('items', GetAllItems.as_view(), name='items'),

    path('buy/<int:item_id>', BuyItem.as_view(), name='buy_item'),
    path('item/<int:item_id>', GetItem.as_view(), name='item'),

    path('order/<str:order_id>', OrderAPI.as_view(), name='order'),
    path('order', OrderCreateAPI.as_view(), name='create_order'),

    path('success', SuccessUrl.as_view(), name='success'),
    path('cancel', CancelUrl.as_view(), name='cancel')
]