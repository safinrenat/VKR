from django.shortcuts import render, redirect
from django.http import HttpResponse
from news.forms import UserDataForm
from news.models import UserData
from news.models import Food
from news.models import Transport
from news.models import Fun
from news.models import Sport
from decimal import Decimal


# Create your views here.

#def index(request):
    #print(request)
    #return HttpResponse('Hello world')

#def index(request):
    #if request.method == 'POST':
       # form = UserDataForm(request.POST)
        #if form.is_valid():
            #form.save()
            #return redirect('result/')
    #else:
        #form = UserDataForm()
    #return render(request, 'news/index.html', {'form': form})

def index(request):
    error = ''
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            food_weight = form.cleaned_data['food_weight']
            transport_weight = form.cleaned_data['transport_weight']
            fun_weight = form.cleaned_data['fun_weight']
            sport_weight = form.cleaned_data['sport_weight']
            sum = food_weight + transport_weight + fun_weight + sport_weight
            if sum == 100:
              form.save()
              return redirect('result/')
            else:
                error = 'Сумма удельных весов сфер жизни не равна 100%. Проверьте корректность ввода данных'
    else:
        form = UserDataForm()
    return render(request, 'news/index.html', {'form': form, 'error': error})

def result(request):
    result_data = UserData.objects.last()
    result_data.monthly_budget = result_data.monthly_income - result_data.credit_payment - result_data.apartment_costs - result_data.education_payment - result_data.other_expenses
    result_data.food_budget = ((result_data.monthly_budget / result_data.family_number) * result_data.food_weight / 100).quantize(Decimal("1.00"))
    result_data.transport_budget = ((result_data.monthly_budget / result_data.family_number) * result_data.transport_weight / 100).quantize(Decimal("1.00"))
    result_data.fun_budget = ((result_data.monthly_budget / result_data.family_number) * result_data.fun_weight / 100).quantize(Decimal("1.00"))
    result_data.sport_budget = ((result_data.monthly_budget / result_data.family_number) * result_data.sport_weight / 100).quantize(Decimal("1.00"))
    result_data.save()
    #optimal = UserData.objects.last().food_selection
    #UserData.objects.last().food_selection
    #result_data.food_selection
    #optimal = [2, 4, 6]
    #food_optimal = result_data.food_selection
    #food_set = Food.objects.order_by('-id')[:3]
    food_set = Food.objects.filter(id__in = result_data.food_selection())
    #food_set = Food.objects.filter(id__in = optimal)
    #food_set = Food.objects.filter(id__in = food_optimal)
    food_cal_total = 0
    food_cost_total = 0
    for item in result_data.food_selection():
        food_cal_total = food_cal_total + Food.objects.get(id = item).calorific
        food_cost_total = food_cost_total + Food.objects.get(id = item).cost

    transport_set = Transport.objects.filter(id__in=result_data.transport_selection().keys())
    #transport_set_number = result_data.transport_selection()
    #for tsn in transport_set_number:
       # transport_set_number[Transport.objects.get(id = tsn).name] = transport_set_number.pop(tsn)

    transport_set_number_orig = result_data.transport_selection()
    transport_set_number = {}
    for tsn in transport_set_number_orig:
        key = Transport.objects.get(id=tsn).name
        value = int(transport_set_number_orig[tsn])
        transport_set_number[key] = value
        #transport_set_number[Transport.objects.get(id=tsn).name] = transport_set_number.pop(tsn)

    transport_cost_total = 0
    #for item in result_data.transport_selection().keys():
        #transport_cost_total = transport_cost_total + Transport.objects.get(id=item).cost

    for item in transport_set_number_orig:
        transport_cost_total = transport_cost_total + (Transport.objects.get(id=item).cost * int(transport_set_number_orig[item]))

    fun_set = Fun.objects.filter(id__in=result_data.fun_selection().keys())
    fun_set_number_orig = result_data.fun_selection()
    fun_set_number = {}
    for tsn in fun_set_number_orig:
        key = Fun.objects.get(id=tsn).name
        value = int(fun_set_number_orig[tsn])
        fun_set_number[key] = value

    fun_cost_total = 0
    for item in fun_set_number_orig:
        fun_cost_total = fun_cost_total + (Fun.objects.get(id=item).cost * int(fun_set_number_orig[item]))

    sport_set = Sport.objects.filter(id__in=result_data.sport_selection().keys())
    sport_set_number_orig = result_data.sport_selection()
    sport_set_number = {}
    for tsn in sport_set_number_orig:
        key = Sport.objects.get(id=tsn).name
        value = int(sport_set_number_orig[tsn])
        sport_set_number[key] = value

    sport_cost_total = 0
    for item in sport_set_number_orig:
        sport_cost_total = sport_cost_total + (Sport.objects.get(id=item).cost * int(sport_set_number_orig[item]))

    return render(request, 'news/result.html', {'result_data': result_data, 'food_set': food_set, 'food_cal_total': food_cal_total, 'food_cost_total': food_cost_total, 'transport_set': transport_set, 'transport_set_number': transport_set_number, 'transport_cost_total': transport_cost_total, 'fun_set': fun_set, 'fun_set_number': fun_set_number, 'fun_cost_total': fun_cost_total, 'sport_set': sport_set, 'sport_set_number': sport_set_number, 'sport_cost_total': sport_cost_total})