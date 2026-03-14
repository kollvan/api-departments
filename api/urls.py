from django.urls import path

from api.views import DepartmentsViewSet, EmployeeView

app_name = 'api'
urlpatterns = [
    path('departments/', DepartmentsViewSet.as_view({'post': 'create'})),
    path('departments/<int:pk>/',
         DepartmentsViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('departments/<int:pk>/employees', EmployeeView.as_view()),
]

