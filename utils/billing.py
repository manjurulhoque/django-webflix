import stripe
from djstripe.settings import djstripe_settings


def get_stripe_module():
    """
    Gets the Stripe API module, with the API key properly populated
    """
    stripe.api_key =  djstripe_settings.STRIPE_SECRET_KEY
    return stripe
