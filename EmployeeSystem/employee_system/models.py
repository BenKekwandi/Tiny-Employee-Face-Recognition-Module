from django.db import models
from django.conf import settings
from random import randint

class EmployeeModel(models.Model):
    id=models.AutoField(primary_key=True)
    employee_no=models.CharField(max_length=10)
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
    profile_picture=models.ImageField()
    class Meta:
        db_table='employees'
        app_label='employee_system'
    def save(self):
        if not self.employee_no:
            no = randint(1000000,9999999)
            counter=EmployeeModel.objects.filter(employee_no=no).count()
            if counter==0:
                self.employee_no = no
                super(EmployeeModel, self).save()
            else:
                self.save()  
        return self.id
class PictureModel(models.Model):
    id=models.AutoField(primary_key=True)
    location=models.CharField(max_length=500000)
    name=models.CharField(max_length=2500)
    employee_id=models.IntegerField()
    class Meta:
        db_table='employee_pictures'
        app_label='employee_system'
