from django import forms
from .models import Produk


class TransaksiForm(forms.Form):

    produk = forms.ModelChoiceField(
        queryset=Produk.objects.all()
    )

    jumlah = forms.IntegerField()


class ProdukForm(forms.ModelForm):

    class Meta:
        model = Produk
        fields = [
            'nama',
            'harga',
            'stok',
            'halal'
        ]