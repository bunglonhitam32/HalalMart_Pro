from django.db import models

class Produk(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.IntegerField()
    stok = models.IntegerField()
    halal = models.BooleanField(default=True)

    def __str__(self):
        return self.nama
    
class Transaksi(models.Model):
    produk = models.ForeignKey(
        Produk,
        on_delete=models.CASCADE
    )

    jumlah = models.IntegerField()

    total_harga = models.IntegerField()

    tanggal = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.produk.nama} - {self.jumlah}"