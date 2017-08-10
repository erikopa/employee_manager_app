# -*- coding: utf-8 -*-

from rest_framework import serializers
from api.models import Employee
from rest_framework.validators import UniqueValidator


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    name = serializers.CharField(min_length=3, max_length=200)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Employee.objects.all())])
    department = serializers.CharField(min_length=2, max_length=200)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Employee
        fields = ('name', 'email', 'department')
