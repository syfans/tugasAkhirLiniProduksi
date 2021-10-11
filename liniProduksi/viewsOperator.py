from django.shortcuts import render, redirect

from .models import Operator, Proses, StasiunKerja
from django.contrib.auth.models import User
from .forms import OperatorForm
from django.http import HttpResponseRedirect

def newOperator(request):
    operator_form = OperatorForm(request.POST or None)

    # masukin data dari form ke database
    if request.method == 'POST':
        id = request.POST.get('id')
        proses = request.POST.get('proses')
        namaLengkap = request.POST.get('namaLengkap')
        levelOperator = request.POST.get('levelOperator')

        proses_sk = Proses.objects.get(idProses=proses)
        p_sk = str(proses_sk.stasiunKerja)
        stasiunKerja = StasiunKerja.objects.get(idStasiunKerja=p_sk)
        Operator.objects.create(id=id, stasiunKerja=stasiunKerja, proses=proses_sk, namaLengkap=namaLengkap, levelOperator=levelOperator)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

    context = {
        'Judul': 'Tambah Operator',
        'operator_form': operator_form,
    }
    return render(request, 'liniProduksi/newOperator.html', context)

def deleteOperator(request, delete_id):
    #cara delete
    Operator.objects.filter(id=delete_id).delete()
    if request.method == 'GET':
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)

def updateOperator(request, update_id):
    #cara edit Produk
    operator_update = Operator.objects.get(id=update_id)

    data = {
        'proses': operator_update.proses,
        'namaLengkap': operator_update.namaLengkap,
        'levelOperator':operator_update.levelOperator,
    }

    operator_form = OperatorForm(request.POST or None, initial=data, instance=operator_update)

    if request.method == 'POST':
        #validasi data
        if operator_form.is_valid():
            operator_form.save()
            #menyimpan ke database
            operator_form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'Judul': 'Update Operator',
        'operator_form': operator_form,
    }

    return render(request,'liniProduksi/newOperator.html',context)