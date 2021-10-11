from django.shortcuts import render, redirect
from django.db.models import Count
import datetime
from .models import Material, Varian
from .forms import MaterialForm

def newMaterial(request):
    #cara mencocokan antara input dengan data yang telah ada = PostForm(request.POST)
    material_form = MaterialForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        #validasi data
        if material_form.is_valid():
            #menyimpan ke database
            material_form.save()
            return redirect('produk:index')

    context = {
        'Judul': 'Tambah Material',
        'material_form': material_form,
    }
    return render(request,'produk/newMaterial.html',context)

def deleteMaterial(request, delete_id):
    #cara delete
    Material.objects.filter(id=delete_id).delete()
    return redirect('produk:index')

def updateMaterial(request, update_id):
    #cara edit
    material_update = Material.objects.get(id=update_id)

    data = {
        'varian': material_update.varian,
        'idMaterial': material_update.idMaterial,
        'namaMaterial': material_update.namaMaterial,
        'namaSupplier': material_update.namaSupplier,
        'penyusunProduk': material_update.penyusunProduk,
    }
    material_form = MaterialForm(request.POST or None, initial=data, instance=material_update)

    if request.method == 'POST':
        # validasi data
        if material_form.is_valid():
            # menyimpan ke database
            material_form.save()
            return redirect('produk:index')

    context = {
        'Judul': 'Update Material',
        'material_form': material_form,
    }

    return render(request, 'produk/newMaterial.html', context)

def billOfMaterial(request, idVarianInput):
    matVar = Varian.objects.filter(idVarian = idVarianInput)
    mat = Material.objects.filter(varian_id = idVarianInput).filter(is_diubah=False)
    matBOM = Material.objects.filter(varian_id = idVarianInput).filter(namaSupplier__isnull=False).filter(is_diubah=False)
    matBOM_jumlah = matBOM.values('idMaterial','namaMaterial').annotate(jumlahKumulatif=Count('varian')).order_by('idMaterial')
    matBOM_supplier = matBOM.values('idMaterial','namaSupplier').annotate(jumlahKumulatif=Count('varian')).order_by('idMaterial')
    matUbah = Material.objects.filter(varian_id=idVarianInput).filter(is_diubah=True)

    context = {
        'Judul': 'Bill of Material',
        'matVar':matVar,
        'mat': mat,
        'matBOM':matBOM,
        'matBOM_jumlah': matBOM_jumlah,
        'matBOM_supplier': matBOM_supplier,
        'matUbah':matUbah,
    }

    return render(request, 'produk/material.html', context)