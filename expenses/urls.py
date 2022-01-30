from django.urls import path
from expenses.views import edit_expense, index, add_expense

urlpatterns = [
    path('', index, name='expenses'),
    path('add-expense', add_expense, name='add-expense'),
    path('edit-expense/<int:id>', edit_expense, name='edit-expense')
]