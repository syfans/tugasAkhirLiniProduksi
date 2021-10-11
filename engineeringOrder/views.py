from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import datetime

from .models import EngineeringOrder
from .forms import EOForm, PersetujuanEOForm
from produk.models import Material, Varian
from produk.forms import MaterialPenggantiForm
from liniProduksi.models import KebutuhanMaterial, Proses, StasiunKerja, PengirimanMaterial
from liniProduksi.forms import ProsesGantiForm


def index(request):
    eo = EngineeringOrder.objects.all().order_by('-tanggalPengajuan')
    mat = Material.objects.all()
    context = {
        'Judul': 'Engineering Order',
        'eo': eo,
        'mat': mat,
    }
    return render(request, 'engineeringOrder/indexV2.html', context)

def newEO(request):
    eo_form = EOForm(request.POST or None)
    material_form = MaterialPenggantiForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        eo_form.id = request.POST.get('id')
        eo_form.material = request.POST.get('material')
        eo_form.idEO = request.POST.get('idEO')
        eo_form.namaPengusul = request.POST.get('namaPengusul')
        eo_form.departemenPengusul = request.POST.get('departemenPengusul')
        eo_form.keterangan = request.POST.get('keterangan')

        mt = Material.objects.get(id=eo_form.material)
        eo_form.tanggalPengajuan = datetime.datetime.now().date()
        EngineeringOrder.objects.create(id=eo_form.id,material=mt, idEO=eo_form.idEO, namaPengusul=eo_form.namaPengusul,
                                        departemenPengusul=eo_form.departemenPengusul, keterangan=eo_form.keterangan,
                                        tanggalPengajuan=eo_form.tanggalPengajuan)

        material_form.varian = request.POST.get('varian')
        get_varian = Varian.objects.get(idVarian=material_form.varian)
        material_form.id = request.POST.get('id')
        material_form.idMaterial = request.POST.get('idMaterial')
        material_form.namaMaterial = request.POST.get('namaMaterial')
        material_form.namaSupplier = request.POST.get('namaSupplier')
        material_form.penyusunProduk = request.POST.get('penyusunProduk')
        get_penyusunProduk = Material.objects.get(id = material_form.penyusunProduk)
        get_penggantiMaterial = Material.objects.get(id = eo_form.material)
        Material.objects.create(id=material_form.id, varian=get_varian, idMaterial=material_form.idMaterial,
                                namaMaterial=material_form.namaMaterial, namaSupplier=material_form.namaSupplier,
                                penyusunProduk=get_penyusunProduk, penggantiMaterial=get_penggantiMaterial,
                                is_berlaku = False)
        next = request.POST.get('next', '/')
        return redirect('engineeringOrder:index')

    context = {
        'JudulEO': 'Tambah Engineering Order',
        'JudulMat': 'Material Pengganti',
        'eo_form': eo_form,
        'material_form': material_form,
    }
    return render(request, 'engineeringOrder/newEO.html', context)

def deleteEO(request, delete_id):
    #cara delete
    EngineeringOrder.objects.filter(id=delete_id).delete()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

def setuju(request,setuju_id):
    eo_update = EngineeringOrder.objects.get(id=setuju_id)
    matEO = str(eo_update.material.id)
    mat = Material.objects.get(id=matEO)
    mat_pengganti = Material.objects.get(penggantiMaterial=matEO)

    mat_kebutuhan = KebutuhanMaterial.objects.get(material=matEO)

    eo_form = PersetujuanEOForm(request.POST or None, instance=eo_update)

    if request.method == 'POST':
        tanggalPerubahanBerlaku = request.POST.get('tanggalPerubahanBerlaku')
        tanggal = datetime.datetime.now().date()
        EngineeringOrder.objects.filter(id=setuju_id).update(is_disetujui=True,
                                                                tanggalPersetujuan=tanggal,
                                                                tanggalPerubahanBerlaku=tanggalPerubahanBerlaku)

        if eo_update.material.id == mat.id:
            Material.objects.filter(id=mat.id).update(is_berlaku=False,
                                                          tanggalGanti=tanggalPerubahanBerlaku,
                                                          keterangan=eo_update.keterangan)
            Material.objects.filter(id=mat_pengganti.id).update(is_berlaku=True,
                                                      tanggalMulaiBerlaku=tanggalPerubahanBerlaku,)

        return HttpResponseRedirect("prosesEO/{id}".format(id=eo_update.id))

    context = {
        'Judul': 'Persetujuan Engineering Order',
        'Judul_Proses': 'Proses Material Sebelum',
        'eo_form': eo_form,
        'mat': mat,
        'eo_update': eo_update,
        'mat_kebutuhan': mat_kebutuhan,
    }
    return render(request, 'engineeringOrder/setuju.html', context)

def tidakSetuju(request,tidakSetuju_id):
    tanggal = datetime.datetime.now().date()
    eo_update = EngineeringOrder.objects.get(id=tidakSetuju_id)
    matEO = str(eo_update.material.id)
    mat = Material.objects.get(id=matEO)
    mat_pengganti = Material.objects.get(penggantiMaterial=matEO)

    EngineeringOrder.objects.filter(id=tidakSetuju_id).update(is_disetujui=False, tanggalPersetujuan=tanggal)
    Material.objects.filter(id=mat_pengganti.id).update(is_berlaku = None)
    return redirect('engineeringOrder:tidakDisetujui')

def belumDisetujui(request):
    eo = EngineeringOrder.objects.filter(is_disetujui__isnull=True)
    mat = Material.objects.all()
    context = {
        'Judul': 'Engineering Order Belum Disetujui',
        'eo': eo,
        'mat': mat,
    }
    return render(request, 'engineeringOrder/belumDisetujuiV2.html', context)

def disetujui(request):
    eo = EngineeringOrder.objects.filter(is_disetujui=True)
    mat = Material.objects.all()
    mat_pengganti = Material.objects.filter(is_berlaku = False)
    mat_kebutuhan = KebutuhanMaterial.objects.all()
    context = {
        'Judul': 'Engineering Order Disetujui',
        'eo': eo,
        'mat': mat,
        'mat_kebutuhan': mat_kebutuhan,
    }
    return render(request, 'engineeringOrder/disetujuiV2.html', context)

def tidakDisetujui(request):
    eo = EngineeringOrder.objects.filter(is_disetujui=False)
    mat = Material.objects.all()

    context = {
        'Judul': 'Engineering Order Tidak Disetujui',
        'eo': eo,
        'mat': mat,
    }
    return render(request, 'engineeringOrder/tidakDisetujuiV2.html', context)

def prosesEO(request, setuju_id):
    eo = EngineeringOrder.objects.get(id=setuju_id)
    matEO = str(eo.material.id)
    mat = Material.objects.get(id=matEO)
    mat_kebutuhan = KebutuhanMaterial.objects.get(material=matEO)

    context = {
        'Judul': 'Proses Material Sebelum',
        'mat': mat,
        'mat_kebutuhan': mat_kebutuhan,
        'eo': eo,
    }
    return render(request, 'engineeringOrder/prosesEO.html', context)


def prosesLamaEO(request, setuju_id):
    eo_update = EngineeringOrder.objects.get(id=setuju_id)
    material_ganti_eo = eo_update.material

    material_pengganti = Material.objects.get(penggantiMaterial = material_ganti_eo)
    mid = str(material_pengganti.idMaterial)
    idmaterial = Material.objects.filter(idMaterial=mid).first()

    material_ganti_kebutuhan = KebutuhanMaterial.objects.get(material=material_ganti_eo)

    EngineeringOrder.objects.filter(id=setuju_id).update(is_prosesBaru=False)
    KebutuhanMaterial.objects.filter(id=material_ganti_kebutuhan.id).delete()
    KebutuhanMaterial.objects.create(stasiunKerja=material_ganti_kebutuhan.stasiunKerja, proses=material_ganti_kebutuhan.proses,
                                     material=material_pengganti)

    proses_sk = Proses.objects.get(idProses=str(material_ganti_kebutuhan.proses))
    p_sk = str(proses_sk.stasiunKerja)
    stasiunKerja = StasiunKerja.objects.get(idStasiunKerja=p_sk)
    material = KebutuhanMaterial.objects.filter(stasiunKerja=stasiunKerja).filter(material__idMaterial=idmaterial).first()
    km = material.jumlahMaterialPerCycleTime
    kumulatif = km + 1
    KebutuhanMaterial.objects.filter(material__idMaterial=idmaterial).update(jumlahMaterialPerCycleTime=kumulatif)
    return redirect('engineeringOrder:disetujui')

def prosesBerlakuEO(request, setuju_id):
    eo = EngineeringOrder.objects.get(id=setuju_id)
    matEO = str(eo.material.id)
    mat = Material.objects.get(id=matEO)
    mat_kebutuhan = KebutuhanMaterial.objects.get(material=matEO)

    context = {
        'Judul': 'Proses Material Sebelum',
        'mat': mat,
        'mat_kebutuhan': mat_kebutuhan,
        'eo': eo,
    }
    return render(request, 'engineeringOrder/prosesBerlakuEO.html', context)

def prosesLamaBerlakuEO(request,setuju_id):
    eo = EngineeringOrder.objects.get(id=setuju_id)
    matEO = str(eo.material.id)
    mat_kebutuhan = KebutuhanMaterial.objects.get(material=matEO)
    mat_kebutuhan_proses = str(mat_kebutuhan.proses.idProses)
    proses = Proses.objects.get(idProses=mat_kebutuhan_proses)

    Proses.objects.filter(idProses=proses).update(is_berlaku=True)
    return HttpResponseRedirect("prosesEO/prosesBaruEO/{id}".format(id=eo.id))

def prosesLamaTidakBerlakuEO(request,setuju_id):
    eo = EngineeringOrder.objects.get(id=setuju_id)
    matEO = str(eo.material.id)
    mat_kebutuhan = KebutuhanMaterial.objects.get(material=matEO)
    mat_kebutuhan_proses = str(mat_kebutuhan.proses.idProses)
    proses = Proses.objects.get(idProses=mat_kebutuhan_proses)

    Proses.objects.filter(idProses=proses).update(is_berlaku=False, tanggalSelesaiBerlaku=eo.tanggalPerubahanBerlaku)
    return HttpResponseRedirect("prosesEO/prosesBaruEO/{id}".format(id=eo.id))

def prosesBaruEO(request, setuju_id):
    eo_update = EngineeringOrder.objects.get(id=setuju_id)
    proses_form = ProsesGantiForm(request.POST or None, instance=eo_update)

    material_ganti_eo = eo_update.material
    material_pengganti = Material.objects.get(penggantiMaterial = material_ganti_eo)

    if request.method == 'POST':
        stasiunKerja = request.POST.get('stasiunKerja')
        sk_mt = StasiunKerja.objects.get(idStasiunKerja=stasiunKerja)
        idProses = request.POST.get('idProses')
        namaProses = request.POST.get('namaProses')
        durasiProses = request.POST.get('durasiProses')

        Proses.objects.create(stasiunKerja=sk_mt, idProses=idProses,namaProses=namaProses,
                              durasiProses=durasiProses, is_berlaku=True)

        pr_mt = Proses.objects.get(idProses=idProses)
        KebutuhanMaterial.objects.create(stasiunKerja=sk_mt, proses=pr_mt, material=material_pengganti)
        Proses.objects.filter(idProses=idProses).update(tanggalMulaiBerlaku = material_pengganti.tanggalMulaiBerlaku)
        EngineeringOrder.objects.filter(id=setuju_id).update(is_prosesBaru=True)

        mid = str(material_pengganti.idMaterial)
        idmaterial = Material.objects.filter(idMaterial=mid).first()
        material = KebutuhanMaterial.objects.filter(stasiunKerja=stasiunKerja).filter(
            material__idMaterial=idmaterial).first()
        km = material.jumlahMaterialPerCycleTime
        kumulatif = km + 1
        KebutuhanMaterial.objects.filter(material__idMaterial=idmaterial).update(jumlahMaterialPerCycleTime=kumulatif)

        return redirect('engineeringOrder:disetujui')

    context = {
        'Judul': 'Tambah Proses untuk Material Pengganti',
        'proses_form': proses_form,
    }
    return render(request, 'liniProduksi/newProses.html', context)