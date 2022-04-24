### Assumptions:

1. This is a staging or a production service that will deal with real data of Indian customers.
2. Transactions will always be performed using either a UPI ID or an account number.
3. The users have to be registered with the platform to send money.
4. The users do not have to be registered with the platform to receive money.
5. Transaction numbers can be universally unique.
6. DecimalField is giving some unusual issues so assuming that transactions are integers