from rest_framework import generics

# Create your views here.
from api.models import Employee
from api.serializers import EmployeeSerializer


class ListAndCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class RetriveAndUpdateAndDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
