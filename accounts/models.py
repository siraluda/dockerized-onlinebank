from django.db import models
from users.models import CustomerProfile


ACCOUNT_TYPES = [
    ('SAVINGS', 'Savings'),
    ('CHECKING', 'Checking'),
]

TRANSACTION_TYPE = [
    ('WITHDRAWAL', 'Withdrawal'),
    ('DEPOSIT', 'Deposit'),
]


class CustomerAccount(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=100, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.customer) + " " + str(self.account_type) 


class Transaction(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=50, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.customer) 
