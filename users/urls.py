from django.urls import path
from .views import index, logout_view, CustomerProfileUpdate, CustomLoginView, SignupView

app_name='users'

urlpatterns=[
    path('', index, name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('customer-profile/', CustomerProfileUpdate.as_view(), name='customer_profile'),
]
