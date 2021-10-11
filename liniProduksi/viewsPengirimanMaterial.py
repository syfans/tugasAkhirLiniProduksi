from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import PengirimanMaterial, KebutuhanMaterial, StasiunKerja
from .forms import PengirimanMaterialForm
from produk.models import Material


def newPengirimanMaterial(request):
    pengirimanMaterial_form = PengirimanMaterialForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        id = request.POST.get('id')
        kebutuhanMaterial = request.POST.get('kebutuhanMaterial')
        jumlahMaterialTiapPengiriman = request.POST.get('jumlahMaterialTiapPengiriman')


        material_sk = KebutuhanMaterial.objects.get(id=kebutuhanMaterial)
        p_sk = str(material_sk.stasiunKerja)
        stasiunKerja = StasiunKerja.objects.get(idStasiunKerja=p_sk)
        PengirimanMaterial.objects.create(id=id, stasiunKerja=stasiunKerja,kebutuhanMaterial=material_sk, jumlahMaterialTiapPengiriman=jumlahMaterialTiapPengiriman)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    context = {
        'Judul': 'Tambah Informasi Pengiriman Material',
        'pengirimanMaterial_form': pengirimanMaterial_form,
    }
    return render(request, 'liniProduksi/newPengirimanMaterial.html', context)

def deletePengirimanMaterial(request, delete_id):
    #cara delete
    PengirimanMaterial.objects.filter(id=delete_id).delete()
    if request.method == 'GET':
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)

def updatePengirimanMaterial(request, update_id):
    #cara edit Produk
    pengirimanMaterial_update = PengirimanMaterial.objects.get(id=update_id)
    pengirimanMaterial_form = PengirimanMaterialForm(request.POST or None, instance=pengirimanMaterial_update)

    if request.method == 'POST':
        #validasi data
        if pengirimanMaterial_form.is_valid():
            #menyimpan ke database
            pengirimanMaterial_form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'Judul': 'Update Informasi Pengiriman Material',
        'pengirimanMaterial_form': pengirimanMaterial_form,
    }

    return render(request,'liniProduksi/newPengirimanMaterial.html',context)