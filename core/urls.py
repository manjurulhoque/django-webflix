from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('pricing/', views.pricing, name='pricing'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/canceled/', views.checkout_canceled, name='checkout_canceled'),
    path('subscription/cancel/', views.cancel_subscription, name='cancel_subscription'),
]
