# -*- coding: utf-8 -*-
from datetime import datetime
from django.test import TestCase
from api.models import Employee


class EmployeeModelTest(TestCase):

    def setUp(self):
        self.obj = Employee(
            name='Eriko Verissimo',
            email='teste@teste.com.br',
            department='TI'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Employee.objects.exists())

    def test_created_at(self):
        """Employee must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_modify_at(self):
        """Employee must have an auto modify_at attr."""
        self.obj.name = 'Eriko'
        self.obj.save()
        self.assertTrue(self.obj.created_at < self.obj.modified_at)

    def test_str(self):
        self.assertEqual('Eriko Verissimo', str(self.obj))
