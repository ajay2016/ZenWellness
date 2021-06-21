from django import forms
from .models import ProductTransaction


class WarehouseTransactionForm(forms.ModelForm):
    class Meta:
        model = ProductTransaction
        fields = [
            'product', 'transaction_type', 'rate', 'quantity',
            'discount', 'brand', 'company'
        ]


class WarehouseTransactionUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductTransaction
        fields = [
            'rate', 'quantity', 'discount', 'brand', 'company'
        ]
