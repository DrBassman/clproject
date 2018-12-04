from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

import datetime

from decimal import Decimal, getcontext
from .models import ContactLens, ConfigDefaults

# Create your views here.
def index(request):
    cl_list = ContactLens.objects.order_by('clens')
    for cl in cl_list:
        cl.ys = cl.cost_per_package * cl.num_year_supply * 2
    def_amts = ConfigDefaults.objects.get(pk=1)
    cur_dt = datetime.date.today().strftime('%Y-%m-%d')
    print(cur_dt)
    context = {
        'cl_list': cl_list,
        'def_amts': def_amts,
        'cur_dt': cur_dt,
    }
    return render(request, 'cl/index.html', context)

def results(request):
    def_amts = ConfigDefaults.objects.get(pk=1)
    TP = Decimal(10) ** -2
    exam_dt = datetime.datetime.strptime(request.POST['exam_dt'], "%Y-%m-%d").date()
    od_cl = request.POST['od_cl']
    od_contactlens = ContactLens.objects.get(pk=od_cl)
    od_contactlens.ys = (od_contactlens.cost_per_package * ((Decimal(100.0) - def_amts.def_ys_discount) / Decimal(100.0))).quantize(TP)
    od_rebates = od_contactlens.contactrebate_set.exclude(to_dt__lt=exam_dt).exclude(from_dt__gt=exam_dt)
    od_yearsupply = (od_contactlens.num_year_supply * od_contactlens.cost_per_package).quantize(TP)
    od_6month_supply = (od_yearsupply / Decimal(2)).quantize(TP)
    os_cl = request.POST['os_cl']
    os_contactlens = ContactLens.objects.get(pk=os_cl)
    os_contactlens.ys = (os_contactlens.cost_per_package * ((Decimal(100.0) - def_amts.def_ys_discount) / Decimal(100.0))).quantize(TP)
    os_rebates = os_contactlens.contactrebate_set.exclude(to_dt__lt=exam_dt).exclude(from_dt__gt=exam_dt)
    os_yearsupply = (os_contactlens.num_year_supply * os_contactlens.cost_per_package).quantize(TP)
    os_6month_supply = (os_yearsupply / Decimal(2)).quantize(TP)
    year_supply = (od_yearsupply + os_yearsupply).quantize(TP)
    year_discount = (year_supply * (def_amts.def_ys_discount / Decimal(100.0))).quantize(TP)
    halfyear_supply = (od_6month_supply + os_6month_supply).quantize(TP)
    halfyear_discount = (Decimal("0.00")).quantize(TP)
    discounted_year_supply = (year_supply - year_discount).quantize(TP)
    cl_service_amt = (Decimal(request.POST['cl_service_amt'])).quantize(TP)
    exam_amt = (Decimal(request.POST['exam_amt'])).quantize(TP)
    benefit_amt = (Decimal(request.POST['benefit_amt'])).quantize(TP)
    total_year = (discounted_year_supply + cl_service_amt + exam_amt - benefit_amt).quantize(TP)
    total_halfyear = (halfyear_supply + cl_service_amt + exam_amt - benefit_amt).quantize(TP)
    rebates = []
    amt = Decimal(0)
    num_exclusive=0
    num_nonexclusive=0
    od_ne = Decimal(0)
    os_ne = Decimal(0)
    dtot_ne = Decimal(0)
    tot_year_ne = Decimal(0)
    num_rebates = 0
    if len(od_rebates) == len(os_rebates) and len(od_rebates) > 0:
        for i in range(0,len(od_rebates)):
            num_rebates += 1
            rebates.append({
                'amt': (od_rebates[i].amt + os_rebates[i].amt).quantize(TP),
                'dtot': (discounted_year_supply - od_rebates[i].amt - os_rebates[i].amt).quantize(TP),
                'gtot': (total_year - od_rebates[i].amt - os_rebates[i].amt).quantize(TP),
            })
            if od_rebates[i].exclusive:
                num_exclusive += 1
            else:
                num_nonexclusive += 1
                od_ne += od_rebates[i].amt
                os_ne += os_rebates[i].amt
                amt += od_rebates[i].amt + os_rebates[i].amt
# Kludge!!!!!  Want to get total for non-exclusive Rebates added together
#        if num_exclusive == 0:
#            rebates[0]['amt'] = (amt).quantize(TP)
#            rebates[0]['dtot'] = (discounted_year_supply - amt).quantize(TP)
#            rebates[0]['gtot'] = (total_year - amt).quantize(TP)
    if num_nonexclusive > 1:
        num_rebates += 1
        od_ne = (od_ne).quantize(TP)
        os_ne = (os_ne).quantize(TP)
        amt = (amt).quantize(TP)
        dtot_ne = (discounted_year_supply - amt).quantize(TP)
        tot_year_ne = (total_year - amt).quantize(TP)
    else:
        od_ne = 0
        os_ne = 0
        amt = 0
        dtot_ne = 0
        tot_year_ne = 0
    context = {
        'exam_dt': exam_dt.strftime("%m/%d/%Y"),
        'od_contactlens': od_contactlens,
        'od_yearsupply': od_yearsupply,
        'od_6month_supply': od_6month_supply,
        'os_contactlens': os_contactlens,
        'os_yearsupply': os_yearsupply,
        'os_6month_supply': os_6month_supply,
        'year_supply': year_supply,
        'year_discount': year_discount,
        'discounted_year_supply': discounted_year_supply,
        'halfyear_supply': halfyear_supply,
        'halfyear_discount': halfyear_discount,
        'cl_service_amt': cl_service_amt,
        'exam_amt': exam_amt,
        'benefit_amt': benefit_amt,
        'total_year': total_year,
        'total_halfyear': total_halfyear,
        'od_rebates': od_rebates,
        'os_rebates': os_rebates,
        'rebates': rebates,
        'amt': amt,
        'od_ne': od_ne,
        'os_ne': os_ne,
        'dtot_ne': dtot_ne,
        'tot_year_ne': tot_year_ne,
        'num_rebates': (num_rebates * 2),
    }
    return render(request, 'cl/results.html', context)
