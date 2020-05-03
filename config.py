# Stripe config options
#
import os

STRIPE_API_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY') or "sk_test_edhurKZR5OMK0Wvl7uYLyu1n"
WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET') or "whsec_K8reb65yXmHSEyKkSMx8h84rozwb5R69"
