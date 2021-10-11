from django import forms
from .models  import Brand, Model, Varian, Material


class VarianForm(forms.ModelForm):
    #akses kelas dari model
    class Meta:
        model = Varian
        fields = [
            'idBrand',
            'namaBrand',
            'idModel',
            'namaModel',
            'idVarian',
            'namaVarian',
            'namaAtribut',
            'nilaiAtribut',
        ]

        labels = {
            'idBrand': 'ID Brand',
            'namaBrand': 'Nama Brand',
            'idModel': 'ID Model',
            'namaModel':'Nama Model',
            'idVarian': 'ID Varian',
            'namaVarian':'Nama Varian',
            'namaAtribut':'Nama Atribut',
            'nilaiAtribut':'Nilai Atribut',
        }
        widgets = {
            'idBrand': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan ID brand',
                }
            ),
            'namaBrand': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama brand',
                }
            ),
            'idModel': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan ID model',
                }
            ),
            'namaModel': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama model',
                }
            ),
            'idVarian': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan ID varian',
                }
            ),
            'namaVarian': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Masukkan nama varian',
                }
            ),
            'namaAtribut': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama atribut',
                }
            ),
            'nilaiAtribut': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nilai atribut',
                }
            ),
        }

class MaterialForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['penyusunProduk'].queryset = Material.objects.filter(is_berlaku=True).order_by('varian')
        self.fields['penyusunProduk'].label_from_instance = lambda obj: "%s - %s" % (obj.varian,obj.idMaterial)

    #akses kelas dari model
    class Meta:
        model = Material
        fields = [
            'varian',
            'idMaterial',
            'namaMaterial',
            'namaSupplier',
            'penyusunProduk',
            'tanggalMulaiBerlaku',
        ]

        labels = {
            'varian':'ID Varian',
            'idMaterial':'ID Material',
            'namaMaterial':'Nama Material',
            'namaSupplier':'Nama Supplier',
            'penyusunProduk':'Penyusun Produk',
            'tanggalMulaiBerlaku':'Tanggal Material Mulai Berlaku*',
        }
        widgets = {
            'idMaterial': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan ID material',
                }
            ),
            'namaMaterial': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama material',
                }
            ),
            'namaSupplier': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama supplier',
                }
            ),
            'tanggalMulaiBerlaku': forms.TimeInput(
                attrs={
                    'type': 'date',
                }
            ),
        }


class MaterialPenggantiForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(MaterialPenggantiForm, self).__init__(*args, **kwargs)
        self.fields['penyusunProduk'].queryset = Material.objects.filter(is_berlaku=True).order_by('varian')
        self.fields['penyusunProduk'].label_from_instance = lambda obj: "%s - %s" % (obj.varian,obj.idMaterial)
    #akses kelas dari model
    class Meta:
        model = Material
        fields = [
            'varian',
            'idMaterial',
            'namaMaterial',
            'namaSupplier',
            'penyusunProduk',
        ]

        labels = {
            'varian':'ID Varian',
            'idMaterial':'ID Material',
            'namaMaterial':'Nama Material',
            'namaSupplier':'Nama Supplier',
            'penyusunProduk':'Penyusun Produk',
        }
        widgets = {
            'idMaterial': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan ID material',
                }
            ),
            'namaMaterial': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama material',
                }
            ),
            'namaSupplier': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Masukkan nama supplier',
                }
            ),
        }