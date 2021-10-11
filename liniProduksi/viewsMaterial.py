from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import KebutuhanMaterial, Proses, StasiunKerja
from .forms import KebutuhanMaterialForm
from produk.models import Varian
from produk.models import Material
from django.db.models import Count, F


def newMaterial(request):
    kebutuhanMaterial_form = KebutuhanMaterialForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        id = request.POST.get('id')
        proses = request.POST.get('proses')
        material = request.POST.get('material')

        proses_sk = Proses.objects.get(idProses=proses)
        p_sk = str(proses_sk.stasiunKerja)
        idm = Material.objects.get(id=material)
        mid = str(idm.idMaterial)
        var = str(idm.varian)
        varmat = Varian.objects.get(idVarian = var)
        idmaterial = Material.objects.filter(idMaterial=mid, varian = varmat).first()
        stasiunKerja = StasiunKerja.objects.get(idStasiunKerja=p_sk)

        KebutuhanMaterial.objects.create(id=id, stasiunKerja=stasiunKerja,material=idm, proses=proses_sk,)

        material = KebutuhanMaterial.objects.filter(stasiunKerja=stasiunKerja).filter(material__idMaterial=idmaterial, material__varian = varmat).first()
        km = material.jumlahMaterialPerCycleTime
        kumulatif = km+1

        KebutuhanMaterial.objects.filter(material__idMaterial=idmaterial, material__varian = varmat).update(jumlahMaterialPerCycleTime=kumulatif)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    context = {
        'Judul': 'Tambah Kebutuhan Material',
        'kebutuhanMaterial_form': kebutuhanMaterial_form,
    }
    return render(request, 'liniProduksi/newMaterial.html', context)

def deleteMaterial(request, delete_id):
    #cara delete
    KebutuhanMaterial.objects.filter(id=delete_id).delete()
    next = request.POST.get('next', '/')
    if request.method == 'GET':
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)

def updateMaterial(request, update_id):
    #cara edit Produk
    kebutuhanMaterial_update = KebutuhanMaterial.objects.get(id=update_id)
    kebutuhanMaterial_form = KebutuhanMaterialForm(request.POST or None, instance=kebutuhanMaterial_update)

    if request.method == 'POST':
        proses = request.POST.get('proses')
        material = request.POST.get('material')

        proses_sk = Proses.objects.get(idProses=proses)
        p_sk = str(proses_sk.stasiunKerja)
        idm = Material.objects.get(id=material)
        stasiunKerja = StasiunKerja.objects.get(idStasiunKerja=p_sk)

        KebutuhanMaterial.objects.filter(id=update_id).update(stasiunKerja=stasiunKerja,material=idm, proses=proses_sk,)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    context = {
        'Judul': 'Update Kebutuhan Material',
        'kebutuhanMaterial_form': kebutuhanMaterial_form,
    }

    return render(request,'liniProduksi/newMaterial.html',context)