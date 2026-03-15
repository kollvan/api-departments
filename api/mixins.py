from django.db.models import Model
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnDict

from api.serializers import RecursionSerializer, EmployeeSerializer
from departments.models import Department, Employee


class CustomSerializerMixin:

    def get_recursion_depth(self, request: Request) -> int:
        depth = int(request.query_params.get('depth', 1)) - 1
        if 0 <= depth <= 4:
            return depth
        raise ValidationError('The depth value must be between 1 and 5.')

    def get_recursive_records(self, request: Request, instance: Model) -> ReturnDict:
        children_serializer = RecursionSerializer(
            instance.children.all(),
            many=True,
            context={
                'depth': self.get_recursion_depth(request)
            }
        )
        return children_serializer.data

    def get_employees(self, instance: Department) -> ReturnDict:
        serializer = EmployeeSerializer(
            Employee.objects.filter(department_id=instance.pk),
            many=True
        )
        return serializer.data
