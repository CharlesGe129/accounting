from django.test import TestCase
from django.urls import reverse
from .models import Category, Expense
import datetime


class ExpensesModalTests(TestCase):
    def setUp(self):
        Category.objects.create(id=1, name='lunch')
        Category.objects.create(id=2, name='Exchange for RMB')
        Expense.create('lunch', 1, amount=100)
        Expense.create('RMB', 2, amount=100)

    def test_amount_fake(self):
        self.assertEqual(Expense.objects.get(name='lunch').amount_fake, 120)
        self.assertEqual(Expense.objects.get(name='RMB').amount_fake, 0)


class ExpenseViewTests(TestCase):
    def setUp(self):
        Category.objects.create(id=1, name='food')
        Category.objects.create(id=2, name='supper')
        Category.objects.create(id=3, name='salary')
        Expense.create('apple', 1, amount=5)
        Expense.create('lunch', 2, amount=15)
        Expense.create('salary', 3, amount=100, type_id=1)
        Expense.create('salary', 3, amount=50, type_id=1)

    def test_index_sum_avg(self):
        response = self.client.get(reverse('expenses:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sum_ex'], 20)
        self.assertEqual(response.context['sum_in'], 150)
        self.assertEqual(float(response.context['avg_ex']), round(20 / int(datetime.datetime.today().strftime('%d')), 2))
        self.assertEqual(float(response.context['avg_in']), round(150 / int(datetime.datetime.today().strftime('%d')), 2))

    def test_index_category_filter(self):
        response = self.client.get(reverse('expenses:index'), {'cat': '1, 3'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['sum_ex'], 15)
        self.assertEqual(response.context['sum_in'], 0)

    def test_index_post(self):
        def test_new():
            self.assertEqual(len(Expense.objects.filter(name='yogurt')), 0, 'Create expense initialization failed!!')
            self.client.post(reverse('expenses:new'), {'name': 'yogurt', 'type_id': 0, 'amount': '4',
                                                       'amount_fake': '', 'comment': '', 'category_id': 1})
            self.assertEqual(len(Expense.objects.filter(name='yogurt')), 1, 'Create expense failed!')

        def test_edit():
            url = reverse('expenses:edit', args=(Expense.objects.get(name='yogurt').id, ))
            self.client.post(url, {'name': 'yogurt', 'type_id': 0, 'amount': '3', 'amount_fake': '',
                                   'comment': '', 'category_id': 1})
            self.assertEqual(Expense.objects.get(name='yogurt').amount, 3, 'Edit expense failed!')

        test_new()
        test_edit()

