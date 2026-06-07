from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('produk/', views.daftar_produk, name='produk'),
    path('jual/', views.jual_produk, name='jual'),
    path('transaksi/', views.daftar_transaksi, name='transaksi'),
    path('laporan/', views.laporan_keuangan, name='laporan'),
]