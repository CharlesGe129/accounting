from django.shortcuts import render
from .models import Expense
import datetime


def index(request):
    month = datetime.datetime.today().strftime('%Y-%m')
    expenses = Expense.objects.filter(created_at__startswith=month)
    context = index_form(expenses)
    return render(request, 'expenses/index.html', context)


def index_form(expenses):
    sum_expense = 0
    for expense in expenses:
        expense.type = 'Expense' if expense.type_id == 0 else 'Income'
        sum_expense += expense.amount if expense.type_id == 0 else -expense.amount
    avg_expense = sum_expense / expenses.count()
    return {'expenses': expenses, 'sum': sum_expense, 'avg': round(avg_expense, 2)}
