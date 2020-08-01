from .models import CustomerAccount, Transaction
from django.db.models import Sum


# UTILITY FUNCTIONS

def _update_customer_balance(id, account_type, transaction_type, amount):
    '''Update a customer's account if a deposit or a withdrawal is made'''
    
    current_account_balance = CustomerAccount.objects.get(
        customer__customer__id=id, account_type=account_type).balance

    if transaction_type == "DEPOSIT":
        new_balance = current_account_balance + amount
        return CustomerAccount.objects.filter(
            customer__customer__id=id, account_type=account_type
            ).update(balance=new_balance)

    if transaction_type == "WITHDRAWAL" and current_account_balance > 0:
        new_balance = current_account_balance - amount
        if new_balance >= 0:
            return CustomerAccount.objects.filter(
                customer__customer__id=id, account_type=account_type
                ).update(balance=new_balance)
        else:
            raise Exception
    else:
        raise Exception


def _customer_total_balance(id):
    ''' Sum up the balances in customer's accounts types'''
    return CustomerAccount.objects.filter(customer__customer__id=id).aggregate(Sum('balance')).get('balance__sum')


def _check_customer_account_exist(id, account_type):
    '''Check if the customer already has a Checking or Savings account '''
    try:
        c_account = CustomerAccount.objects.get(
            customer__customer__id=id, account_type=account_type)
    except Exception:
        return False
    else:
        return True


def _customer_total_transactions(pk, transction_type):
    '''Return the total sum of customer withdrawals or deposits'''
    return Transaction.objects.filter(
        customer__customer__id=pk, transaction_type=transction_type).aggregate(Sum('amount')).get('amount__sum')
