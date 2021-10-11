from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth
from django.db.models import Sum, F, IntegerField

from .models import ProduksiHarian, KebutuhanMaterial, WaktuIstirahat, LiniProduksi, TargetHarian, TargetMingguan, TargetBulanan, TargetTahunan
from .forms import ProduksiHarianForm, WaktuIstirahatForm, HariLiburForm, TargetHarianForm, TargetMingguanForm, TargetBulananForm, TargetTahunanForm
from produk.models import Varian
import datetime
import time
# Create your views here.

def produksiHarian(request):
    today = datetime.datetime.now()
    produksiHarian = ProduksiHarian.objects.filter(tanggalProduksi = today).order_by('-tanggalProduksi')
    istirahat = WaktuIstirahat.objects.all().order_by('waktuMulaiIstirahat')
    target = TargetHarian.objects.all()
    context = {
        'Judul': 'Produksi',
        'produksiHarian': produksiHarian,
        'istirahat': istirahat,
        'today': today,
        'target': target,
    }

    return render(request, 'liniProduksi/liniProduksi_harian.html', context)

def tambahCapaian(request, id):
    targetCapaian = TargetHarian.objects.get(id=id)
    TargetHarian.objects.filter(id=id).update(capaian = F('capaian')+1)
    var = Varian.objects.get(idVarian=targetCapaian.varian)
    kebutuhanMaterial = KebutuhanMaterial.objects.filter(material__varian=var)
    for o in kebutuhanMaterial:
        if o.jumlahMaterialKumulatif != 0:
            kumulatif = o.jumlahMaterialKumulatif - o.jumlahMaterialPerCycleTime
            KebutuhanMaterial.objects.filter(id=o.id).update(jumlahMaterialKumulatif = kumulatif)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def newProduksiHarian(request):
    #cara mencocokan antara input dengan data yang telah ada = PostForm(request.POST)
    stasiunkerja_form = ProduksiHarianForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        kondisiIstirahat = request.POST.get('kondisiIstirahat')
        if stasiunkerja_form.is_valid():
            # menyimpan ke database
            m = stasiunkerja_form.save()
            ph = ProduksiHarian.objects.get(id=m.id)
            if kondisiIstirahat == "Normal":
                istirahat = WaktuIstirahat.objects.filter(produksiHarian__isnull=True)
                t = 0
                for i in istirahat:
                    WaktuIstirahat.objects.create(produksiHarian=ph, waktuMulaiIstirahat=i.waktuMulaiIstirahat,
                                                  waktuSelesaiIstirahat=i.waktuSelesaiIstirahat, kondisi="Normal")
            #         durasi_istirahat = datetime.datetime.combine(datetime.date.today(), i.waktuSelesaiIstirahat) - datetime.datetime.combine(datetime.date.today(), i.waktuMulaiIstirahat)
            #         x = time.strptime('%s' % (durasi_istirahat), '%H:%M:%S')
            #         durasi_istirahat_second = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min,
            #                                                      seconds=x.tm_sec).total_seconds()
            #         t = t + durasi_istirahat_second
            #
            #     lp = LiniProduksi.objects.get(idLiniProduksi=ph.liniProduksi)
            #     waktu_detik = ((lp.jumlahStasiunKerja - 1) * lp.waktuSiklus)
            #     jam_selesai = waktu_detik // 3600
            #     menit_selesai = (waktu_detik % 3600) // 60
            #     detik_selesai = waktu_detik % 60
            #     timedelta_selesai = datetime.timedelta(hours=jam_selesai, minutes=menit_selesai,
            #                                            seconds=detik_selesai)
            #
            #     jam_istirahat = t // 3600
            #     menit_istirahat = (t % 3600) // 60
            #     detik_istirahat = t % 60
            #     timedelta_durasi_ist = datetime.timedelta(hours=jam_istirahat, minutes=menit_istirahat,seconds=detik_istirahat)
            #
            #     waktuIst = datetime.datetime.combine(datetime.date(1, 1, 1), ph.waktuSelesaiProduksiAktual)
            #     waktu = (waktuIst + timedelta_durasi_ist +  timedelta_selesai).time()
            #     ProduksiHarian.objects.filter(id=ph.id).update(waktuSelesaiProduksiAktual=waktu)

        return redirect('liniProduksi:harian')

    context = {
        'Judul': 'Tambah Produksi Harian',
        'css': 'liniProduksi/css/styles_form.css',
        'stasiunkerja_form': stasiunkerja_form,
    }
    return render(request,'liniProduksi/newStasiunKerja.html',context)

def deleteProduksiHarian(request, delete_id):
    #cara delete
    ProduksiHarian.objects.filter(id=delete_id).delete()
    return redirect('liniProduksi:produksiHarian')

def updateProduksiHarian(request, update_id):
    #cara edit
    produksiHarian_update = ProduksiHarian.objects.get(id=update_id)


    produksiHarian_form = ProduksiHarianForm(request.POST or None, instance=produksiHarian_update)

    if request.method == 'POST':
        #validasi data
        if produksiHarian_form.is_valid():
            #menyimpan ke database
            produksiHarian_form.save()
            return redirect('liniProduksi:produksiHarian')

    context = {
        'Judul': 'Update Target Produksi',
        'produksiHarian_form': produksiHarian_form,
    }

    return render(request,'liniProduksi/newLiniProduksi_harian.html',context)

def newWaktuIstirahat(request, produksiHarianInput):
    waktuIstirahat_form = WaktuIstirahatForm(request.POST or None)

    if request.method == 'POST':
        waktuMulaiIstirahat = request.POST.get('waktuMulaiIstirahat')
        waktuSelesaiIstirahat = request.POST.get('waktuSelesaiIstirahat')
        ph = ProduksiHarian.objects.get(id=produksiHarianInput)

        WaktuIstirahat.objects.create(produksiHarian=ph, waktuMulaiIstirahat=waktuMulaiIstirahat,
                                      waktuSelesaiIstirahat=waktuSelesaiIstirahat)

        return redirect('liniProduksi:produksiHarian')

    context = {
        'Judul': 'Tambah Waktu Istirahat Customize',
        'css': 'liniProduksi/css/styles_form.css',
        'waktuIstirahat_form': waktuIstirahat_form,
    }
    return render(request, 'liniProduksi/newWaktuIstirahat.html', context)

def newWaktuIstirahatNormal(request):
    waktuIstirahat_form = WaktuIstirahatForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        waktuMulaiIstirahat = request.POST.get('waktuMulaiIstirahat')
        waktuSelesaiIstirahat = request.POST.get('waktuSelesaiIstirahat')

        WaktuIstirahat.objects.create(waktuMulaiIstirahat=waktuMulaiIstirahat, waktuSelesaiIstirahat=waktuSelesaiIstirahat,
                                      kondisi = "Normal")
        return redirect('liniProduksi:harian')

    context = {
        'Judul': 'Tambah Waktu Istirahat Normal',
        'css': 'liniProduksi/css/styles_form.css',
        'waktuIstirahat_form': waktuIstirahat_form,
    }
    return render(request, 'liniProduksi/newWaktuIstirahat.html', context)

def deleteWaktuIstirahat(request, delete_id):
    #cara delete
    WaktuIstirahat.objects.filter(id=delete_id).delete()
    return redirect('liniProduksi:harian')

def updateWaktuIstirahat(request, update_id):
    #cara edit
    waktuIstirahat_update = WaktuIstirahat.objects.get(id=update_id)

    data = {
        'waktuMulaiIstirahat':waktuIstirahat_update.waktuMulaiIstirahat,
        'waktuSelesaiIstirahat':waktuIstirahat_update.waktuSelesaiIstirahat,
    }
    waktuIstirahat_form = WaktuIstirahatForm(request.POST or None, initial=data, instance=waktuIstirahat_update)

    if request.method == 'POST':
        #validasi data
        if waktuIstirahat_form.is_valid():
            #menyimpan ke database
            waktuIstirahat_form.save()
            return redirect('liniProduksi:harian')

    context = {
        'Judul': 'Update Waktu Istirahat',
        'waktuIstirahat_form': waktuIstirahat_form,
    }

    return render(request,'liniProduksi/newWaktuIstirahat.html',context)

def harian(request):
    produksiHarian = ProduksiHarian.objects.all().order_by('-tanggalProduksi')
    istirahat = WaktuIstirahat.objects.all().order_by('waktuMulaiIstirahat')
    target = TargetHarian.objects.all().order_by('waktuMulaiProduksi')
    today = datetime.datetime.now()
    context = {
        'Judul': 'Produksi',
        'produksiHarian': produksiHarian,
        'istirahat': istirahat,
        'today': today,
        'target':target,
    }

    return render(request, 'liniProduksi/produksi_harian.html', context)

def mingguan(request):
    targetMingguan = TargetMingguan.objects.all().order_by('-tahun','-minggu', 'varian')
    targetHarian = TargetHarian.objects.annotate(year=ExtractYear('tanggal')).annotate(week=ExtractWeek('tanggal')).values('year', 'week', 'varian').annotate(sum_capaian=Sum('capaian', output_field=IntegerField()), sum_target=Sum('target', output_field=IntegerField())).order_by('-year','-week')
    today = datetime.datetime.now().date()
    wk = today.isocalendar()[1]
    yr = today.isocalendar()[0]
    context = {
        'Judul': 'Produksi',
        'targetHarian': targetHarian,
        'targetMingguan': targetMingguan,
        'wk': wk,
        'yr': yr,
    }

    return render(request, 'liniProduksi/produksi_mingguan.html', context)

def bulanan(request):
    targetBulanan = TargetBulanan.objects.all().order_by('-tahun', '-bulan', 'varian')
    targetHarian = TargetHarian.objects.annotate(year=ExtractYear('tanggal')).annotate(
        month=ExtractMonth('tanggal')).values('year', 'month', 'varian').annotate(
        sum_capaian=Sum('capaian', output_field=IntegerField()),
        sum_target=Sum('target', output_field=IntegerField())).order_by('-year', '-month')
    today = datetime.datetime.now().date()
    mon = today.month
    yr = today.isocalendar()[0]
    context = {
        'Judul': 'Produksi',
        'targetHarian': targetHarian,
        'targetBulanan': targetBulanan,
        'mon':mon,
        'yr':yr,
    }

    return render(request, 'liniProduksi/produksi_bulanan.html', context)

def tahunan(request):
    targetTahunan = TargetTahunan.objects.all().order_by('-tahun', 'varian')
    targetHarian = TargetHarian.objects.annotate(year=ExtractYear('tanggal')).values('year','varian').annotate(
        sum_capaian=Sum('capaian', output_field=IntegerField()),
        sum_target=Sum('target', output_field=IntegerField())).order_by('-year',)
    today = datetime.datetime.now().date()
    yr = today.isocalendar()[0]
    context = {
        'Judul': 'Produksi',
        'targetHarian': targetHarian,
        'targetTahunan': targetTahunan,
        'yr': yr,
    }

    return render(request, 'liniProduksi/produksi_tahunan.html', context)

def hariLibur(request):
    # cara mencocokan antara input dengan data yang telah ada = PostForm(request.POST)
    hariLibur_form = HariLiburForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        liniProduksi = request.POST.get('liniProduksi')
        tanggalProduksi = request.POST.get('tanggalProduksi')
        alasanLibur = request.POST.get('alasanLibur')

        lp = LiniProduksi.objects.get(idLiniProduksi = liniProduksi)
        ProduksiHarian.objects.create(liniProduksi=lp, tanggalProduksi=tanggalProduksi,
                                      waktuMulaiProduksi = datetime.datetime.now().time(), waktuSelesaiProduksi = datetime.datetime.now().time(),
                                      is_libur="Libur", alasanLibur=alasanLibur)
        return redirect('liniProduksi:produksiHarian')

    context = {
        'Judul': 'Tambah Hari Libur',
        'css': 'liniProduksi/css/styles_form.css',
        'hariLibur_form': hariLibur_form,
    }
    return render(request, 'liniProduksi/newHariLibur.html', context)

def newTargetHarian(request, produksiHarianInput):
    stasiunkerja_form = TargetHarianForm(request.POST or None)

    if request.method == 'POST':
        if stasiunkerja_form.is_valid():
            ph = stasiunkerja_form.save()

            p = ProduksiHarian.objects.get(id=produksiHarianInput)
            TargetHarian.objects.filter(id=ph.id).update(produksiHarian=p, tanggal=p.tanggalProduksi)
            lp = LiniProduksi.objects.get(idLiniProduksi=p.liniProduksi)

            targetBaru = TargetHarian.objects.get(id=ph.id)
            waktu = (targetBaru.target * lp.waktuSiklus) + ((lp.jumlahStasiunKerja - 1) * lp.waktuSiklus)
            jam = waktu // 3600
            menit = (waktu % 3600) // 60
            detik = waktu % 60
            timedelta = datetime.timedelta(hours=jam, minutes=menit, seconds=detik)
            waktuMulai = datetime.datetime.combine(datetime.date(1, 1, 1), targetBaru.waktuMulaiProduksiAktual)
            waktuSelesaiVarian = (waktuMulai + timedelta).time()

            waktuIstirahat = WaktuIstirahat.objects.filter(produksiHarian=produksiHarianInput, waktuMulaiIstirahat__gte=targetBaru.waktuMulaiProduksi).order_by('waktuMulaiIstirahat')
            jumlahIstirahat = WaktuIstirahat.objects.filter(produksiHarian=produksiHarianInput, waktuMulaiIstirahat__gte=targetBaru.waktuMulaiProduksi).count()

            if jumlahIstirahat == 0:
                TargetHarian.objects.filter(id=targetBaru.id).update(waktuSelesaiProduksiAktual=waktuSelesaiVarian)

            elif waktuSelesaiVarian < waktuIstirahat[0].waktuMulaiIstirahat:
                TargetHarian.objects.filter(id=targetBaru.id).update(waktuSelesaiProduksiAktual=waktuSelesaiVarian)

            j = 0
            waktuIstirahatKumulatif = 0
            while j < jumlahIstirahat-1:
                # durasi kumulatif istirahat
                t_awalIst = waktuIstirahat[j].waktuMulaiIstirahat
                t_awIst = str(t_awalIst)
                t_akhirIst = waktuIstirahat[j].waktuSelesaiIstirahat
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
                wsv = datetime.datetime.combine(datetime.date(1, 1, 1), waktuSelesaiVarian)
                wsv_ist = (wsv + timedelta_durasi_ist).time()
                if (wsv_ist >= waktuIstirahat[j].waktuMulaiIstirahat) and (wsv_ist < waktuIstirahat[j+1].waktuMulaiIstirahat):
                    #jadwal + istirahat
                    TargetHarian.objects.filter(id=targetBaru.id).update(waktuSelesaiProduksiAktual=wsv_ist)
                    break
                else:
                    j += 1

            if jumlahIstirahat != 0:
                if waktuSelesaiVarian >= waktuIstirahat[jumlahIstirahat-1].waktuMulaiIstirahat:
                    k = 0
                    waktuIstirahatKum = 0
                    while k < jumlahIstirahat:
                        t_awalIst = waktuIstirahat[k].waktuMulaiIstirahat
                        t_awIst = str(t_awalIst)
                        t_akhirIst = waktuIstirahat[k].waktuSelesaiIstirahat
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
                    wsv = datetime.datetime.combine(datetime.date(1, 1, 1), waktuSelesaiVarian)
                    wsv_ist = (wsv + timedelta_durasi_ist).time()
                    TargetHarian.objects.filter(id=targetBaru.id).update(waktuSelesaiProduksiAktual=wsv_ist)

            th = TargetHarian.objects.get(id=targetBaru.id)

            if p.waktuMulaiProduksiAktual == None:
                ProduksiHarian.objects.filter(id=produksiHarianInput).update(waktuMulaiProduksiAktual = th.waktuMulaiProduksiAktual,
                                                                             waktuSelesaiProduksiAktual = th.waktuSelesaiProduksiAktual,waktuMulaiProduksi = th.waktuMulaiProduksi,waktuSelesaiProduksi = th.waktuSelesaiProduksi)

            if p.waktuMulaiProduksi != None:
                if th.waktuMulaiProduksi < p.waktuMulaiProduksi:
                    ProduksiHarian.objects.filter(id=produksiHarianInput).update(waktuMulaiProduksi=th.waktuMulaiProduksi)

                if th.waktuSelesaiProduksi > p.waktuSelesaiProduksi:
                    ProduksiHarian.objects.filter(id=produksiHarianInput).update(waktuSelesaiProduksi=th.waktuSelesaiProduksi)

                if th.waktuMulaiProduksiAktual < p.waktuMulaiProduksiAktual:
                    ProduksiHarian.objects.filter(id=produksiHarianInput).update(waktuMulaiProduksiAktual=th.waktuMulaiProduksiAktual)

                if th.waktuSelesaiProduksiAktual > p.waktuSelesaiProduksiAktual:
                    ProduksiHarian.objects.filter(id=produksiHarianInput).update(waktuSelesaiProduksiAktual=th.waktuSelesaiProduksiAktual)
            return redirect('liniProduksi:harian')

    context = {
        'Judul': 'Tambah Target Harian',
        'css': 'liniProduksi/css/styles_form.css',
        'stasiunkerja_form': stasiunkerja_form,
    }
    return render(request, 'liniProduksi/newStasiunKerja.html', context)

def deleteTargetHarian(request, delete_id):
    #cara delete
    TargetHarian.objects.filter(id=delete_id).delete()
    return redirect('liniProduksi:harian')

def updateTargetHarian(request, update_id):
    #cara edit
    target_update = TargetHarian.objects.get(id=update_id)

    stasiunkerja_form = TargetHarianForm(request.POST or None, instance=target_update)

    if request.method == 'POST':
        if stasiunkerja_form.is_valid():
            ph = stasiunkerja_form.save()

            p = ProduksiHarian.objects.get(id=str(ph.produksiHarian))
            TargetHarian.objects.filter(id=ph.id).update(produksiHarian=p, tanggal=p.tanggalProduksi)
            lp = LiniProduksi.objects.get(idLiniProduksi=p.liniProduksi)
            waktu = (ph.target * lp.waktuSiklus) + ((lp.jumlahStasiunKerja - 1) * lp.waktuSiklus)
            jam = waktu // 3600
            menit = (waktu % 3600) // 60
            detik = waktu % 60
            timedelta = datetime.timedelta(hours=jam, minutes=menit,
                                           seconds=detik)

            waktuMulai = datetime.datetime.combine(datetime.date(1, 1, 1), ph.waktuSelesaiProduksiAktual)
            waktuSelesaiVarian = (waktuMulai + timedelta).time()

            waktuIstirahat = WaktuIstirahat.objects.filter(produksiHarian=str(ph.produksiHarian),
                                                           waktuMulaiIstirahat__gte=ph.waktuMulaiProduksi).order_by(
                'waktuMulaiIstirahat')
            jumlahIstirahat = WaktuIstirahat.objects.filter(produksiHarian=str(ph.produksiHarian),
                                                            waktuMulaiIstirahat__gte=ph.waktuMulaiProduksi).count()

            if jumlahIstirahat == 0:
                TargetHarian.objects.filter(id=ph.id).update(waktuSelesaiProduksiAktual=waktuSelesaiVarian)

            elif waktuSelesaiVarian < waktuIstirahat[0].waktuMulaiIstirahat:
                TargetHarian.objects.filter(id=ph.id).update(waktuSelesaiProduksiAktual=waktuSelesaiVarian)

            j = 0
            waktuIstirahatKumulatif = 0
            while j < jumlahIstirahat - 1:
                # durasi kumulatif istirahat
                t_awalIst = waktuIstirahat[j].waktuMulaiIstirahat
                t_awIst = str(t_awalIst)
                t_akhirIst = waktuIstirahat[j].waktuSelesaiIstirahat
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
                wsv = datetime.datetime.combine(datetime.date(1, 1, 1), waktuSelesaiVarian)
                wsv_ist = (wsv + timedelta_durasi_ist).time()
                if (wsv_ist >= waktuIstirahat[j].waktuMulaiIstirahat) and (
                        wsv_ist < waktuIstirahat[j + 1].waktuMulaiIstirahat):
                    # jadwal + istirahat
                    TargetHarian.objects.filter(id=ph.id).update(waktuSelesaiProduksiAktual=wsv_ist)
                    break
                else:
                    j += 1

            if jumlahIstirahat != 0:
                if waktuSelesaiVarian >= waktuIstirahat[jumlahIstirahat - 1].waktuMulaiIstirahat:
                    k = 0
                    waktuIstirahatKum = 0
                    while k < jumlahIstirahat:
                        t_awalIst = waktuIstirahat[k].waktuMulaiIstirahat
                        t_awIst = str(t_awalIst)
                        t_akhirIst = waktuIstirahat[k].waktuSelesaiIstirahat
                        t_akIst = str(t_akhirIst)
                        FMT = '%H:%M:%S'
                        durasi_istirahat = datetime.datetime.strptime(t_akIst, FMT) - datetime.datetime.strptime(
                            t_awIst,
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
                    wsv = datetime.datetime.combine(datetime.date(1, 1, 1), waktuSelesaiVarian)
                    wsv_ist = (wsv + timedelta_durasi_ist).time()
                    TargetHarian.objects.filter(id=ph.id).update(waktuSelesaiProduksiAktual=wsv_ist)

            th = TargetHarian.objects.get(id=ph.id)

            if p.waktuMulaiProduksiAktual == None:
                ProduksiHarian.objects.filter(id=str(ph.produksiHarian)).update(
                    waktuMulaiProduksiAktual=th.waktuMulaiProduksiAktual,
                    waktuSelesaiProduksiAktual=th.waktuSelesaiProduksiAktual, waktuMulaiProduksi=th.waktuMulaiProduksi,
                    waktuSelesaiProduksi=th.waktuSelesaiProduksi)

            if p.waktuMulaiProduksi != None:
                if th.waktuMulaiProduksi < p.waktuMulaiProduksi:
                    ProduksiHarian.objects.filter(id=str(ph.produksiHarian)).update(
                        waktuMulaiProduksi=th.waktuMulaiProduksi)

                if th.waktuSelesaiProduksi > p.waktuSelesaiProduksi:
                    ProduksiHarian.objects.filter(id=str(ph.produksiHarian)).update(
                        waktuSelesaiProduksi=th.waktuSelesaiProduksi)

                if th.waktuMulaiProduksiAktual < p.waktuMulaiProduksiAktual:
                    ProduksiHarian.objects.filter(id=str(ph.produksiHarian)).update(
                        waktuMulaiProduksiAktual=th.waktuMulaiProduksiAktual)

                if th.waktuSelesaiProduksiAktual > p.waktuSelesaiProduksiAktual:
                    ProduksiHarian.objects.filter(id=str(ph.produksiHarian)).update(
                        waktuSelesaiProduksiAktual=th.waktuSelesaiProduksiAktual)
            return redirect('liniProduksi:harian')

    context = {
        'Judul': 'Update Target Harian',
        'stasiunkerja_form': stasiunkerja_form,
    }

    return render(request,'liniProduksi/newStasiunKerja.html',context)

def newTargetMingguan(request):
    stasiunkerja_form = TargetMingguanForm(request.POST or None)

    if request.method == 'POST':
        varian = request.POST.get('varian')
        liniProduksi = request.POST.get('liniProduksi')
        target = request.POST.get('target')
        minggu = request.POST.get('minggu')
        v = Varian.objects.get(idVarian=varian)
        lp = LiniProduksi.objects.get(idLiniProduksi=liniProduksi)
        mg = datetime.datetime.strptime(minggu, "%Y-%m-%d").date()
        wk = mg.isocalendar()[1]
        yr = mg.isocalendar()[0]
        TargetMingguan.objects.create(varian=v, liniProduksi=lp, target=target, minggu = wk, tahun = yr)
        return redirect('liniProduksi:mingguan')

    context = {
        'Judul': 'Tambah Target Mingguan',
        'css': 'liniProduksi/css/styles_form.css',
        'stasiunkerja_form': stasiunkerja_form,
    }
    return render(request, 'liniProduksi/newStasiunKerja.html', context)

def deleteTargetMingguan(request, delete_id):
    #cara delete
    TargetMingguan.objects.filter(id=delete_id).delete()
    return redirect('liniProduksi:mingguan')

def updateTargetMingguan(request, update_id):
    #cara edit
    target_update = TargetMingguan.objects.get(id=update_id)

    stasiunkerja_form = TargetMingguanForm(request.POST or None, instance=target_update)

    if request.method == 'POST':
        varian = request.POST.get('varian')
        liniProduksi = request.POST.get('liniProduksi')
        target = request.POST.get('target')
        minggu = request.POST.get('minggu')
        v = Varian.objects.get(idVarian=varian)
        lp = LiniProduksi.objects.get(idLiniProduksi=liniProduksi)
        mg = datetime.datetime.strptime(minggu, "%Y-%m-%d").date()
        wk = mg.isocalendar()[1]
        yr = mg.isocalendar()[0]
        TargetMingguan.objects.filter(id = update_id).update(varian=v, liniProduksi=lp, target=target, minggu=wk, tahun=yr)
        return redirect('liniProduksi:mingguan')

    context = {
        'Judul': 'Update Target Mingguan',
        'stasiunkerja_form': stasiunkerja_form,
    }

    return render(request,'liniProduksi/newStasiunKerja.html',context)

def newTargetBulanan(request):
    stasiunkerja_form = TargetBulananForm(request.POST or None)

    if request.method == 'POST':
        varian = request.POST.get('varian')
        liniProduksi = request.POST.get('liniProduksi')
        target = request.POST.get('target')
        bulan = request.POST.get('bulan')
        v = Varian.objects.get(idVarian=varian)
        lp = LiniProduksi.objects.get(idLiniProduksi=liniProduksi)
        mg = datetime.datetime.strptime(bulan, "%Y-%m-%d").date()
        mon = mg.month
        yr = mg.isocalendar()[0]
        TargetBulanan.objects.create(varian=v, liniProduksi=lp, target=target, bulan = mon, tahun = yr)
        return redirect('liniProduksi:bulanan')

    context = {
        'Judul': 'Tambah Target Bulanan',
        'css': 'liniProduksi/css/styles_form.css',
        'stasiunkerja_form': stasiunkerja_form,
    }
    return render(request, 'liniProduksi/newStasiunKerja.html', context)

def deleteTargetBulanan(request, delete_id):
    #cara delete
    TargetBulanan.objects.filter(id=delete_id).delete()
    return redirect('liniProduksi:bulanan')

def updateTargetBulanan(request, update_id):
    #cara edit
    target_update = TargetBulanan.objects.get(id=update_id)

    stasiunkerja_form = TargetBulananForm(request.POST or None, instance=target_update)

    if request.method == 'POST':
        varian = request.POST.get('varian')
        liniProduksi = request.POST.get('liniProduksi')
        target = request.POST.get('target')
        bulan = request.POST.get('bulan')
        v = Varian.objects.get(idVarian=varian)
        lp = LiniProduksi.objects.get(idLiniProduksi=liniProduksi)
        mg = datetime.datetime.strptime(bulan, "%Y-%m-%d").date()
        mon = mg.month
        yr = mg.isocalendar()[0]
        TargetBulanan.objects.filter(id=update_id).update(varian=v, liniProduksi=lp, target=target, bulan=mon, tahun=yr)
        return redirect('liniProduksi:bulanan')

    context = {
        'Judul': 'Update Target Bulanan',
        'stasiunkerja_form': stasiunkerja_form,
    }

    return render(request,'liniProduksi/newStasiunKerja.html',context)

def newTargetTahunan(request):
    stasiunkerja_form = TargetTahunanForm(request.POST or None)

    if request.method == 'POST':
        varian = request.POST.get('varian')
        liniProduksi = request.POST.get('liniProduksi')
        target = request.POST.get('target')
        tahun = request.POST.get('tahun')
        v = Varian.objects.get(idVarian=varian)
        lp = LiniProduksi.objects.get(idLiniProduksi=liniProduksi)
        mg = datetime.datetime.strptime(tahun, "%Y-%m-%d").date()
        yr = mg.isocalendar()[0]
        TargetTahunan.objects.create(varian=v, liniProduksi=lp, target=target, tahun = yr)
        return redirect('liniProduksi:tahunan')

    context = {
        'Judul': 'Tambah Target Tahunan',
        'css': 'liniProduksi/css/styles_form.css',
        'stasiunkerja_form': stasiunkerja_form,
    }
    return render(request, 'liniProduksi/newStasiunKerja.html', context)

def deleteTargetTahunan(request, delete_id):
    #cara delete
    TargetTahunan.objects.filter(id=delete_id).delete()
    return redirect('liniProduksi:tahunan')

def updateTargetTahunan(request, update_id):
    #cara edit
    target_update = TargetTahunan.objects.get(id=update_id)

    stasiunkerja_form = TargetTahunanForm(request.POST or None, instance=target_update)

    if request.method == 'POST':
        varian = request.POST.get('varian')
        liniProduksi = request.POST.get('liniProduksi')
        target = request.POST.get('target')
        tahun = request.POST.get('tahun')
        v = Varian.objects.get(idVarian=varian)
        lp = LiniProduksi.objects.get(idLiniProduksi=liniProduksi)
        mg = datetime.datetime.strptime(tahun, "%Y-%m-%d").date()
        yr = mg.isocalendar()[0]
        TargetTahunan.objects.filter(id=update_id).update(varian=v, liniProduksi=lp, target=target, tahun=yr)
        return redirect('liniProduksi:tahunan')

    context = {
        'Judul': 'Update Target Tahunan',
        'stasiunkerja_form': stasiunkerja_form,
    }

    return render(request,'liniProduksi/newStasiunKerja.html',context)