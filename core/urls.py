from django.urls import path

from memberships.views import MembershipView, StripePaymentView, submit_payment_method, update_transaction_records, submit_card_info
from .views import home

app_name = "core"

urlpatterns = [
    path('', home, name="home"),
    path('subscriptions', MembershipView.as_view(), name="subscriptions"),
    path('payment', StripePaymentView.as_view(), name="stripe-payment"),
    path('submit-payment-method', submit_payment_method, name="submit-payment-method"),
    path('submit-card', submit_card_info, name="submit-card"),
    path('update-transactions/<subscription_id>/', update_transaction_records, name='update-transactions'),
]
