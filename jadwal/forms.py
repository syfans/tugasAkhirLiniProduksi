from django import forms
from .models  import JadwalLiniProduksi
from liniProduksi.models import KebutuhanMaterial
from django.db.models import Q
import datetime
#
# class JadwalLiniProduksiForm(forms.ModelForm):
#     def __init__(self,*args, **kwargs):
#         super(JadwalLiniProduksiForm, self).__init__(*args, **kwargs)
#         self.fields['kebutuhanMaterial'].queryset = KebutuhanMaterial.objects.filter((Q(
#             material__tanggalGanti__gt=datetime.datetime.today()) & Q(
#             material__tanggalMulaiBerlaku__lte=datetime.datetime.today())) | (Q(
#             material__tanggalGanti__isnull=True) & Q(
#             material__tanggalMulaiBerlaku__lte=datetime.datetime.today()))).order_by('proses').distinct()
#         self.fields['kebutuhanMaterial'].label_from_instance = lambda obj: "%s | %s" % (
#         obj.proses.idProses, obj.material.idMaterial)
#
#     #akses kelas dari model
#     class Meta:
#         model = JadwalLiniProduksi
#         fields = [
#             'kebutuhanMaterial',
#             'tanggal',
#
#         ]
#
#         labels = {
#             'kebutuhanMaterial':'ID Material',
#             'tanggal':'Tanggal (dd/mm/yyyy)',
#             'jumlahMaterialTersedia':'Jumlah Material yang Tersedia pada Stasiun Kerja'
#         }
#
#         help_texts = {
#             'kebutuhanMaterial': 'Jika terdapat dua ID material yang sama dengan proses yang sama, pilih yang pertama',
#         }
#
#         widgets = {
#             'tanggal': forms.TimeInput(
#                 attrs={
#                     'type': 'date',
#                 }
#             ),
#             'jumlahMaterialTersedia':forms.NumberInput(
#                 attrs={
#                     'class': 'form-control',
#                     'placeholder': 'Masukkan jumlah material yang tersedia pada stasiun kerja',
#                 }
#             )
#         }