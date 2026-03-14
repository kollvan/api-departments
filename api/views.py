from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response

from api.serializers import DepartmentSerializer, EmployeeSerializer, create_dynamic_serializer
from departments.models import Department, Employee


# Create your views here.
class DepartmentsViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def retrieve(self, request, *args, **kwargs):
        response_data = {}
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance.parent_id:
            recursion_serializer = create_dynamic_serializer(
                model=Department,
                depth=request.query_params.get('depth', 1)
            )
            children_serializer = recursion_serializer(
                instance=Department.objects.get(pk=instance.parent_id.pk)
            )
            response_data['children'] = children_serializer.data
        if request.query_params.get('include_employees', True):
            _serializer = create_dynamic_serializer(
                model=Employee,
            )
            employee_serializer = _serializer(
                Employee.objects.filter(department_id=instance.pk).order_by('full_name').all(),
                many=True
            )
            response_data['employees'] = employee_serializer.data
        response_data['department'] = serializer.data
        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        mode = request.query_params.get('mode', 'cascade')
        if 'cascade' == mode:
            return super().destroy(request, *args, **kwargs)
        elif mode == 'reassign':
            department_id = request.query_params.get('reassign_to_department_id', None)
            if department_id is not None and department_id.isdigit():
                pk = kwargs.get('pk', None)
                department = get_object_or_404(Department, pk=department_id)
                Employee.objects.filter(department_id=pk).update(department_id=department)
                return super().destroy(request, *args, **kwargs)
            else:
                return Response(
                    data={
                        'detail': 'Required Integer parameter: reassign_to_department_id.'},
                    status=400
                )
        return Response(
            data={'detail': 'Incorrect value for the mode parameter.'},
            status=400
        )


class EmployeeView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
