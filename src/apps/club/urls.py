from django.urls import path
from . import views

app_name = 'apps.club'
urlpatterns = [
    path('d', views.Dashboard.as_view(), name='dashboard'),
    path('transaction/add', views.TransactionAdd.as_view(), name='transaction_add'),
    path('wallet/<int:user_id>/spend', views.SpendWallet.as_view(), name='wallet_spend'),
]
