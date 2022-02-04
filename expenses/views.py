from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
from expenses.models import Category, Expense
from expenses.utils import now
import datetime
import json
import csv
import xlwt

from django.db.models import Sum
from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile


# Create your views here.
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__startswith=search_str,
            owner = request.user
        ) | Expense.objects.filter(
            date__istartswith=search_str,
            owner = request.user
        ) | Expense.objects.filter(
            description__icontains=search_str,
            owner = request.user
        ) | Expense.objects.filter(
            category__icontains=search_str,
            owner = request.user
        )
        data = expenses.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user).all()
    currency = UserPreference.objects.get(user=request.user).currency

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'expenses':expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    from datetime import datetime
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

    return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='/authentication/login')
def edit_expense(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    else:
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount 입력은 필수입니다.')
            return render(request, 'expenses/edit-expense.html', context)
        elif not description:
            messages.error(request, 'Description 입력은 필수입니다.')
            return render(request, 'expenses/edit-expense.html', context)
        
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()
        messages.success(request, '지출내역이 갱신되었습니다.')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk = id)
    expense.delete()
    messages.success(request, '지출내역이 삭제되었습니다.')
    return redirect('expenses')
    

def expense_category_summary(request):
    today = datetime.date.today()
    six_months_ago = today - datetime.timedelta(days=30*6)

    expenses = Expense.objects.filter(owner = request.user, date__gte = six_months_ago, date__lte = today)
    category_list = list(set(map(lambda x:x.category, expenses)))

    finalrep = {}
    for y in category_list:
        finalrep[y] = sum(item.amount for item in expenses.filter(category=y))

    return JsonResponse({'expense_category_data':finalrep}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner = request.user)
    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    
    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    
    expenses = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')
    
    for expense in expenses:
        row_num += 1
        for col_num in range(len(expense)):
            ws.write(row_num, col_num, str(expense[col_num]), font_style)

    wb.save(response)

    return response

# Only on Linux
# def export_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'

#     expenses = Expense.objects.filter(owner = request.user)
#     sum = expenses.aggregate(Sum('amount'))

#     html_string = render_to_string('expenses/pdf-output', {'expenses':expenses, "total":sum['amount__sum']})
#     html = HTML(string = html_string)

#     result = html.write_pdf()
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())

#     return response

