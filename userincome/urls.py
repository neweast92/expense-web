from django.urls import path
from userincome.views import delete_income, edit_income, index, add_income, search_incomes
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='income'),
    path('add-income', add_income, name='add-income'),
    path('edit-income/<int:id>', edit_income, name='edit-income'),
    path('delete-income/<int:id>', delete_income, name='delete-income'),
    path('search-incomes', csrf_exempt(search_incomes), name='search-incomes')
]