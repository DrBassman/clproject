from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

import datetime

from decimal import Decimal, getcontext
from .models import ContactLens

# Create your views here.
def index(request):
    cl_list = ContactLens.objects.order_by('clens')
    cur_dt = datetime.date.today().strftime('%Y-%m-%d')
    context = {
        'cl_list': cl_list,
        'cur_dt': cur_dt,
    }
    return render(request, 'cl/index.html', context)

def results(request):
    TP = Decimal(10) ** -2
    exam_dt = request.POST['exam_dt']
    od_cl = request.POST['od_cl']
    od_contactlens = ContactLens.objects.get(pk=od_cl)
    od_rebates = od_contactlens.contactrebate_set.exclude(to_dt__lt=exam_dt).exclude(from_dt__gt=exam_dt)
    od_yearsupply = (od_contactlens.num_year_supply * od_contactlens.cost_per_package).quantize(TP)
    od_6month_supply = (od_yearsupply / Decimal(2)).quantize(TP)
    os_cl = request.POST['os_cl']
    os_contactlens = ContactLens.objects.get(pk=os_cl)
    os_rebates = os_contactlens.contactrebate_set.exclude(to_dt__lt=exam_dt).exclude(from_dt__gt=exam_dt)
    os_yearsupply = (os_contactlens.num_year_supply * os_contactlens.cost_per_package).quantize(TP)
    os_6month_supply = (os_yearsupply / Decimal(2)).quantize(TP)
    year_supply = (od_yearsupply + os_yearsupply).quantize(TP)
    year_discount = (year_supply * Decimal('0.20')).quantize(TP)
    halfyear_supply = (od_6month_supply + os_6month_supply).quantize(TP)
    halfyear_discount = (Decimal("0.00")).quantize(TP)
    discounted_year_supply = (year_supply - year_discount).quantize(TP)
    cl_service_amt = (Decimal(request.POST['cl_service_amt'])).quantize(TP)
    exam_amt = (Decimal(request.POST['exam_amt'])).quantize(TP)
    benefit_amt = (Decimal(request.POST['benefit_amt'])).quantize(TP)
    total_year = (discounted_year_supply + cl_service_amt + exam_amt - benefit_amt).quantize(TP)
    total_halfyear = (halfyear_supply + cl_service_amt + exam_amt - benefit_amt).quantize(TP)
    rebates = []
    amt = 0
    num_exclusive=0
    if len(od_rebates) == len(os_rebates) and len(od_rebates) > 0:
        for i in range(0,len(od_rebates)):
            if od_rebates[i].exclusive:
                num_exclusive += 1
                rebates.append({
                    'amt': (od_rebates[i].amt + os_rebates[i].amt).quantize(TP),
                    'dtot': (discounted_year_supply - od_rebates[i].amt - os_rebates[i].amt).quantize(TP),
                    'gtot': (total_year - od_rebates[i].amt - os_rebates[i].amt).quantize(TP),
                })
            else:
                rebates.append({'amt' : (od_rebates[i].amt + os_rebates[i].amt).quantize(TP)})
                amt += od_rebates[i].amt + os_rebates[i].amt
# Kludge!!!!!  Want to get total for non-exclusive Rebates added together
        if num_exclusive == 0:
            rebates[0]['amt'] = (amt).quantize(TP)
            rebates[0]['dtot'] = (discounted_year_supply - amt).quantize(TP)
            rebates[0]['gtot'] = (total_year - amt).quantize(TP)
    context = {
        'exam_dt': exam_dt,
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
    }
    return render(request, 'cl/results.html', context)
