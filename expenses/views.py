from django.shortcuts import render
from django.http import HttpResponse
from .models import Expense


def index(request):
    expenses = Expense.objects.order_by('id')
    context = index_form(expenses)
    return render(request, 'expenses/index.html', context)


def index_form(expenses):
    sum_expense = 0
    for expense in expenses:
        expense.type = 'Expense' if expense.type_id == 0 else 'Income'
        sum_expense += expense.amount if expense.type_id == 0 else -expense.amount
    avg_expense = sum_expense / expenses.count()
    return {'expenses': expenses, 'sum': sum_expense, 'avg': round(avg_expense, 2)}
