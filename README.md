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
- More than 50 transaction requests by the same IP in the last minute (rate-limit).
- More than 10 transactions of the same amount within 2 minutes (from the same user).
- More than 30 transactions of the same amount within 2 minutes (from any user, to prevent Bangladesh-like heist).
- If a user is caught with a fraudulent transaction, all their transactions will keep getting flagged as fraudulent with a cool-down period of 1 month