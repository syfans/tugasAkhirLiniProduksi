from django import forms
from .models  import LiniProduksi, StasiunKerja, KebutuhanMaterial, Proses, PeralatanProduksi, Operator, ProduksiHarian, PengirimanMaterial, Gangguan, WaktuIstirahat, TargetHarian, TargetMingguan, TargetBulanan, TargetTahunan
from django.contrib.auth.models import User
from produk.models import Material
from django.db.models import Q
import datetime


class LiniProduksiForm(forms.ModelForm):
    #akses kelas dari model
    class Meta:
        model = LiniProduksi
        fields = [
            'idLiniProduksi',
            'waktuSiklus',
            'jumlahStasiunKerja',
        ]

        labels = {
            'idLiniProduksi':'ID Lini Produksi',
            'waktuSiklus':'Waktu Siklus (detik)',
            'jumlahStasiunKerja':'Jumlah Stasiun Kerja',
        }
        widgets = {
            'idLiniProduksi': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Masukkan id lini produksi',
                }
            ),
            'waktuSiklus': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan waktu siklus',
                }
            ),
            'jumlahStasiunKerja': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan jumlah stasiun kerja',
                }
            ),
        }


class ProduksiHarianForm(forms.ModelForm):
    class Meta:
        model = ProduksiHarian
        fields = [
            'liniProduksi',
            'tanggalProduksi',
            'is_lembur',
            'kondisiIstirahat',
            ]

        labels = {
            'liniProduksi':'ID Lini Produksi',
            'tanggalProduksi':'Tanggal Produksi',
            'is_lembur':'Apabila target belum tercapai, apakah akan lembur atau tidak lembur?*',
            'kondisiIstirahat': 'Apakah waktu istirahat normal atau customize?',
        }
        widgets = {
            'tanggalProduksi': forms.TimeInput(
                attrs={
                    'type': 'date',
                }
            ),
        }


class HariLiburForm(forms.ModelForm):
    class Meta:
        model = ProduksiHarian
        fields = [
            'liniProduksi',
            'tanggalProduksi',
            'alasanLibur'
            ]

        labels = {
            'liniProduksi':'ID Lini Produksi',
            'tanggalProduksi':'Tanggal Libur',
            'alasanLibur':'Alasan Libur',
        }
        widgets = {
            'tanggalProduksi': forms.TimeInput(
                attrs={
                    'type': 'date',
                }
            ),
            'alasanLibur': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan alasan libur',
                }
            ),
        }


class WaktuIstirahatForm(forms.ModelForm):
    #akses kelas dari model
    class Meta:
        model = WaktuIstirahat
        fields = [
            'waktuMulaiIstirahat',
            'waktuSelesaiIstirahat',
        ]

        labels = {
            'waktuMulaiIstirahat': 'Waktu Mulai Istirahat',
            'waktuSelesaiIstirahat': 'Waktu Selesai Istirahat',
        }
        widgets = {
            'waktuMulaiIstirahat': forms.TimeInput(
                attrs={
                    'type': 'time',
                }
            ),
            'waktuSelesaiIstirahat': forms.TimeInput(
                attrs={
                    'type': 'time',
                }
            ),
        }


class TargetHarianForm(forms.ModelForm):
    #akses kelas dari model
    class Meta:
        model = TargetHarian
        fields = [
            'varian',
            'target',
            'waktuMulaiProduksi',
            'waktuSelesaiProduksi',
        ]

        labels = {
            'varian':'ID Varian',
            'target': 'Target Produksi',
            'waktuMulaiProduksi': 'Waktu Mulai Produksi',
            'waktuSelesaiProduksi': 'Waktu Selesai Produksi',
        }

        widgets = {
            'target': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan target produksi',
                }
            ),
            'waktuMulaiProduksi': forms.TimeInput(
                attrs={
                    'type': 'time',
                }
            ),
            'waktuSelesaiProduksi': forms.TimeInput(
                attrs={
                    'type': 'time',
                }
            ),
        }


class TargetMingguanForm(forms.ModelForm):
    #akses kelas dari model
    class Meta:
        model = TargetMingguan
        fields = [
            'varian',
            'liniProduksi',
            'minggu',
            'target',
        ]

        labels = {
            'varian': 'ID Varian',
            'liniProduksi': 'ID Lini Produksi',
            'minggu': 'Minggu ke-',
            'target': 'Target Produksi',
        }

        help_texts = {
            'minggu': 'Pilih salah satu tanggal pada minggu tersebut',
        }

        widgets = {
            'minggu': forms.TimeInput(
                attrs={
                    'type': 'date',

                }
            ),
            'target': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan target produksi',
                }
            ),
        }


class TargetBulananForm(forms.ModelForm):
    #akses kelas dari model
    class Meta:
        model = TargetBulanan
        fields = [
            'varian',
            'liniProduksi',
            'bulan',
            'target',
        ]

        labels = {
            'varian': 'ID Varian',
            'liniProduksi': 'ID Lini Produksi',
            'bulan': 'Bulan ke-',
            'target': 'Target Produksi',
        }

        help_texts = {
            'bulan': 'Pilih salah satu tanggal pada bulan tersebut',
        }

        widgets = {
            'bulan': forms.TimeInput(
                attrs={
                    'type': 'date',

                }
            ),
            'target': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan target produksi',
                }
            ),
        }


class TargetTahunanForm(forms.ModelForm):
    #akses kelas dari model
    class Meta:
        model = TargetTahunan
        fields = [
            'varian',
            'liniProduksi',
            'tahun',
            'target',
        ]

        labels = {
            'varian': 'ID Varian',
            'liniProduksi': 'ID Lini Produksi',
            'tahun': 'Tahun',
            'target': 'Target Produksi',
        }

        help_texts = {
            'tahun': 'Pilih salah satu tanggal pada tahun tersebut',
        }

        widgets = {
            'tahun': forms.TimeInput(
                attrs={
                    'type': 'date',

                }
            ),
            'target': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan target produksi',
                }
            ),
        }


class StasiunKerjaForm(forms.ModelForm):
    #akses kelas dari model
    class Meta:
        model = StasiunKerja
        fields = [
            'liniProduksi',
            'idStasiunKerja',
            'nomorStasiunKerja',
            'sisiStasiunKerja',
        ]

        labels = {
            'liniProduksi':'ID Lini Produksi',
            'idStasiunKerja': 'ID Stasiun Kerja',
            'nomorStasiunKerja': 'Nomor Stasiun Kerja',
            'sisiStasiunKerja':'Sisi Stasiun Kerja',
        }
        widgets = {
            'idStasiunKerja': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan id stasiun kerja',
                }
            ),
            'nomorStasiunKerja': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nomor stasiun kerja',
                }
            ),
            'sisiStasiunKerja': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


class KebutuhanMaterialForm(forms.ModelForm):
    #akses kelas dari model
    def __init__(self, material,*args, **kwargs):
        super(KebutuhanMaterialForm, self).__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.filter(namaSupplier__isnull=False).filter((Q(tanggalGanti__gt=datetime.datetime.today()) & Q(tanggalMulaiBerlaku__lte=datetime.datetime.today()))|(Q(tanggalGanti__isnull=True) & Q(tanggalMulaiBerlaku__lte=datetime.datetime.today()))).filter(Q(kebutuhanMaterial=self.instance))
        self.fields['material'].label_from_instance = lambda obj: "%s || Varian: %s || Penyusun produk: %s || Supplier: %s" % (obj.idMaterial, obj.varian, obj.penyusunProduk, obj.namaSupplier)

    class Meta:
        model = KebutuhanMaterial
        fields = [
            'proses',
            'material',
        ]

        labels = {
            'proses':'ID Proses',
            'material':'ID Material',
        }


class ProsesForm(forms.ModelForm):
    class Meta:
        model = Proses
        fields = [
            'stasiunKerja',
            'idProses',
            'namaProses',
            'durasiProses',
            'tanggalMulaiBerlaku',
        ]

        labels = {
            'stasiunKerja':'ID Stasiun Kerja',
            'idProses':'ID Proses',
            'namaProses': 'Nama Proses',
            'durasiProses': 'Durasi Proses (detik)',
            'tanggalMulaiBerlaku': 'Tanggal Mulai Berlaku*'
        }

        widgets = {
            'idProses': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan id Proses',
                }
            ),
            'namaProses': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama Proses',
                }
            ),
            'durasiProses': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan durasi proses dalam detik',
                }
            ),
            'tanggalMulaiBerlaku': forms.TimeInput(
                attrs={
                    'type': 'date',
                }
            ),
        }


class ProsesGantiForm(forms.ModelForm):
    class Meta:
        model = Proses
        fields = [
            'stasiunKerja',
            'idProses',
            'namaProses',
            'durasiProses',
        ]

        labels = {
            'stasiunKerja':'ID Stasiun Kerja',
            'idProses':'ID Proses',
            'namaProses': 'Nama Proses',
            'durasiProses': 'Durasi Proses (detik)',
        }

        widgets = {
            'idProses': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan id Proses',
                }
            ),
            'namaProses': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama Proses',
                }
            ),
            'durasiProses': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan durasi proses dalam detik',
                }
            ),
        }


class ProsesBerlakuForm(forms.ModelForm):
    class Meta:
        model = Proses
        fields = [
            'is_berlaku',
        ]

        labels = {
            'stasiunKerja':'ID Stasiun Kerja',
            'idProses':'ID Proses',
            'namaProses': 'Nama Proses',
            'durasiProses': 'Durasi Proses (detik)',
        }

        widgets = {
            'idProses': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan id Proses',
                }
            ),
        }


class PeralatanProduksiForm(forms.ModelForm):
    class Meta:
        model = PeralatanProduksi
        fields = [
            'proses',
            'idPeralatan',
            'jenisPeralatan',
        ]

        labels = {
            'proses':'ID Proses',
            'idPeralatan': 'ID Peralatan',
            'jenisPeralatan': 'Jenis Peralatan',
        }

        widgets = {
            'idPeralatan': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan id peralatan',
                }
            ),
            'jenisPeralatan': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan jenis peralatan',
                }
            ),
        }

class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = [
            'proses',
            'namaLengkap',
            'levelOperator',
        ]

        labels = {
            'proses':'ID Proses',
            'namaLengkap':'Nama Operator',
            'levelOperator':'Level Operator',
        }
        widgets = {
            'namaLengkap': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama lengkap operator',
                }
            ),
            'levelOperator': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan level operator',
                }
            ),
        }


class PengirimanMaterialForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(PengirimanMaterialForm, self).__init__(*args, **kwargs)
        self.fields['kebutuhanMaterial'].queryset = KebutuhanMaterial.objects.filter((Q(material__tanggalGanti__gt=datetime.datetime.today()) & Q(material__tanggalMulaiBerlaku__lte=datetime.datetime.today()))|(Q(material__tanggalGanti__isnull=True) & Q(material__tanggalMulaiBerlaku__lte=datetime.datetime.today()))).order_by('proses').filter(Q(pengirimanMaterial=self.instance)).distinct()
        self.fields['kebutuhanMaterial'].label_from_instance = lambda obj: "%s | %s" % (obj.proses.idProses, obj.material.idMaterial)

    class Meta:
        model = PengirimanMaterial
        fields = [
            'kebutuhanMaterial',
            'jumlahMaterialTiapPengiriman',
        ]

        labels = {
            'kebutuhanMaterial':'ID Material',
            'jumlahMaterialTiapPengiriman': 'Jumlah Material Tiap Pengiriman',
        }

        help_texts = {
            'kebutuhanMaterial': 'Jika terdapat dua ID material yang sama dengan proses yang sama, pilih yang pertama',
        }

        widgets = {
            'jumlahMaterialTiapPengiriman': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan jumlah material tiap pengiriman',
                }
            ),
        }


class GangguanForm(forms.ModelForm):
    class Meta:
        model = Gangguan
        fields = [
            'idGangguan',
            'keterangan',
        ]

        labels = {
            'idGangguan': 'ID Gangguan',
            'keterangan': 'Keterangan Gangguan',
        }

        widgets = {
            'idGangguan': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan id gangguan',
                }
            ),
            'keterangan': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan keterangan gangguan yang terjadi',
                }
            ),
        }