<h1 align="center"> Stripe PaymentIntents API Integration</h1>

Welcome to the Trailblazer Sneaker shop!
[![NPM version](https://badge.fury.io/js/tiny-npm-license.svg)](https://www.npmjs.org/package/tiny-npm-license)

<div align="center">
<img src="images/Shoe_feather.png" alt="hero image" width="400"/>
</div>


As an owner of an ecommerce store, you will want to integrate with the payments API for Stripe. This is a simple way to build a checkout form that collects name, email, card details. Included are some basic build and run scripts you can use to start up the application.

## Overview

This guide is an integration with the PaymentIntents API for  Stripe.
1. The frontend form takes in basic payment details such as name, email and card details. 
1. The backend receives this request and creates a new PaymentIntents request and customer object in Stripe. 
1. Then it makes the payment request to Stripe and sends the client secret back to the frontend.
1. The client confirms the payment using the client secret.
1. Webhooks wait on hearing about the successful completion of the charge and perform post payment actions.


## Features
|     | Features
:---: | :---
✨ | **Simple UI for card payments**. This demo uses pre-built Stripe components, including the [Card Element](https://stripe.com/docs/elements) which provides real-time validation.
🔐 | **Dynamic 3D Secure for Visa and Mastercard.** The app automatically handles the correct flow to complete card payments with [3D Secure](https://stripe.com/docs/payments/dynamic-3ds), whether it’s required by the card or encoded in one of your [3D Secure Radar rules](https://dashboard.stripe.com/radar/rules).
🚀 | **Built-in proxy for local HTTPS and webhooks.** The [Stripe CLI](https://github.com/stripe/stripe-cli#listen) is used to forward webhook events to the local server.
📦 | **No datastore required.** Customers are stored using the [Stripe API](https://stripe.com/docs/api/products) and inventory is in memory, so you don't need a database to keep track of products.
🔧 | **Payment Logs.** You can access the payment logs stored in the file demo.log.

## Setup

<img src="images/Stripe_PaymentIntent_1.2020-05-04 11_21_40.gif" width="800" />

### Requirements
You’ll need the following:

1. Python >= 3.6
1. Modern browser that supports ES6.
1. Stripe account to accept payments (sign up for free).

In order to complete the request and update inventory, we need to receive a real-time webhook notification. We're using the Stripe CLI to forward webhook events to our local development server.

### Config
Set your environment variables STRIPE_SECRET_KEY and
STRIPE_WEBHOOK_SECRET using the following commands:

```
export STRIPE_SECRET_KEY=<your_key>
export STRIPE_WEBHOOK_SECRET=<your_secret>
```

### Build & Run backend server

1. Install all requirements for the backend server.

```
pip3 install -r requirements.txt
```

2. Run the server: Specify the FLASK_APP environment variable for the target server and the FLASK_ENV environment variable so that you can see debug logs for a local run of the app.

```
export FLASK_APP=server.py
export FLASK_ENV=development
python3 -m flask run --port=4242
```
Navigate to http://localhost:4242/ to verify your server is up and running. 
To view your total amount go to http://localhost:4242/get-total and to view your cart go to http://localhost:4242/get-cart

### Forward events to webhook using Stripe CLI

1. Follow the instructions [here](https://stripe.com/docs/payments/handling-payment-events#install-cli) to install Stripe CLI and login into your account.

1. Forward events locally to your webhook using:
```
stripe listen --forward-to http://localhost:4242/webhook
```

In a different terminal tab, use the following:
```
stripe trigger payment_intent.succeeded
```

You should be able to see the following:
```
[200 POST] OK payment_intent.succeeded
```

### Build & Run the client app

1. Build the frontend client app: Run the following to install all dependencies needed.

```
npm install
```

2. Run the client app.

```
npm start
```


### Testing

#### Successful Payment Test

1. Verify your cart is full of the items Nike Zoom Fly 2 units by going to http://localhost:4242/get-cart. Your total of 300 should be visible at http://localhost:4242/get-total.

1. Go to [http://localhost:3000/checkout](http://localhost:3000/checkout). Enter your name and email address in the form provided. Enter card details "4242 4242 4242 4242" for testing a successful payment. Enter any valid values for the rest of the options such as CVV, expiration date and zip code. Press "Pay". You should see the payment go through successfully.

1. Verify your total is now 0 and you cart is now empty by going to http://localhost:4242/get-total and  http://localhost:4242/get-cart respectively.

1. Your webhook listener should report events such as:

```
2020-05-04 11:13:57  <--  [200] POST http://localhost:4242/webhook [evt_1Gex9GG8lTpkPNJEk7vB6cJR]
2020-05-04 11:14:05   --> payment_intent.succeeded [evt_1Gex9OG8lTpkPNJEOMkO3Sqp]
2020-05-04 11:14:05   --> charge.succeeded [evt_1Gex9OG8lTpkPNJEjnEMPWZK]
2020-05-04 11:14:05  <--  [200] POST http://localhost:4242/webhook [evt_1Gex9OG8lTpkPNJEjnEMPWZK]
```

#### Successful Payment with Authentication Test

1. Shut down the previous instances of frontend and backend if running and restart them. This should make your cart full again.

1. Verify your cart is full of the items Nike Zoom Fly 2 units by going to http://localhost:4242/get-cart. Your total of 300 should be visible at http://localhost:4242/get-total.

1. Go to [http://localhost:3000/checkout](http://localhost:3000/checkout). Enter your name and email address in the form provided. Enter card details "4000 0025 0000 3155" for testing a successful payment. Enter any valid values for the rest of the options such as CVV, expiration date and zip code. Press "Pay". You will be asked to confirm payment for 3DS. Press confirm payment. You should see the payment go through successfully.

1. Verify your total is now 0 and you cart is now empty by going to http://localhost:4242/get-total and  http://localhost:4242/get-cart respectively.

1. Your webhook listener should report events such as:

```
2020-05-04 11:13:57  <--  [200] POST http://localhost:4242/webhook [evt_1Gex9GG8lTpkPNJEk7vB6cJR]
2020-05-04 11:14:05   --> payment_intent.succeeded [evt_1Gex9OG8lTpkPNJEOMkO3Sqp]
2020-05-04 11:14:05   --> charge.succeeded [evt_1Gex9OG8lTpkPNJEjnEMPWZK]
2020-05-04 11:14:05  <--  [200] POST http://localhost:4242/webhook [evt_1Gex9OG8lTpkPNJEjnEMPWZK]
```

#### Insufficient Balance Test

1. Shut down the previous instances of frontend and backend if running and restart them. This should make your cart full again.

1. Verify your cart is full of the items Nike Zoom Fly 2 units by going to http://localhost:4242/get-cart. Your total of 300 should be visible at http://localhost:4242/get-total.

1. Go to [http://localhost:3000/checkout](http://localhost:3000/checkout). Enter your name and email address in the form provided. Enter card details "4000 0000 0000 9995" for testing a successful payment. Enter any valid values for the rest of the options such as CVV, expiration date and zip code. Press "Pay". You should see the payment getting failed with an insufficient balance message.

1. Verify your total is still 300 and you cart is full of the same items by going to http://localhost:4242/get-total and  http://localhost:4242/get-cart respectively.

1. Your webhook listener should report events such as:

```
2020-05-04 13:05:39  <--  [200] POST http://localhost:4242/webhook [evt_1GeytdG8lTpkPNJECVG7uZI0]
2020-05-04 13:05:40   --> payment_intent.created [evt_1GeyteG8lTpkPNJEe5k4r8cd]
2020-05-04 13:05:40  <--  [200] POST http://localhost:4242/webhook [evt_1GeyteG8lTpkPNJEe5k4r8cd]
2020-05-04 13:05:45   --> charge.failed [evt_1GeytjG8lTpkPNJEoV9XSQva]
2020-05-04 13:05:45  <--  [200] POST http://localhost:4242/webhook [evt_1GeytjG8lTpkPNJEoV9XSQva]
2020-05-04 13:05:46   --> payment_intent.payment_failed [evt_1GeytjG8lTpkPNJEDkm5R1qb]
2020-05-04 13:05:46  <--  [200] POST http://localhost:4242/webhook [evt_1GeytjG8lTpkPNJEDkm5R1qb]
```
