from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from api.exceptions import IncorrectReassignException
from api.mixins import CustomSerializerMixin
from api.serializers import DepartmentSerializer, EmployeeSerializer
from departments.models import Department, Employee


# Create your views here.
class DepartmentsViewSet(CustomSerializerMixin, viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def retrieve(self, request: Request, *args, **kwargs):
        response_data = {}
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        try:
            response_data['children'] = self.get_recursive_records(request, instance)
        except ValidationError as e:
            return Response({'detail': e.args[0]}, status=400)

        is_include = request.query_params.get('include_employees', 'true').lower()
        if is_include == 'true':
            response_data['employees'] = self.get_employees(instance)
        response_data['department'] = serializer.data
        return Response(response_data)

    def destroy(self, request: Request, *args, **kwargs):
        mode = request.query_params.get('mode', 'cascade')
        if mode == 'reassign':
            try:
                self.reassign_employees(request, *args, **kwargs)
            except IncorrectReassignException as e:
                return Response(
                    data={
                        'detail': e.args[0]},
                    status=400
                )
        else:
            return Response(
                data={'detail': 'Incorrect value for the mode parameter.'},
                status=400
            )
        return super().destroy(request, *args, **kwargs)

    def reassign_employees(self, request: Request, *args, **kwargs):
        department_id = request.query_params.get('reassign_to_department_id', None)
        if department_id is not None and department_id.isdigit():
            pk = kwargs.get('pk', None)
            department = get_object_or_404(Department, pk=department_id)
            Employee.objects.filter(department_id=pk).update(department_id=department)
            return super().destroy(request, *args, **kwargs)
        else:
            raise IncorrectReassignException('Required Integer parameter: reassign_to_department_id.')


class EmployeeView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
