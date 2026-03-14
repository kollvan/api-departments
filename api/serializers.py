from rest_framework import serializers

from departments.models import Department, Employee


class DynamicRecursionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'


def create_dynamic_serializer(**kwargs):
    for key, value in kwargs.items():
        setattr(DynamicRecursionSerializer.Meta, key, value)
    return DynamicRecursionSerializer


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

    def create(self, validated_data):
        department_id = self.context['view'].kwargs.get('pk', None)
        validated_data['department_id'] = Department.objects.get(pk=department_id)
        return super().create(validated_data)
