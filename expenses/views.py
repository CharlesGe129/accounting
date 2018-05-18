from django.shortcuts import render, redirect
from .models import Expense, Category
import datetime


def index(request):
    month = datetime.datetime.today().strftime('%Y-%m')
    expenses = Expense.objects.filter(created_at__startswith=month)
    context = index_context(expenses)
    return render(request, 'expenses/index.html', context)


def index_context(expenses):
    sum_expense = 0
    for expense in expenses:
        expense.type = 'Expense' if expense.type_id == 0 else 'Income'
        sum_expense += expense.amount if expense.type_id == 0 else -expense.amount
        expense.created_at = expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
    avg_expense = sum_expense / int(datetime.datetime.today().strftime('%m'))
    return {'expenses': expenses, 'sum': sum_expense, 'avg': round(avg_expense, 2)}


def edit(request, expense_id):
    msg = ''
    if request.method == 'POST':
        edit_expense(request.POST, Expense.objects.filter(id=expense_id)[0])
        msg = 'Expense updated successfully'
        return redirect('/expenses')
    return render(request, 'expenses/edit.html', edit_context(expense_id), msg)


def edit_context(expense_id, msg=''):
    return {'expense': Expense.objects.filter(id=expense_id)[0], 'categories': Category.objects.all(), 'msg': msg}


def edit_expense(params, expense):
    expense.name = params['name']
    expense.amount = params['amount']
    expense.type_id = params['type_id']
    expense.comment = params['comment']
    expense.category = Category.objects.filter(id=params['category_id'])[0]
    expense.save()


def new(request):
    if request.method == 'GET':
        return render(request, 'expenses/new.html', {'categories': Category.objects.all()})
    elif request.method == 'POST':
        params = request.POST
        expense = Expense(name=params['name'], amount=params['amount'], type_id=params['type_id'],
                          comment=params['comment'], category=Category.objects.filter(id=params['category_id'])[0])
        expense.save()
        return redirect('/expenses')
