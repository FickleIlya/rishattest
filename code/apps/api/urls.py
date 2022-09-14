from django.urls import path

from .views import GetItem, BuyItem, SuccessUlr, CancelUrl

urlpatterns = [
    path('buy/<int:item_id>', BuyItem.as_view(), name='buy'),
    path('item/<int:item_id>', GetItem.as_view(), name='item'),

    path('success', SuccessUlr.as_view(), name='success'),
    path('cancel', CancelUrl.as_view(), name='cancel')
]