from django.db import models


class Categories(models.Model):
    id = models.AutoField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Expenses(models.Model):
    id = models.AutoField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    type_id = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    category_id = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
