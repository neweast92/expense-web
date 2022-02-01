from django.urls import path
from expenses.views import delete_expense, edit_expense, index, add_expense, search_expenses
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='expenses'),
    path('add-expense', add_expense, name='add-expense'),
    path('edit-expense/<int:id>', edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>', delete_expense, name='delete-expense'),
    path('search-expenses', csrf_exempt(search_expenses), name='search-expenses')
]