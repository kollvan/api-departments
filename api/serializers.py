from typing import Any

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict

from departments.models import Department, Employee


class RecursionSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'created_at', 'children']

    def get_children(self, obj: Department) -> ReturnDict:
        depth = self.context.get('depth', 1)
        if depth <= 0 or not obj.children.exists():
            return []

        serializer = RecursionSerializer(
            obj.children.all(),
            many=True,
            context={**self.context, 'depth': depth - 1}
        )
        return serializer.data


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['pk', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['pk', 'department_id', 'created_at']

    def create(self, validated_data: dict) -> Any:
        department_id = self.context['view'].kwargs.get('pk', None)
        validated_data['department_id'] = get_object_or_404(Department, pk=department_id)
        return super().create(validated_data)
