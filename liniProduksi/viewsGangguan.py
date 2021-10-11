from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import Gangguan, StasiunKerja, LiniProduksi, ProduksiHarian, TargetHarian, WaktuIstirahat
from .forms import GangguanForm
from jadwal.models import JadwalLiniProduksi
import datetime, time
from django.db.models import Q,F


def gangguan(request):
    stasiunKerja = StasiunKerja.objects.all()
    liniProduksi = LiniProduksi.objects.all()

    context = {
        'Judul': 'Gangguan',
        'stasiunKerja': stasiunKerja,
        'liniProduksi': liniProduksi,
    }
    return render(request, 'liniProduksi/gangguan.html', context)

def gangguan_semua(request):
    gangguan = Gangguan.objects.all().order_by('-tanggalGangguan', '-waktuMulaiGangguan')
    gangguan_selesai = Gangguan.objects.filter(status = "Gangguan selesai").order_by('-waktuMulaiGangguan', 'tanggalGangguan').order_by('-tanggalGangguan', '-waktuMulaiGangguan')
    gangguan_belumSelesai = Gangguan.objects.filter(Q(status = "Indikasi masalah") | Q(status="Lini produksi terhenti")).order_by('-tanggalGangguan', '-waktuMulaiGangguan')

    context = {
        'Judul': 'Gangguan',
        'gangguan': gangguan,
        'gangguan_selesai': gangguan_selesai,
        'gangguan_belumSelesai': gangguan_belumSelesai,
    }
    return render(request, 'liniProduksi/gangguanSemua_index.html', context)

def gangguanStasiunKerja(request, idStasiunKerjaInput):
    stasiunKerja = StasiunKerja.objects.filter(idStasiunKerja=idStasiunKerjaInput)
    gangguan = Gangguan.objects.filter(stasiunKerja__idStasiunKerja=idStasiunKerjaInput).order_by('-tanggalGangguan', '-waktuMulaiGangguan')

    context = {
        'Judul': 'Gangguan',
        'stasiunKerja': stasiunKerja,
        'gangguan': gangguan,
    }
    return render(request, 'liniProduksi/gangguanStasiunKerja_index.html', context)

def indikasiMasalah(request,idStasiunKerjaInput):
    stasiunKerja = StasiunKerja.objects.get(idStasiunKerja=idStasiunKerjaInput)
    waktuMulaiGangguan = datetime.datetime.now().time().replace(microsecond=0)
    tanggalGangguan = datetime.datetime.now()
    gangguan = Gangguan.objects.create(stasiunKerja=stasiunKerja, status="Indikasi masalah",
                                       waktuMulaiGangguan=waktuMulaiGangguan, tanggalGangguan=tanggalGangguan)
    return HttpResponseRedirect("{idSK}/{idG}".format(idSK=stasiunKerja.idStasiunKerja, idG=gangguan.id))

def gangguanForm(request, idStasiunKerjaInput, idGangguanInput):
    stasiunKerja = StasiunKerja.objects.filter(idStasiunKerja=idStasiunKerjaInput)
    gangguan = Gangguan.objects.filter(stasiunKerja__idStasiunKerja = idStasiunKerjaInput).order_by('-tanggalGangguan', '-waktuMulaiGangguan')
    gangguan_id = Gangguan.objects.filter(id=idGangguanInput)
    gangguan_form = GangguanForm(request.POST or None)

    if request.method == 'POST':
        idGangguan = request.POST.get('idGangguan')
        keterangan = request.POST.get('keterangan')

        Gangguan.objects.filter(id=idGangguanInput).update(idGangguan=idGangguan,
                                                           keterangan=keterangan)

        return HttpResponseRedirect("{idG}".format(idG=idGangguanInput))

    context = {
        'Judul': 'Gangguan',
        'stasiunKerja': stasiunKerja,
        'gangguan_form': gangguan_form,
        'gangguan': gangguan,
        'gangguan_id': gangguan_id,
    }
    return render(request, 'liniProduksi/gangguanStasiunKerja.html', context)

def liniProduksiTerhenti(request,idStasiunKerjaInput,idGangguanInput):
    waktuMulaiLiniProduksiTerhenti = datetime.datetime.now().time().replace(microsecond=0)

    Gangguan.objects.filter(id=idGangguanInput).update(status="Lini produksi terhenti",
                                                       waktuMulaiLiniProduksiTerhenti=waktuMulaiLiniProduksiTerhenti)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def gangguanSelesai(request, idStasiunKerjaInput, idGangguanInput):
    waktuGangguanSelesai = datetime.datetime.now().time().replace(microsecond=0)

    Gangguan.objects.filter(id=idGangguanInput).update(waktuSelesaiGangguan=waktuGangguanSelesai)

    gangguan = Gangguan.objects.get(id=idGangguanInput)

    t1 = datetime.datetime.strptime(str(gangguan.waktuSelesaiGangguan), '%H:%M:%S').replace(microsecond=0)
    t2 = datetime.datetime.strptime(str(gangguan.waktuMulaiGangguan), '%H:%M:%S').replace(microsecond=0)
    durasiGangguan_detik = abs(t1-t2).total_seconds()
    Gangguan.objects.filter(id=idGangguanInput).update(durasiGangguan=durasiGangguan_detik,
                                                       status="Gangguan selesai")

    if gangguan.waktuMulaiLiniProduksiTerhenti != None:
        Gangguan.objects.filter(id=idGangguanInput).update(waktuSelesaiLiniProduksiTerhenti=waktuGangguanSelesai)
        gangguan = Gangguan.objects.get(id=idGangguanInput)

        t3 = datetime.datetime.strptime(str(gangguan.waktuMulaiLiniProduksiTerhenti), '%H:%M:%S').replace(microsecond=0)
        t4 = datetime.datetime.strptime(str(gangguan.waktuSelesaiLiniProduksiTerhenti), '%H:%M:%S').replace(microsecond=0)
        durasiLiniProduksiTerhenti_detik = abs(t3 - t4).total_seconds()
        Gangguan.objects.filter(id=idGangguanInput).update(durasiLiniProduksiTerhenti = durasiLiniProduksiTerhenti_detik)

        jam_gangguan = durasiLiniProduksiTerhenti_detik // 3600
        menit_gangguan = (durasiLiniProduksiTerhenti_detik % 3600) // 60
        detik_gangguan = durasiLiniProduksiTerhenti_detik % 60
        timedelta_jadwal = datetime.timedelta(hours=jam_gangguan, minutes=menit_gangguan,
                                              seconds=detik_gangguan)

        gangguan_SK = StasiunKerja.objects.get(idStasiunKerja=idStasiunKerjaInput)
        sk_lp = LiniProduksi.objects.get(idLiniProduksi=gangguan_SK.liniProduksi)
        target = ProduksiHarian.objects.get(tanggalProduksi=gangguan.tanggalGangguan, liniProduksi = sk_lp.idLiniProduksi)
        targetHarian = TargetHarian.objects.filter(produksiHarian=target.id).order_by('waktuMulaiProduksi')

        waktuTarget_combine = datetime.datetime.combine(datetime.date(1, 1, 1), target.waktuSelesaiProduksiAktual)
        waktuTarget_update = (waktuTarget_combine + timedelta_jadwal).time()
        waktuMulaiTarget_combine = datetime.datetime.combine(datetime.date(1, 1, 1), target.waktuMulaiProduksiAktual)
        waktuMulaiTarget_update = (waktuMulaiTarget_combine + timedelta_jadwal).time()

        jadwal = JadwalLiniProduksi.objects.all()

        if target.is_lembur == 'Lembur':
            if gangguan.waktuMulaiLiniProduksiTerhenti < target.waktuMulaiProduksiAktual:
                ProduksiHarian.objects.filter(tanggalProduksi=gangguan.tanggalGangguan).filter(
                    liniProduksi__idLiniProduksi=sk_lp.idLiniProduksi).update(waktuMulaiProduksiAktual=waktuMulaiTarget_update,
                    waktuSelesaiProduksiAktual=waktuTarget_update, downtime=F('downtime') + durasiLiniProduksiTerhenti_detik
                )
            else:
                ProduksiHarian.objects.filter(tanggalProduksi=gangguan.tanggalGangguan).filter(
                    liniProduksi__idLiniProduksi=sk_lp.idLiniProduksi).update(
                    waktuSelesaiProduksiAktual=waktuTarget_update,
                    downtime=F('downtime') + durasiLiniProduksiTerhenti_detik
                )

            for th in targetHarian:
                waktuMulai_combine = datetime.datetime.combine(datetime.date(1, 1, 1),
                                                               th.waktuMulaiProduksiAktual)
                waktuMulai_update = (waktuMulai_combine + timedelta_jadwal).time()
                waktuSelesai_combine = datetime.datetime.combine(datetime.date(1, 1, 1),
                                                                 th.waktuSelesaiProduksiAktual)
                waktuSelesai_update = (waktuSelesai_combine + timedelta_jadwal).time()
                if th.waktuMulaiProduksiAktual > gangguan.waktuMulaiLiniProduksiTerhenti:
                    TargetHarian.objects.filter(id = th.id).update(
                        waktuMulaiProduksiAktual=waktuMulai_update, waktuSelesaiProduksiAktual=waktuSelesai_update
                    )
                elif (th.waktuMulaiProduksiAktual < gangguan.waktuMulaiLiniProduksiTerhenti) and (
                        th.waktuSelesaiProduksiAktual > gangguan.waktuMulaiLiniProduksiTerhenti):
                    TargetHarian.objects.filter(id=th.id).update(waktuSelesaiProduksiAktual=waktuSelesai_update
                                                                 )

            for j in jadwal:
                if j.tanggal == gangguan.tanggalGangguan:
                    if j.jadwalKedatangan > gangguan.waktuMulaiLiniProduksiTerhenti:
                        waktuKedatangan = j.jadwalKedatangan
                        waktuJadwalKedatangan_combine = datetime.datetime.combine(datetime.date(1, 1, 1), waktuKedatangan)
                        waktuKedatangan_update = (waktuJadwalKedatangan_combine + timedelta_jadwal).time()
                        istirahat = WaktuIstirahat.objects.filter(produksiHarian = target.id, waktuMulaiIstirahat__gte=target.waktuMulaiProduksi)
                        jumlahIstirahat = WaktuIstirahat.objects.filter(produksiHarian=target.id,
                                                                        waktuMulaiIstirahat__gte=target.waktuMulaiProduksi).count()

                        if waktuKedatangan_update < istirahat[0].waktuMulaiIstirahat:
                            JadwalLiniProduksi.objects.filter(id=j.id).update(jadwalKedatangan=waktuKedatangan_update)

                        m = 0
                        waktuIstirahatKumulatif = 0
                        while m < jumlahIstirahat - 1:
                            # durasi kumulatif istirahat
                            t_awalIst = istirahat[m].waktuMulaiIstirahat
                            t_awIst = str(t_awalIst)
                            t_akhirIst = istirahat[m].waktuSelesaiIstirahat
                            t_akIst = str(t_akhirIst)
                            FMT = '%H:%M:%S'
                            durasi_istirahat = datetime.datetime.strptime(t_akIst, FMT) - datetime.datetime.strptime(
                                t_awIst,
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
                            waktuKirim = datetime.datetime.combine(datetime.date(1, 1, 1), waktuKedatangan_update)
                            waktuKirim_ist = (waktuKirim + timedelta_durasi_ist).time()
                            if (waktuKirim_ist >= istirahat[m].waktuSelesaiIstirahat) and (
                                    waktuKirim_ist <= istirahat[m + 1].waktuMulaiIstirahat):
                                # jadwal + istirahat
                                JadwalLiniProduksi.objects.filter(id=j.id).update(
                                    jadwalKedatangan=waktuKirim_ist)
                                break
                            else:
                                m += 1

                        if waktuKedatangan_update >= istirahat[jumlahIstirahat - 1].waktuMulaiIstirahat:
                            k = 0
                            waktuIstirahatKum = 0
                            while k < jumlahIstirahat:
                                t_awalIst = istirahat[k].waktuMulaiIstirahat
                                t_awIst = str(t_awalIst)
                                t_akhirIst = istirahat[k].waktuSelesaiIstirahat
                                t_akIst = str(t_akhirIst)
                                FMT = '%H:%M:%S'
                                durasi_istirahat = datetime.datetime.strptime(t_akIst,
                                                                              FMT) - datetime.datetime.strptime(t_awIst,
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
                            waktuKirim = datetime.datetime.combine(datetime.date(1, 1, 1), waktuKedatangan_update)
                            waktuKirim_ist = (waktuKirim + timedelta_durasi_ist).time()
                            JadwalLiniProduksi.objects.filter(id = j.id).update(jadwalKedatangan = waktuKirim_ist)

        if target.is_lembur == 'Tidak lembur':
            if gangguan.waktuMulaiLiniProduksiTerhenti < target.waktuMulaiProduksiAktual:
                if waktuTarget_update > target.waktuSelesaiProduksi:
                    ProduksiHarian.objects.filter(tanggalProduksi=gangguan.tanggalGangguan).filter(
                        liniProduksi__idLiniProduksi=sk_lp.idLiniProduksi).update(waktuMulaiProduksiAktual=waktuMulaiTarget_update,
                        waktuSelesaiProduksiAktual=target.waktuSelesaiProduksi,
                        downtime=F('downtime') + durasiLiniProduksiTerhenti_detik
                        )
                else:
                    ProduksiHarian.objects.filter(tanggalProduksi=gangguan.tanggalGangguan).filter(
                        liniProduksi__idLiniProduksi=sk_lp.idLiniProduksi).update(waktuMulaiProduksiAktual=waktuMulaiTarget_update,
                        waktuSelesaiProduksiAktual=waktuTarget_update,
                        downtime=F('downtime') + durasiLiniProduksiTerhenti_detik
                        )

            else:
                if waktuTarget_update > target.waktuSelesaiProduksi:
                    ProduksiHarian.objects.filter(tanggalProduksi=gangguan.tanggalGangguan).filter(
                        liniProduksi__idLiniProduksi=sk_lp.idLiniProduksi).update(
                        waktuSelesaiProduksiAktual=target.waktuSelesaiProduksi,
                        downtime=F('downtime') + durasiLiniProduksiTerhenti_detik
                        )
                else:
                    ProduksiHarian.objects.filter(tanggalProduksi=gangguan.tanggalGangguan).filter(
                        liniProduksi__idLiniProduksi=sk_lp.idLiniProduksi).update(
                        waktuSelesaiProduksiAktual=waktuTarget_update,
                        downtime=F('downtime') + durasiLiniProduksiTerhenti_detik
                        )

            for th in targetHarian:
                waktuMulai_combine = datetime.datetime.combine(datetime.date(1, 1, 1),
                                                               th.waktuMulaiProduksiAktual)
                waktuMulai_update = (waktuMulai_combine + timedelta_jadwal).time()
                waktuSelesai_combine = datetime.datetime.combine(datetime.date(1, 1, 1),
                                                                 th.waktuSelesaiProduksiAktual)
                waktuSelesai_update = (waktuSelesai_combine + timedelta_jadwal).time()
                if th.waktuMulaiProduksiAktual > gangguan.waktuMulaiLiniProduksiTerhenti:
                    if waktuMulai_update > target.waktuSelesaiProduksi:
                        TargetHarian.objects.filter(id=th.id).update(waktuMulaiProduksiAktual=target.waktuSelesaiProduksi,
                                                                     waktuSelesaiProduksiAktual=target.waktuSelesaiProduksi)
                    elif waktuSelesai_update > target.waktuSelesaiProduksi:
                        TargetHarian.objects.filter(id=th.id).update(waktuMulaiProduksiAktual=waktuMulai_update,
                                                                     waktuSelesaiProduksiAktual=target.waktuSelesaiProduksi)
                    else:
                        TargetHarian.objects.filter(id=th.id).update(waktuMulaiProduksiAktual=waktuMulai_update,
                                                                     waktuSelesaiProduksiAktual=waktuSelesai_update)

                elif (th.waktuMulaiProduksiAktual < gangguan.waktuMulaiLiniProduksiTerhenti) and (
                        th.waktuSelesaiProduksiAktual > gangguan.waktuMulaiLiniProduksiTerhenti):
                    if waktuSelesai_update > target.waktuSelesaiProduksi:
                        TargetHarian.objects.filter(id=th.id).update(
                            waktuSelesaiProduksiAktual=target.waktuSelesaiProduksi)
                    else:
                        TargetHarian.objects.filter(id=th.id).update(waktuSelesaiProduksiAktual=waktuSelesai_update)

            for j in jadwal:
                if j.tanggal == gangguan.tanggalGangguan:
                    if j.jadwalKedatangan > gangguan.waktuMulaiLiniProduksiTerhenti:
                        waktuKedatangan = j.jadwalKedatangan
                        waktuJadwalKedatangan_combine = datetime.datetime.combine(datetime.date(1, 1, 1), waktuKedatangan)
                        waktuKedatangan_update = (waktuJadwalKedatangan_combine + timedelta_jadwal).time()
                        istirahat = WaktuIstirahat.objects.filter(produksiHarian=target.id,
                                                                  waktuMulaiIstirahat__gte=target.waktuMulaiProduksi)
                        jumlahIstirahat = WaktuIstirahat.objects.filter(produksiHarian=target.id,
                                                                        waktuMulaiIstirahat__gte=target.waktuMulaiProduksi).count()

                        if waktuKedatangan_update < istirahat[0].waktuMulaiIstirahat:
                            JadwalLiniProduksi.objects.filter(id=j.id).update(jadwalKedatangan=waktuKedatangan_update)
                            jadwal_id = JadwalLiniProduksi.objects.get(id=j.id)
                            if jadwal_id.jadwalKedatangan >= target.waktuSelesaiProduksi:
                                JadwalLiniProduksi.objects.filter(id=j.id).delete()

                        m = 0
                        waktuIstirahatKumulatif = 0
                        while m < jumlahIstirahat - 1:
                            # durasi kumulatif istirahat
                            t_awalIst = istirahat[m].waktuMulaiIstirahat
                            t_awIst = str(t_awalIst)
                            t_akhirIst = istirahat[m].waktuSelesaiIstirahat
                            t_akIst = str(t_akhirIst)
                            FMT = '%H:%M:%S'
                            durasi_istirahat = datetime.datetime.strptime(t_akIst, FMT) - datetime.datetime.strptime(
                                t_awIst,
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
                            waktuKirim = datetime.datetime.combine(datetime.date(1, 1, 1), waktuKedatangan_update)
                            waktuKirim_ist = (waktuKirim + timedelta_durasi_ist).time()
                            if (waktuKirim_ist >= istirahat[m].waktuSelesaiIstirahat) and (
                                    waktuKirim_ist <= istirahat[m + 1].waktuMulaiIstirahat):
                                # jadwal + istirahat
                                JadwalLiniProduksi.objects.filter(id=j.id).update(
                                    jadwalKedatangan=waktuKirim_ist)
                                jadwal_id = JadwalLiniProduksi.objects.get(id=j.id)
                                if jadwal_id.jadwalKedatangan >= target.waktuSelesaiProduksi:
                                    JadwalLiniProduksi.objects.filter(id=j.id).delete()
                                break
                            else:
                                m += 1

                        if waktuKedatangan_update >= istirahat[jumlahIstirahat - 1].waktuMulaiIstirahat:
                            k = 0
                            waktuIstirahatKum = 0
                            while k < jumlahIstirahat:
                                t_awalIst = istirahat[k].waktuMulaiIstirahat
                                t_awIst = str(t_awalIst)
                                t_akhirIst = istirahat[k].waktuSelesaiIstirahat
                                t_akIst = str(t_akhirIst)
                                FMT = '%H:%M:%S'
                                durasi_istirahat = datetime.datetime.strptime(t_akIst,
                                                                              FMT) - datetime.datetime.strptime(t_awIst,
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
                            waktuKirim = datetime.datetime.combine(datetime.date(1, 1, 1), waktuKedatangan_update)
                            waktuKirim_ist = (waktuKirim + timedelta_durasi_ist).time()
                            JadwalLiniProduksi.objects.filter(id=j.id).update(jadwalKedatangan=waktuKirim_ist)
                            jadwal_id = JadwalLiniProduksi.objects.get(id=j.id)
                            if jadwal_id.jadwalKedatangan >= target.waktuSelesaiProduksi:
                                JadwalLiniProduksi.objects.filter(id=j.id).delete()


    return redirect('liniProduksi:gangguan')