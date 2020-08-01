from django.urls import path
from .views import customerDashboardView, performTransaction, createAccount, accountsTransfer

app_name = "accounts"

urlpatterns = [
    path('customer-account/<int:pk>', customerDashboardView, name='customer-account-page'),
    path('transaction', performTransaction, name='perform_transaction'),
    path('create-account', createAccount, name='create_account'),
    path('accounts-funds-transfer', accountsTransfer, name='accounts_transfer'),
]