from django.test import TestCase
from .models import Category, Expense


class ExpensesModalTests(TestCase):
    def setUp(self):
        Category.objects.create(name='lunch')
        Category.objects.create(name='Exchange for RMB')
        e = Expense(name='lunch', type_id=0, amount=100,
                    category=Category.objects.filter(name='lunch')[0])
        e.cal_amount_fake()
        e.save()
        e = Expense(name='RMB', type_id=0, amount=100,
                    category=Category.objects.filter(name='Exchange for RMB')[0])
        e.cal_amount_fake()
        e.save()

    def test_amount_fake(self):
        self.assertEqual(Expense.objects.get(name='lunch').amount_fake, 120)
        self.assertEqual(Expense.objects.get(name='RMB').amount_fake, 0)
