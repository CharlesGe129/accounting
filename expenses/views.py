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
    sum_income = 0
    for expense in expenses:
        expense.type = 'Expense' if expense.type_id == 0 else 'Income'
        if expense.type_id == 0:
            sum_expense += expense.amount
        else:
            sum_income += expense.amount
        expense.created_at = expense.created_at.strftime('%Y-%m-%d %H:%M:%S')
    avg_expense = sum_expense / int(datetime.datetime.today().strftime('%d'))
    avg_income = sum_income / int(datetime.datetime.today().strftime('%d'))
    return {'expenses': expenses, 'sum_ex': sum_expense, 'avg_ex': round(avg_expense, 2),
            'sum_in': sum_income, 'avg_in': round(avg_income, 2)}


def edit(request, expense_id):
    msg = ''
    expense = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        edit_expense(request.POST, expense)
        msg = 'Expense updated successfully'
        return redirect('/expenses')
    return render(request, 'expenses/edit.html', edit_context(expense), msg)


def edit_context(expense, msg=''):
    return {'expense': expense, 'categories': Category.objects.all(), 'msg': msg}


def edit_expense(params, expense):
    amount = sum(list(map(float, params['amount'].split(', '))))
    expense.name = params['name']
    expense.amount = amount
    expense.amount_fake = params['amount_fake']
    expense.type_id = params['type_id']
    expense.comment = params['comment']
    expense.category = Category.objects.get(id=params['category_id'])
    expense.cal_amount_fake()
    expense.save()


def new(request):
    if request.method == 'GET':
        return render(request, 'expenses/new.html', {'categories': Category.objects.all()})
    elif request.method == 'POST':
        params = request.POST
        amount = sum(list(map(float, params['amount'].split(', '))))
        Expense.create(params['name'], params['category_id'], amount=amount, amount_fake=params['amount_fake'],
                       type_id=params['type_id'], comment=params['comment'])
        return redirect('/expenses')
