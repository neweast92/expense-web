from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from expenses.models import Category, Expense
from django.contrib import messages

from expenses.utils import edit_date, now
# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user).all()
    context = {
        'expenses':expenses
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    date = now()
    
    context = {
        'categories': categories,
        'date': date,
        'values': request.POST
    }
    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount 입력은 필수입니다.')
        elif not description:
            messages.error(request, 'Description 입력은 필수입니다.')
        else:
            Expense.objects.create(amount=amount, date=date, category=category, description=description, owner=request.user)

            messages.success(request, '지출내역이 저장되었습니다.')

        return redirect('expenses')

    return render(request, 'expenses/add_expense.html', context)


def edit_expense(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    expense.date = edit_date(expense.date)
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    else:
        return render(request, 'expenses/edit-expense.html', context)