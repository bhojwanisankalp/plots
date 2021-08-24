from django.db import models

# Create your models here.

class Data(models.Model):
    obs_no = models.IntegerField(default=0)
    date_time = models.DateTimeField(null=True)
    dept_name = models.CharField(max_length=50, null=True)
    entry_pay = models.DecimalField(decimal_places=2, max_digits=3)
    sp = models.DecimalField(decimal_places=2, max_digits=3)
    pay = models.DecimalField(decimal_places=2 ,max_digits=3)
    iv = models.DecimalField(decimal_places=2, max_digits=5)
    g1 = models.DecimalField(decimal_places=2, max_digits=5)
    g2 = models.DecimalField(decimal_places=2, max_digits=5)
    g3 = models.DecimalField(decimal_places=2, max_digits=5)
    g4 = models.DecimalField(decimal_places=2, max_digits=5)
    money = models.DecimalField(decimal_places=2, max_digits=5)
    val_int = models.DecimalField(decimal_places=2, max_digits=3)
    val_tm = models.DecimalField(decimal_places=2, max_digits=3)
    net_pay = models.DecimalField(decimal_places=2, max_digits=3)
    entry_no_entry_date_obs_no = models.CharField(max_length=50)