### Assumptions:

1. This is a staging or a production service that will deal with real data of Indian customers.
2. Transactions will always be performed using either a UPI ID or an account number.
3. The users have to be registered with the platform to send money.
4. The users do not have to be registered with the platform to receive money.
5. Transaction numbers can be universally unique.

### Validations:
Good fraud prevention starts with validation measures like KYC so I have implemented basic validations. Phone number, bank account must be Indian. UPI ID must follow the usual format
### Fraud Scenarios:
- UPI ID and phone number belong to the same user for a transaction.
- More than 50 transaction requests (even with different amounts) by the same IP in the last minute (rate-limit).
- More than 10 transactions of the same amount within 2 minutes (from the same user).
- More than 30 transactions of the same amount within 2 minutes (from any user, to prevent Bangladesh-like heist).
- If a user has more than 1 fraudulent transaction in a cool-down period of last 30 days, the current transaction will also be marked as fraudulent

### Instructions to run:

1. Setup a virtual environment:
```sh
$ pip install virtualenv
$ virtualenv venv
$ venv/scripts/activate
```

2. Install the required dependencies after activating the virtual environment
```sh
$ pip install -r requirements.txt
```

3. Run the server directly since migration files and test DB is present in the repo (not recommended in actual work setup)
```sh
$ python manage.py runserver
```

4. Use a client like Postman or Thunder Client to make requests to the API endpoint:
 http://localhost:8000/core/check-fraud/

#### Sample request data based on the test DB:

##### Not a terrorist, so it will work: Make this a terrorist by sending more than 10 requests in 2 mins
{
    "sender": "9999999998",
    "amount": 131.2345,
    "receiver_account_number": "12910234234"
}
##### Not a terrorist, so it will work: Do not make this number a terrorist, keep this number clean
{
    "sender": "9999999997",
    "amount": 11.2345,
    "receiver_account_number": "12910234234"
}

##### Got a terrorist response less than 30 days ago, so it will again be marked as terrorist:
{
    "sender": "9999999999",
    "amount": 121.2345,
    "receiver_account_number": "12910234234"
}

5. Run tests using the installed coverage package
```sh
$ coverage run manage.py test
$ coverage report
```