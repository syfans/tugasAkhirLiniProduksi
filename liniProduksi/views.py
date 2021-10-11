from django.shortcuts import render, redirect

from .models import LiniProduksi
from .forms import LiniProduksiForm
# Create your views here.

# def liniProduksi(request, idBrandInput, idModelInput, idVarianInput):
#     # if request.method=="POST":
#     #     fromdate = request.POST.get('fromdate')
#     #     todate = request.POST.get('todate')
#     #     namaLP = request.POST.get('namaLP')
#     #     searchresult = LiniProduksi.objects.raw('select id,idLiniProduksi,waktuMulaiProduksi,waktuSelesaiProduksi,waktuSiklus,tanggalMulaiProduksi FROM produk_liniproduksi WHERE ((idLiniProduksi = "'+namaLP+'") OR (tanggalMulaiProduksi between "'+fromdate+'" and "'+todate+'")) ')
#     #     context = {
#     #         'Judul': 'Lini Produksi',
#     #         'semua_liniProduksi': searchresult,
#     #
#     #         'css': 'produk/css/styles_table.css',
#     #     }
#     #     return render(request,'produk/index.html', context)
#     # else:
#     model_p = LiniProduksi.objects.filter(brand__id=idBrandInput)
#     varian_p = Varian.objects.filter(id=idVarianInput)
#     liniProduksi = LiniProduksi.objects.filter(varian__id=idVarianInput)
#     context = {
#         'Judul': 'Lini Produksi',
#         'liniProduksi': liniProduksi,
#         'model_p':model_p,
#         'varian_p': varian_p,
#         'css': 'produk/css/styles_table.css',
#     }
#     return render(request,'produk/liniProduksi.html',context)

def index(request):
    liniProduksi = LiniProduksi.objects.all()

    context = {
        'Judul': 'Lini Produksi',
        'liniProduksi': liniProduksi,
        'css': 'produk/css/styles_table.css',
    }
    return render(request, 'liniProduksi/indexV2.html', context)


def newLiniProduksi(request):
    #cara mencocokan antara input dengan data yang telah ada = PostForm(request.POST)
    liniProduksi_form = LiniProduksiForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        # validasi data
        if liniProduksi_form.is_valid():
            # menyimpan ke database
            liniProduksi_form.save()
            return redirect('liniProduksi:index')
    context = {
        'Judul': 'Tambah Lini Produksi',
        'css': 'produk/css/styles_form.css',
        'liniProduksi_form': liniProduksi_form,
    }
    return render(request,'liniProduksi/newLiniProduksi.html',context)

def deleteLiniProduksi(request, delete_id):
    #cara delete
    LiniProduksi.objects.filter(id=delete_id).delete()
    return redirect('liniProduksi:index')

def updateLiniProduksi(request, update_id):
    #cara edit
    liniProduksi_update = LiniProduksi.objects.get(id=update_id)

    data = {
        'idLiniProduksi': liniProduksi_update.idLiniProduksi,
        'waktuSiklus': liniProduksi_update.waktuSiklus,
        'jumlahStasiunKerja': liniProduksi_update.jumlahStasiunKerja,
    }
    liniProduksi_form = LiniProduksiForm(request.POST or None, initial=data, instance=liniProduksi_update)

    if request.method == 'POST':
        #validasi data
        if liniProduksi_form.is_valid():
            #menyimpan ke database
            liniProduksi_form.save()
            return redirect('liniProduksi:index')

    context = {
        'Judul': 'Update Lini Produksi',
        'liniProduksi_form': liniProduksi_form,
    }

    return render(request,'liniProduksi/newLiniProduksi.html',context)