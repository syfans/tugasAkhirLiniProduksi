from django.shortcuts import render, redirect

from .models import Brand, Model, Varian
from .forms import VarianForm
# Create your views here.

def index(request):
    varian = Varian.objects.all()

    context = {
        'Judul': 'Brand-Model-Varian',
        'varian': varian,
        'css': 'produk/css/styles_table.css',
    }
    return render(request,'produk/indexV2.html',context)

def varian(request, idBrandInput, idModelInput):
    varian_p = Varian.objects.all()
    # brand = Brand.objects.all()
    # model_p = Model.objects.filter(brand__id=idBrandInput)
    # varian_p = Varian.objects.filter(model__id=idModelInput)
    # model_title = Model.objects.filter(id=idModelInput)
    # list_model = list(model_title)
    # brand_title = Brand.objects.filter(id=idBrandInput)
    # list_brand = list(brand_title)
    #
    context = {
        'Judul': 'Brand-Model-Varian',
        # 'brand': brand,
        # 'model_p': model_p,
        'varian_p': varian_p,
        # 'list_brand': list_brand,
        # 'list_model': list_model,

    }
    return render(request,'produk/varian.html',context)

def newVarian(request):
    #cara mencocokan antara input dengan data yang telah ada = PostForm(request.POST)
    varian_form = VarianForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        #validasi data
        if varian_form.is_valid():
            #menyimpan ke database
            varian_form.save()
            return redirect('produk:index')

    context = {
        'Judul': 'Tambah Brand-Model-Varian',
        'varian_form': varian_form,
    }
    return render(request,'produk/newVarian.html',context)

def deleteVarian(request, delete_id):
    #cara delete
    Varian.objects.filter(id=delete_id).delete()
    return redirect('produk:index')

def updateVarian(request, update_id):
    #cara edit
    varian_update = Varian.objects.get(id=update_id)

    data = {
        'model':varian_update.model,
        'namaVarian': varian_update.namaVarian,
    }
    varian_form = VarianForm(request.POST or None, initial=data, instance=varian_update)

    if request.method == 'POST':
        #validasi data
        if varian_form.is_valid():
            #menyimpan ke database
            varian_form.save()
            return redirect('produk:index')

    context = {
        'Judul': 'Update Brand-Model-Varian',
        'varian_form': varian_form,
    }

    return render(request,'produk/newVarian.html',context)