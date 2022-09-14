from django.urls import path

from .views import *

urlpatterns = [
    path('items', GetAllItems.as_view(), name='items'),
    path('buy/<int:item_id>', BuyItem.as_view(), name='buy'),
    path('item/<int:item_id>', GetItem.as_view(), name='item'),
    path('order/<int:order_id>', BuyOrder.as_view(), name='order'),

    path('success', SuccessUrl.as_view(), name='success'),
    path('cancel', CancelUrl.as_view(), name='cancel')
]