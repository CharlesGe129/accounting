from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        db_table = 'categories'


class Expense(models.Model):
    id = models.AutoField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    type_id = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    amount_fake = models.DecimalField(decimal_places=2, max_digits=10)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    @staticmethod
    def create(name, category_id, amount=0, type_id=0, amount_fake=None, comment=''):
        e = Expense(name=name, amount=amount, amount_fake=amount_fake, type_id=type_id, comment=comment,
                    category=Category.objects.filter(id=category_id)[0])
        e.cal_amount_fake()
        e.save()

    def cal_amount_fake(self):
        if self.category.name == 'Exchange for RMB':
            self.amount_fake = 0
        elif not self.amount_fake:
            self.amount_fake = self.amount * 1.2

    class Meta:
        db_table = 'expenses'
