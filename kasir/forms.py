from django import forms
from .models import Produk

class TransaksiForm(forms.Form):
    produk = forms.ModelChoiceField(
        queryset=Produk.objects.all()
    )

    jumlah = forms.IntegerField(min_value=1)