from django.shortcuts import render
from expenses.models import Expense, Category


def index(request):
    expenses = Expense.objects.all().order_by('-created_at')
    return render(request, 'stats/index.html', index_context(expenses))


def index_context(expenses):
    rs = dict()
    stats = form_expenses_each_month(expenses)
    categories = dict_id_to_category()
    for month in stats:
        rs[month] = {'sum': stats[month]['sum'], 'details': dict()}
        for category, amount in stats[month].items():
            if category == 'sum':
                continue
            name = categories[category]
            rs[month]['details'][name] = amount
    for month in rs:
        rs[month]['details'] = [(key, rs[month]['details'][key]) for key in
                                sorted(rs[month]['details'], key=rs[month]['details'].get, reverse=True)]
    return {'stats': rs}


def form_expenses_each_month(expenses):
    stats = dict()
    for e in expenses:
        month = e.created_at.strftime("%Y%m")
        amount = e.amount if e.type_id == 0 else -e.amount
        category = e.category_id
        if month in stats:
            stats[month][category] = stats[month][category] + amount if category in stats[month] else amount
        else:
            stats[month] = {category: amount}
        stats[month]['sum'] = stats[month]['sum'] + amount if 'sum' in stats[month] else amount
    return stats


def dict_id_to_category():
    rs = dict()
    categories = Category.objects.all()
    for category in categories:
        rs[category.id] = category.name
    return rs


