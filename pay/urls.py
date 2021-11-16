from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('wallet/',views.walletPage,name="wallet"),
    path('transfer/',views.transfer,name="transfer"),
    path('confirm/',views.confirmTransfer,name="confirm"),
    path('notification/',views.notificationPage,name="noti"),
    path('notification/<str:pk>/',views.notificationDetail,name="noti-detail"),
    path('transactions/',views.transactionsPage,name="transactions"),
    path('transactions/<str:pk>/',views.transactionDetail,name="transaction-detail"),

    path('scan/',views.scanqr,name="scan-qr"),
    path('receive_qr/',views.receiveQR,name="receive-qr"),
]