from django.test import TestCase, Client
from .models import CustomerAccount, Transaction
from users.models import CustomerProfile
from django.contrib.auth import get_user_model

class CustomerAccountTest(TestCase):
    
    def setUp(self):

        self.user = get_user_model().objects.create_user(
            email = 'test@email.com', password = 'testing123')

        self.customer_profile = CustomerProfile(

            customer= self.user,
            phone_number = '+1-234-467-8910', 
            date_of_birth = '01/13/1992',
            address = '23 Wall St',
            city = 'St. Johns',
            postalcode = 'A1B2C3',        
            )

        self.customer_savings_account = CustomerAccount(
            customer = self.customer_profile, 
            account_type = 'Savings', 
            balance = 1000)
        
        self.customer_checking_account = CustomerAccount(
            customer = self.customer_profile, 
            account_type = 'Checking', 
            balance = 1000)

        self.customer_withdrawal_transaction = Transaction(
            customer = self.customer_profile,
            account = self.customer_savings_account,
            transaction_type = "Withdrawal",
            amount = 700,
        )

        self.customer_deposit_transaction = Transaction(
            customer = self.customer_profile,
            account = self.customer_checking_account,
            transaction_type = "Deposit",
            amount = 500,
        )


    def test_create_customer_accounts(self):    
        self.assertTrue(isinstance(self.customer_savings_account, CustomerAccount))
        self.assertTrue(isinstance(self.customer_checking_account, CustomerAccount))

    def test_customer_transaction(self):
        self.assertTrue(isinstance(self.customer_withdrawal_transaction, Transaction))
        self.assertTrue(isinstance(self.customer_deposit_transaction, Transaction))
        



