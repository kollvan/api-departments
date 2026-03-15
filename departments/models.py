from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=200, null=False, blank=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None,
                                  related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}: {self.created_at}'


class Employee(models.Model):
    department_id = models.ForeignKey(to=Department, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    position = models.CharField(max_length=200, null=False, blank=False)
    hired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name}: {self.position}'
