from django.shortcuts import render, redirect

from .models import JadwalLiniProduksi
from produk.models import Material
from liniProduksi.models import LiniProduksi, StasiunKerja, KebutuhanMaterial, ProduksiHarian, PengirimanMaterial, WaktuIstirahat, TargetHarian, Material
from produk.models import Varian
import datetime
import time
import math
from django.utils import timezone
from django.db.models import F
# Create your views here.

def index(request):
        jadwal = JadwalLiniProduksi.objects.all()
        sk = StasiunKerja.objects.all()
        context = {
            'Judul': 'Jadwal Kedatangan Material',
            'jadwal': jadwal,
            'sk': sk,
        }
        return render(request,'jadwal/index.html',context)

def index_SK (request, idStasiunKerjaInput):
    jadwal = JadwalLiniProduksi.objects.filter(kebutuhanMaterial__stasiunKerja = idStasiunKerjaInput)
    sk = StasiunKerja.objects.all()
    context = {
        'Judul': 'Jadwal Kedatangan Material',
        'jadwal': jadwal,
        'sk': sk,
    }
    return render(request, 'jadwal/index.html', context)

def newKonfirmasi(request, konfirmasi_id):
    jadwal_konfirmasi = JadwalLiniProduksi.objects.get(id=konfirmasi_id)
    JadwalLiniProduksi.objects.filter(id=konfirmasi_id).update(is_konfirmasi = True, jadwalKedatangan_aktual = datetime.datetime.now().time())
    matButuh = KebutuhanMaterial.objects.get(id=str(jadwal_konfirmasi.kebutuhanMaterial))
    mat = Material.objects.filter(id=str(matButuh.material_id)).first()
    var = Varian.objects.get(idVarian = str(mat.varian))
    KebutuhanMaterial.objects.filter(material__varian = var, material__idMaterial = mat, stasiunKerja = str(matButuh.stasiunKerja)).update(jumlahMaterialKumulatif=F('jumlahMaterialKumulatif')+jadwal_konfirmasi.jumlah_material)
    return redirect('jadwal:sudahKonfirmasi')

def sudahKonfirmasi(request):
    jadwalKonfirmasi = JadwalLiniProduksi.objects.filter(is_konfirmasi=True)
    sk = StasiunKerja.objects.all()

    context = {
        'Judul': 'Jadwal Sudah Konfirmasi',
        'jadwalKonfirmasi' : jadwalKonfirmasi,
        'sk': sk,
    }
    return render(request, 'jadwal/sudahKonfirmasi.html', context)

def sudahKonfirmasi_SK(request, idStasiunKerjaInput):
    jadwalKonfirmasi = JadwalLiniProduksi.objects.filter(is_konfirmasi=True).filter(kebutuhanMaterial__stasiunKerja = idStasiunKerjaInput)
    sk = StasiunKerja.objects.all()

    context = {
        'Judul': 'Jadwal Sudah Konfirmasi',
        'jadwalKonfirmasi' : jadwalKonfirmasi,
        'sk': sk,
    }
    return render(request, 'jadwal/sudahKonfirmasi.html', context)

def belumKonfirmasi(request):
    jadwal_Konfirmasi = JadwalLiniProduksi.objects.filter(is_konfirmasi=False)
    sk = StasiunKerja.objects.all()

    context = {
        'Judul': 'Jadwal Belum Konfirmasi',
        'jadwal_Konfirmasi': jadwal_Konfirmasi,
        'sk': sk,
    }
    return render(request, 'jadwal/belumKonfirmasi.html', context)

def belumKonfirmasi_SK(request, idStasiunKerjaInput):
    jadwal_Konfirmasi = JadwalLiniProduksi.objects.filter(is_konfirmasi=False).filter(kebutuhanMaterial__stasiunKerja = idStasiunKerjaInput)
    sk = StasiunKerja.objects.all()

    context = {
        'Judul': 'Jadwal Belum Konfirmasi',
        'jadwal_Konfirmasi': jadwal_Konfirmasi,
        'sk': sk,
    }
    return render(request, 'jadwal/belumKonfirmasi.html', context)


def permintaanMaterial(request, pm_id):
    jadwal_jumlahPengiriman = PengirimanMaterial.objects.get(id=pm_id)
    jadwal_material = KebutuhanMaterial.objects.get(id=str(jadwal_jumlahPengiriman.kebutuhanMaterial))
    jadwal_mt = Material.objects.get(id=str(jadwal_material.material_id))
    jadwal_varian = Varian.objects.get(idVarian=str(jadwal_mt.varian))

    sk_m = str(jadwal_material.stasiunKerja)
    jadwal_stasiunKerja = StasiunKerja.objects.get(idStasiunKerja=sk_m)

    sk_lp = str(jadwal_stasiunKerja.liniProduksi)
    jadwal_liniProduksi = LiniProduksi.objects.get(idLiniProduksi=sk_lp)

    lp_id = str(jadwal_liniProduksi.idLiniProduksi)
    jadwal_produksiHarian = ProduksiHarian.objects.get(liniProduksi__idLiniProduksi=lp_id, tanggalProduksi=datetime.datetime.now().date())
    jadwal_target = TargetHarian.objects.get(produksiHarian=jadwal_produksiHarian, varian=jadwal_varian, tanggal=datetime.datetime.now().date())
    jadwal_waktuIstirahat = WaktuIstirahat.objects.filter(produksiHarian=jadwal_produksiHarian, waktuMulaiIstirahat__gte=jadwal_target.waktuMulaiProduksiAktual).order_by('waktuMulaiIstirahat')

    jadwal = JadwalLiniProduksi.objects.filter(tanggal=datetime.datetime.now().date(),
                                      kebutuhanMaterial=str(jadwal_material.id)).count()
    if jadwal != 0:
        return redirect('jadwal:jadwalTersedia')
    else:
        pass

        # durasi dan waktu mulai produksi tiap stasiun kerja
    waktuTambahan_sk = (jadwal_stasiunKerja.nomorStasiunKerja - 1) * jadwal_liniProduksi.waktuSiklus
    jam_waktuTambahan_sk = waktuTambahan_sk // 3600
    menit_waktuTambahan_sk = (waktuTambahan_sk % 3600) // 60
    detik_waktuTambahan_sk = waktuTambahan_sk % 60

        # durasi_sk = durasi_produksi_second - waktuTambahan_sk
    t_awal = jadwal_target.waktuMulaiProduksiAktual
    timedelta_durasi = datetime.timedelta(hours=jam_waktuTambahan_sk, minutes=menit_waktuTambahan_sk,
                                              seconds=detik_waktuTambahan_sk)
    waktuMulai_sk_combine = datetime.datetime.combine(datetime.date(1, 1, 1), t_awal)
    waktuMulai_sk = (waktuMulai_sk_combine + timedelta_durasi).time()

        #jumlah material yang dibutuhkan berdasarkan target produksi dan material yang tersedia
    jumlah_material = int((jadwal_target.target * jadwal_material.jumlahMaterialPerCycleTime))-int(jadwal_material.jumlahMaterialKumulatif)

        # material tiap pengiriman habis setelah berapa cycle time dan seconds
    ct_material_habis = int(jadwal_jumlahPengiriman.jumlahMaterialTiapPengiriman / jadwal_material.jumlahMaterialPerCycleTime)
    second_material_habis = ct_material_habis * (jadwal_liniProduksi.waktuSiklus)

        #jumlah pengiriman
    jumlah_pengiriman = math.ceil(jumlah_material/int(jadwal_jumlahPengiriman.jumlahMaterialTiapPengiriman))

        #jadwal kedatangan material yang pertama
    t = int((int(jadwal_material.jumlahMaterialKumulatif) // jadwal_material.jumlahMaterialPerCycleTime)*jadwal_liniProduksi.waktuSiklus)
    jam = t // 3600
    menit = (t % 3600) // 60
    detik = t % 60
    timedelta_pengiriman = datetime.timedelta(hours=jam, minutes=menit, seconds=detik)
    waktu_pengiriman_combine = datetime.datetime.combine(datetime.date(1, 1, 1), waktuMulai_sk)
    waktu_pengiriman_pertama = (waktu_pengiriman_combine + timedelta_pengiriman).time()

        #jumlah istirahat
    jumlahIstirahat = WaktuIstirahat.objects.filter(produksiHarian=str(jadwal_produksiHarian.id), waktuMulaiIstirahat__gte=jadwal_target.waktuMulaiProduksi).count()

        # pembuatan jadwal
    JadwalLiniProduksi.objects.create(
                              kebutuhanMaterial=jadwal_material, tanggal=datetime.datetime.now().date(), jadwalKedatangan=waktu_pengiriman_pertama,
                              jumlah_material=jadwal_jumlahPengiriman.jumlahMaterialTiapPengiriman,)
    t = 0
    i = 0
    while i < jumlah_pengiriman-1:
            #waktu pengiriman
        t = t + second_material_habis
        jam = t // 3600
        menit = (t % 3600) // 60
        detik = t % 60
        timedelta_pengiriman = datetime.timedelta(hours=jam, minutes=menit, seconds=detik)
        waktu_pengiriman_combine = datetime.datetime.combine(datetime.date(1, 1, 1), waktu_pengiriman_pertama)
        waktu_pengiriman = (waktu_pengiriman_combine + timedelta_pengiriman).time()

        if waktu_pengiriman < jadwal_waktuIstirahat[0].waktuMulaiIstirahat:
            JadwalLiniProduksi.objects.create(
                                      kebutuhanMaterial=jadwal_material, tanggal=datetime.datetime.now().date(), jadwalKedatangan=waktu_pengiriman,
                                      jumlah_material=jadwal_jumlahPengiriman.jumlahMaterialTiapPengiriman,)

        j = 0
        waktuIstirahatKumulatif = 0
        while j < jumlahIstirahat-1:
                # durasi kumulatif istirahat
            t_awalIst = jadwal_waktuIstirahat[j].waktuMulaiIstirahat
            t_awIst = str(t_awalIst)
            t_akhirIst = jadwal_waktuIstirahat[j].waktuSelesaiIstirahat
            t_akIst = str(t_akhirIst)
            FMT = '%H:%M:%S'
            durasi_istirahat = datetime.datetime.strptime(t_akIst, FMT) - datetime.datetime.strptime(t_awIst,
                                                                                                         FMT)
            x = time.strptime('%s' % (durasi_istirahat), '%H:%M:%S')
            durasi_istirahat_second = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min,
                                                            seconds=x.tm_sec).total_seconds()

            waktuIstirahatKumulatif = waktuIstirahatKumulatif + durasi_istirahat_second

            jam_istirahat = waktuIstirahatKumulatif // 3600
            menit_istirahat = (waktuIstirahatKumulatif % 3600) // 60
            detik_istirahat = waktuIstirahatKumulatif % 60
            timedelta_durasi_ist = datetime.timedelta(hours=jam_istirahat, minutes=menit_istirahat,
                                                          seconds=detik_istirahat)
            waktuKirim = datetime.datetime.combine(datetime.date(1, 1, 1), waktu_pengiriman)
            waktuKirim_ist = (waktuKirim + timedelta_durasi_ist).time()
            if (waktuKirim_ist >= jadwal_waktuIstirahat[j].waktuSelesaiIstirahat) and (waktuKirim_ist <= jadwal_waktuIstirahat[j+1].waktuMulaiIstirahat):
                    #jadwal + istirahat
                JadwalLiniProduksi.objects.create(
                                                      kebutuhanMaterial=jadwal_material, tanggal=datetime.datetime.now().date(),
                                                      jadwalKedatangan=waktuKirim_ist,
                                                      jumlah_material=jadwal_jumlahPengiriman.jumlahMaterialTiapPengiriman,)
                break
            else:
                j += 1

        if waktu_pengiriman >= jadwal_waktuIstirahat[jumlahIstirahat-1].waktuMulaiIstirahat:
            k = 0
            waktuIstirahatKum = 0
            while k < jumlahIstirahat:
                t_awalIst = jadwal_waktuIstirahat[k].waktuMulaiIstirahat
                t_awIst = str(t_awalIst)
                t_akhirIst = jadwal_waktuIstirahat[k].waktuSelesaiIstirahat
                t_akIst = str(t_akhirIst)
                FMT = '%H:%M:%S'
                durasi_istirahat = datetime.datetime.strptime(t_akIst, FMT) - datetime.datetime.strptime(t_awIst,
                                                                                                             FMT)
                x = time.strptime('%s' % (durasi_istirahat), '%H:%M:%S')
                durasi_istirahat_sec = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min,
                                                                 seconds=x.tm_sec).total_seconds()

                waktuIstirahatKum = waktuIstirahatKum + durasi_istirahat_sec
                k += 1

            jam_istirahat = waktuIstirahatKum // 3600
            menit_istirahat = (waktuIstirahatKum % 3600) // 60
            detik_istirahat = waktuIstirahatKum % 60
            timedelta_durasi_ist = datetime.timedelta(hours=jam_istirahat, minutes=menit_istirahat,
                                                          seconds=detik_istirahat)
            waktuKirim = datetime.datetime.combine(datetime.date(1, 1, 1), waktu_pengiriman)
            waktuKirim_ist = (waktuKirim + timedelta_durasi_ist).time()
            JadwalLiniProduksi.objects.create(
                                                  kebutuhanMaterial=jadwal_material, tanggal=datetime.datetime.now().date(),
                                                  jadwalKedatangan=waktuKirim_ist,
                                                  jumlah_material=jadwal_jumlahPengiriman.jumlahMaterialTiapPengiriman,)

        i += 1

    return redirect('jadwal:index')

def jadwalTersedia(request):
    context = {
        'Judul': 'Jadwal Sudah Tersedia',
    }
    return render(request, 'jadwal/jadwalTersedia.html', context)