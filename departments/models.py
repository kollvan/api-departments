from django.core.exceptions import ValidationError
from django.db import models, connection
from django.core.validators import MinLengthValidator

from departments.exceptions import CycleValidationError


# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=200, null=False, blank=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None,
                                  related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.name:
            self.name = self.name.strip()

        if not self.name:
            raise ValidationError({'name': 'Name cannot be empty or only whitespace'})

        if len(self.name) < 1 or len(self.name) > 200:
            raise ValidationError({'name': 'Name must be between 1 and 200 characters'})

        is_not_unique = Department.objects.filter(name=self.name, parent_id=self.parent_id).exists()
        if is_not_unique:
            raise ValidationError({
                'name': f'Department with name "{self.name}" already exists under this parent'
            })
        if self.pk and self.parent_id and self.has_cycle(self.pk, self.parent_id.pk):
            raise CycleValidationError('Loop error: Collision detected in parent_id field.')

    def has_cycle(self, dept_id: int, new_parent_id: int) -> bool:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT check_department_cycle(%s, %s)",
                [dept_id, new_parent_id]
            )
            result = cursor.fetchone()
            return result[0] if result else None

    def __str__(self):
        return f'{self.name}: {self.created_at}'


class Employee(models.Model):
    department_id = models.ForeignKey(to=Department, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=False, blank=False, validators=[MinLengthValidator(1)])
    position = models.CharField(max_length=200, null=False, blank=False, validators=[MinLengthValidator(1)])
    hired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name}: {self.position}'
