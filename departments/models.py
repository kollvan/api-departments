from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_lenght=200, null=False, blank=False)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Employee(models.Model):
    department_id = models.ForeignKey(to=Department, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    position = models.CharField(max_length=200, null=False, blank=False)
    hired_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
