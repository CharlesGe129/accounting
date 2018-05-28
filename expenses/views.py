from django.shortcuts import render, redirect
from .models import Expense, Category
import datetime


def index(request):
    exclude_cat = [each for each in request.GET.get('cat').split(',')] if request.GET.get('cat') is not None else []
    month = datetime.datetime.today().strftime('%Y-%m')
    expenses = Expense.objects\
        .filter(created_at__startswith=month)\
        .exclude(category__in=Category.objects.filter(id__in=exclude_cat))
    context = index_context(expenses)
    return render(request, 'expenses/index.html', context)


def index_context(expenses):
    sum_expense = 0
    for expense in expenses:
        expense.type = 'Expense' if expense.type_id == 0 else 'Income'
        sum_expense += expense.amount if expense.type_id == 0 else -expense.amount
        expense.created_at = expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
    avg_expense = sum_expense / int(datetime.datetime.today().strftime('%d'))
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
    expense.amount_fake = params['amount_fake'] if params['amount_fake'] else float(params['amount']) * 1.2
    expense.type_id = params['type_id']
    expense.comment = params['comment']
    expense.category = Category.objects.filter(id=params['category_id'])[0]
    expense.save()


def new(request):
    if request.method == 'GET':
        return render(request, 'expenses/new.html', {'categories': Category.objects.all()})
    elif request.method == 'POST':
        params = request.POST
        expense = Expense(name=params['name'], amount=params['amount'],
                          amount_fake=params['amount_fake'] if params['amount_fake'] else float(params['amount']) * 1.2
                          , type_id=params['type_id'], comment=params['comment'],
                          category=Category.objects.filter(id=params['category_id'])[0])
        expense.save()
        return redirect('/expenses')
