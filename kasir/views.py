from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produk, Transaksi
from django.db.models import Sum
from .forms import TransaksiForm, ProdukForm
from .forms import ProdukForm

import requests

def dashboard(request):
    produk = Produk.objects.all()

    jumlah_produk = produk.count()

    total_stok = sum(item.stok for item in produk)

    total_nilai = sum(
        item.harga * item.stok
        for item in produk
    )

    jumlah_transaksi = Transaksi.objects.count()

    total_omzet = (
        Transaksi.objects.aggregate(
            Sum('total_harga')
        )['total_harga__sum']
        or 0
    )

    kurs = 0

    try:
        response = requests.get(
            "https://open.er-api.com/v6/latest/USD"
        )

        data = response.json()

        kurs = data['rates']['IDR']

    except:
        kurs = 0

    produk_hampir_habis = Produk.objects.filter(
        stok__lt=10
    )

    return render(
        request,
        'kasir/dashboard.html',
        {
            'jumlah_produk': jumlah_produk,
            'total_stok': total_stok,
            'total_nilai': total_nilai,
            'jumlah_transaksi': jumlah_transaksi,
            'total_omzet': total_omzet,
            'produk_hampir_habis': produk_hampir_habis,
            'kurs_usd': kurs,
        }
    )

def daftar_produk(request):

    keyword = request.GET.get('q')

    if keyword:
        produk = Produk.objects.filter(
            nama__icontains=keyword
        )
    else:
        produk = Produk.objects.all()

    return render(
        request,
        'kasir/produk.html',
        {
            'produk': produk
        }
    )
def jual_produk(request):

    if request.method == 'POST':

        form = TransaksiForm(request.POST)

        if form.is_valid():

            produk = form.cleaned_data['produk']
            jumlah = form.cleaned_data['jumlah']

            if jumlah > produk.stok:
                return HttpResponse(
                    "Stok tidak mencukupi!"
                )

            total_harga = produk.harga * jumlah

            Transaksi.objects.create(
                produk=produk,
                jumlah=jumlah,
                total_harga=total_harga
            )

            produk.stok -= jumlah
            produk.save()

            return redirect('transaksi')
        
    else:
        form = TransaksiForm()

    return render(
        request,
        'kasir/jual.html',
        {'form': form}
    )

def daftar_transaksi(request):

    transaksi = (
        Transaksi.objects
        .all()
        .order_by('-tanggal')
    )

    return render(
        request,
        'kasir/transaksi.html',
        {
            'transaksi': transaksi
        }
    )

def laporan_keuangan(request):

    jumlah_transaksi = Transaksi.objects.count()

    total_omzet = (
        Transaksi.objects.aggregate(
            Sum('total_harga')
        )['total_harga__sum']
        or 0
    )

    total_produk_terjual = sum(
        transaksi.jumlah
        for transaksi in Transaksi.objects.all()
    )

    return render(
        request,
        'kasir/laporan.html',
        {
            'jumlah_transaksi': jumlah_transaksi,
            'total_omzet': total_omzet,
            'total_produk_terjual': total_produk_terjual,
        }
    )

def reset_stok(request):

    Produk.objects.all().update(stok=100)

    return redirect('dashboard')

def tambah_produk(request):

    if request.method == 'POST':

        form = ProdukForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('produk')

    else:

        form = ProdukForm()

    return render(
        request,
        'kasir/tambah_produk.html',
        {
            'form': form
        }
    )