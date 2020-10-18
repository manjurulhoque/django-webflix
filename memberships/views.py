from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, TemplateView, FormView
from django.urls import reverse

from .models import Membership, UserMembership, Subscription

import stripe


def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


def get_selected_membership(request):
    memberships = {
        1: 'Free',
        2: 'Monthly',
        3: 'Daily',
    }
    try:
        membership_type = memberships[int(request.session['package'])]
        selected_membership_qs = Membership.objects.filter(membership_type=membership_type)
        if selected_membership_qs.exists():
            return selected_membership_qs.first()
        return None
    except:
        return None


class MembershipView(LoginRequiredMixin, ListView):
    model = Membership
    template_name = "memberships.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context


@login_required(login_url="/accounts/login")
@require_http_methods(["POST"])
def submit_payment_method(request):
    request.session['method'] = request.POST['method']
    request.session['package'] = request.POST['package']

    if request.POST['method'] == "card":
        return redirect(reverse("core:stripe-payment"))
    else:
        messages.info(request, "We are currently accept card only")
        return redirect(reverse("core:subscriptions"))


class StripePaymentView(LoginRequiredMixin, TemplateView):
    template_name = "strip-payment.html"

    def get_context_data(self, **kwargs):
        context = super(StripePaymentView, self).get_context_data(**kwargs)
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

    def get(self, request, *args, **kwargs):
        if not request.session['package'] or not request.session['method']:
            return redirect(reverse('core:subscriptions'), permanent=True)
        return super(StripePaymentView, self).get(request, *args, **kwargs)


@login_required(login_url="/accounts/login")
@require_http_methods(["POST"])
def submit_card_info(request):
    user_membership = get_user_membership(request)
    try:
        selected_membership = get_selected_membership(request)
    except Exception:
        return redirect(reverse("core:subscriptions"))
    try:
        token = request.POST['stripeToken']
        '''
        First we need to add the source for the customer
        '''
        customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
        customer.source = token  # 4242424242424242
        customer.save()

        '''
        Now we can create the subscription using only the customer as we don't need to pass their
        credit card source anymore
        '''

        subscription = stripe.Subscription.create(
            customer=user_membership.stripe_customer_id,
            items=[
                {"plan": selected_membership.stripe_plan_id},
            ]
        )

        return redirect(reverse('core:update-transactions',
                                kwargs={
                                    'subscription_id': subscription.id
                                }))
    except Exception as e:
        print(e)
        messages.info(request, "An error has occurred, investigate it in the console")

    return redirect(reverse('core:subscriptions'))


@login_required(login_url="/accounts/login")
def update_transaction_records(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(
        user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['package']
        del request.session['method']
    except:
        pass

    messages.info(request, 'Successfully created {} membership'.format(selected_membership))
    return redirect(reverse('core:subscriptions'))
