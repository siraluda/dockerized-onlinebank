from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from django.core import serializers
from django.views.generic import DetailView, View

from .models import CustomerAccount, Transaction
from users.models import CustomerProfile
from .forms import CreateAccountForm, CreateTransactionForm, AccountsTransferForm

from .utility_funcs import (
_customer_total_transactions, 
_customer_total_balance,
_check_customer_account_exist,
_update_customer_balance,
)



def customerDashboardView(request, pk):

    template_name = 'accounts/dashboard.html'

    # forms
    forms = {
        "transaction": CreateTransactionForm(),
        "create_account": CreateAccountForm(),
        "accounts_transfer": AccountsTransferForm(),
    }

    # get the current logged in customer's profile, accounts and transaction details
    customer_profile = CustomerProfile.objects.get(id=pk)
    customer_accounts = CustomerAccount.objects.filter(
        customer__customer__id=pk)
    customer_transactions = Transaction.objects.filter(
        customer__customer__id=pk).order_by('-transaction_date')

    # Customer's total withdrawals and deposits
    customer_total_withdrawal = _customer_total_transactions(pk, "WITHDRAWAL") if _customer_total_transactions(pk, "WITHDRAWAL") else 0
    customer_total_deposit = _customer_total_transactions(pk, "DEPOSIT") if _customer_total_transactions(pk, "DEPOSIT") else 0

    trans_totals = {
        "total_deposit": customer_total_deposit, 
        "total_withdrawal": customer_total_withdrawal,
    }

    # customer's total balance
    total_balance = _customer_total_balance(pk) if _customer_total_balance(pk) else 0

    context = {
        "customer_profile": customer_profile,
        "customer_accounts": customer_accounts,
        "customer_transactions": customer_transactions,
        "forms": forms,
        "total_balance": total_balance,
        "totals": trans_totals
    }

    return render(request, template_name, context)


def performTransaction(request):

    if request.is_ajax and request.method == 'POST':
        t_form = CreateTransactionForm(request.POST)

        if t_form.is_valid():

            account_type = t_form.cleaned_data['account_type']
            transaction_type = t_form.cleaned_data['transaction_type']
            amount = t_form.cleaned_data['amount']

            customer_id = request.user.id

            # check if customer account exist
            if not _check_customer_account_exist(id=customer_id, account_type=account_type):
                return JsonResponse({'error': f'Sorry, you don\'t have a {account_type} account'}, status=200)
            
            else:
                try:
                    # update customer account
                    _update_customer_balance(
                        customer_id, account_type, transaction_type, amount)

                except Exception:
                    return JsonResponse({'error': 'Sorry, you have insufficent balance'}, status=200)

                else:
                    # customer object
                    customer = get_object_or_404(CustomerProfile, id=customer_id)

                    # use account_type to find customer's account object
                    customer_account_type = get_object_or_404(
                        CustomerAccount, customer=customer, account_type=account_type)

                    # create new transaction object in database
                    new_transaction = Transaction(
                        customer=customer, account=customer_account_type, 
                        transaction_type=transaction_type, amount=amount)
                    new_transaction.save()

                    # get customer's balance
                    total_balance = _customer_total_balance(customer_id)

                    # Get updated balance in customer's account
                    customer_accounts = serializers.serialize("json", 
                    CustomerAccount.objects.filter(customer__customer__id=customer_id))
                    
                    data = {
                        'amount': amount,
                        'transaction_type': transaction_type,
                        'account_type': account_type,
                        'total_balance': total_balance,
                        'customer_accounts': customer_accounts
                    }

                    return JsonResponse({'data': data}, status=200)
        else:
            return JsonResponse({'error': t_form.errors}, status=400)
    else:
        return JsonResponse({'error': "Invalid form submission method"}, status=400)


def createAccount(request):
    if request.is_ajax and request.method == 'POST':
        create_account_form = CreateAccountForm(request.POST)

        if create_account_form.is_valid():
            account_type = create_account_form.cleaned_data['account_type']

            # check if the type of account the customer is trying to create already exists
            if not _check_customer_account_exist(request.user.id, account_type):
                new_account = CustomerAccount(
                    customer=request.user.customerprofile, account_type=account_type)
                new_account.save()
                return JsonResponse({"success":f"{account_type} account added!"})

            return JsonResponse({"error": f"Sorry, You already have a {account_type} account"})


def accountsTransfer(request):
    if request.is_ajax and request.method == 'POST':
        accounts_transfer_form = AccountsTransferForm(request.POST)
    
    if accounts_transfer_form.is_valid():
        from_ = accounts_transfer_form.cleaned_data['from_']
        to = accounts_transfer_form.cleaned_data['to']
        amount = accounts_transfer_form.cleaned_data['amount']

        if from_ == to:
            return JsonResponse({'error': 'You have selected the same accounts'}, status=200)
        
        else:
            try:
                _update_customer_balance(request.user.id, from_, 'WITHDRAWAL', amount)

            except Exception:
                return JsonResponse({'error': 'Sorry, you have insufficent balance'}, status=200)
            
            else:
                _update_customer_balance(request.user.id, to, 'DEPOSIT', amount)
                return JsonResponse({"success":f"${amount} transfered from {from_} to {to}!"})



