# Stripe PaymentIntent API Integration

Welcome to the ecommerce store for Sneakers!

![Sneakerfeather](https://github.com/manjotpahwa/stripe-assignment/images/Shoe_feather.png)

As an owner of an ecommerce store, you will want to integrate with the payments API for Stripe. This is a simple way to build a checkout form that collects card details. Included are some basic build and run scripts you can use to start up the application.

## Running the sample

1. Build the server

```
pip3 install -r requirements.txt
```

2. Run the server
Specify the FLASK_APP environment variable and the FLASK_ENV (so that you can see debug logs for a local run of the app).

```
export FLASK_APP=server.py
export FLASK_ENV=development
python3 -m flask run --port=4242
```
Navigate to http://localhost:4242/ to verify your server is up and running. 
To view your total amount go to http://localhost:4242/get-total and to view your cart go to http://localhost:4242/get-cart

3. Build the frontend client app
Run the following to install all dependencies needed.
```
npm install
```

4. Run the client app

```
npm start
```

5. Go to [http://localhost:3000/checkout](http://localhost:3000/checkout)

Enter your name and email address in the form provided. Enter card details such as "4242 4242 4242 4242" for testing a successful payment. Enter any valid values for the rest of the options such as CVV, expiration date and zip code. Press "Pay". You should see the payment go through successfully.
