from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from decimal import Decimal, getcontext
from .models import ContactLens

# Create your views here.
def index(request):
    cl_list = ContactLens.objects.order_by('clens')
    context = {'cl_list': cl_list}
    return render(request, 'cl/index.html', context)

def results(request):
    od_cl = request.POST['od_cl']
    od_contactlens = ContactLens.objects.get(pk=od_cl)
    od_yearsupply = od_contactlens.num_year_supply * od_contactlens.cost_per_package
    od_6month_supply = od_yearsupply / Decimal(2)
    os_cl = request.POST['os_cl']
    os_contactlens = ContactLens.objects.get(pk=os_cl)
    os_yearsupply = os_contactlens.num_year_supply * os_contactlens.cost_per_package
    os_6month_supply = os_yearsupply / Decimal(2)
    year_supply = od_yearsupply + os_yearsupply
    year_discount = year_supply / Decimal('5')
    halfyear_supply = od_6month_supply + os_6month_supply
    halfyear_discount = "0.00"
    discounted_year_supply = year_supply - year_discount
    cl_service_amt = Decimal(request.POST['cl_service_amt'])
    exam_amt = Decimal(request.POST['exam_amt'])
    benefit_amt = Decimal(request.POST['benefit_amt'])
    total_year = discounted_year_supply + cl_service_amt + exam_amt - benefit_amt
    total_halfyear = halfyear_supply + cl_service_amt + exam_amt - benefit_amt
    context = {
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
        'total_halfyear' : total_halfyear,
    }
    return render(request, 'cl/results.html', context)
