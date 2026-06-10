from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('produk/', views.daftar_produk, name='produk'),
    path('jual/', views.jual_produk, name='jual'),
    path('transaksi/', views.daftar_transaksi, name='transaksi'),
    path('laporan/', views.laporan_keuangan, name='laporan'),
    path('reset-stok/', views.reset_stok, name='reset_stok'),
    path('produk/tambah/', views.tambah_produk, name='tambah_produk'),
]