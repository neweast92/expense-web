from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from userincome.models import Source, UserIncome
from userpreferences.models import UserPreference
from expenses.utils import now
import json


# Create your views here.
def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        incomes = UserIncome.objects.filter(
            amount__startswith=search_str,
            owner = request.user
        ) | UserIncome.objects.filter(
            date__istartswith=search_str,
            owner = request.user
        ) | UserIncome.objects.filter(
            description__icontains=search_str,
            owner = request.user
        ) | UserIncome.objects.filter(
            source__icontains=search_str,
            owner = request.user
        )
        data =incomes.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    income = UserIncome.objects.filter(owner=request.user).all()
    currency = UserPreference.objects.get(user=request.user).currency

    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'income':income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    from datetime import datetime
    sources = Source.objects.all()
    date = now()
    
    context = {
        'sources': sources,
        'date': date,
        'values': request.POST
    }
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount 입력은 필수입니다.')
        elif not description:
            messages.error(request, 'Description 입력은 필수입니다.')
        else:
            UserIncome.objects.create(amount=amount, date=date, source=source, description=description, owner=request.user)

            messages.success(request, '수입내역이 저장되었습니다.')
            return redirect('income')

        return render(request, 'income/add_income.html', context)

    return render(request, 'income/add_income.html', context)


@login_required(login_url='/authentication/login')
def edit_income(request, id):
    sources = Source.objects.all()
    income = UserIncome.objects.get(pk=id)
    
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    else:
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount 입력은 필수입니다.')
            return render(request, 'income/edit_income.html', context)
        elif not description:
            messages.error(request, 'Description 입력은 필수입니다.')
            return render(request, 'income/edit_income.html', context)
        
        income.owner = request.user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.save()
        messages.success(request, '수입내역이 갱신되었습니다.')

        return redirect('income')


@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk = id)
    income.delete()
    messages.success(request, '수입내역이 삭제되었습니다.')
    return redirect('income')