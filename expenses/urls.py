from django.urls import path
from expenses.views import delete_expense, edit_expense, export_csv, export_excel, index, add_expense, search_expenses, expense_category_summary, stats_view
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='expenses'),
    path('add-expense', add_expense, name='add-expense'),
    path('edit-expense/<int:id>', edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>', delete_expense, name='delete-expense'),
    path('search-expenses', csrf_exempt(search_expenses), name='search-expenses'),
    path('expense_category_summary', expense_category_summary, name="expense_category_summary"),
    path('stats', stats_view, name="stats"),
    path('export-csv', export_csv, name='export-csv'),
    path('export-excel', export_excel, name='export-excel'),
    # path('export-pdf', export_pdf, name='export-pdf')
]