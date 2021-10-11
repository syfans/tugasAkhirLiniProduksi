from django import forms
from .models  import EngineeringOrder
from produk.models import Material
from django.db.models import Q

class EOForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EOForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.filter(is_berlaku=True).filter(Q(eo=self.instance))
        self.fields['material'].label_from_instance = lambda obj: "%s || Varian: %s || Penyusun produk: %s || Supplier: %s" % (obj.idMaterial, obj.varian, obj.penyusunProduk, obj.namaSupplier)

    class Meta:
        model = EngineeringOrder
        fields = [
            'material',
            'idEO',
            'namaPengusul',
            'departemenPengusul',
            'keterangan',
        ]

        labels = {
            'material':'Material yang Diajukan untuk Ganti',
            'idEO':'ID Engineering Order',
            'namaPengusul': 'Nama Lengkap Pengusul',
            'departemenPengusul': 'Departemen Pengusul',
            'keterangan': 'Alasan',
        }
        widgets = {
            'idEO': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Masukkan id engineering order',
                }
            ),
            'namaPengusul': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama lengkap pengusul',
                }
            ),
            'departemenPengusul': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan departemen pengusul',
                }
            ),
            'keterangan': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan alasan mengganti material',
                }
            ),
        }

class PersetujuanEOForm(forms.ModelForm):
    class Meta:
        model = EngineeringOrder
        fields = [
            'tanggalPerubahanBerlaku',
        ]

        labels = {
            'tanggalPerubahanBerlaku': 'Tanggal Perubahan Mulai Berlaku',
        }
        widgets = {
            'tanggalPerubahanBerlaku': forms.TimeInput(
                attrs={
                    'type': 'date',
                }
            ),
        }