from django.shortcuts import render

from .models import LiniProduksi, LiniProduksiHarian


def liniProduksiSemua(request, idLiniProduksiInput):
    liniProduksiHarian = LiniProduksiHarian.objects.filter(liniProduksi__id=idLiniProduksiInput)

    context = {
        'Judul': 'Lini Produksi',
        'liniProduksi': liniProduksi,
        'liniProduksiHarian': liniProduksiHarian,
    }

    return render(request, 'liniProduksi/liniProduksi_semua.html', context)