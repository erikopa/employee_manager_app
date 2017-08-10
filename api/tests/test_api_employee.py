# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework import status

from rest_framework.test import APIClient
from django.core.urlresolvers import reverse

from api.models import Employee


class EmployeeCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.model = {'name': 'Eriko Morais', 'email': 'teste@teste.com', 'department': 'TI'}

    def test_create_employee_with_success(self):
        response = self.client.post(
            reverse('list_all_and_create'),
            self.model,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_an_employee_with_wrong_name(self):
        self.model['name'] = 't'
        response = self.client.post(
            reverse('list_all_and_create'),
            self.model,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_an_employee_with_wrong_email(self):
        self.model['email'] = 'teste@te'
        response = self.client.post(
            reverse('list_all_and_create'),
            self.model,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["Enter a valid email address."]})

    def test_creating_an_employee_without_name(self):
        self.model['name'] = ''
        response = self.client.post(
            reverse('list_all_and_create'),
            self.model,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"name": ["This field may not be blank."]})

    def test_creating_an_employee_without_email(self):
        self.model['email'] = ''
        response = self.client.post(
            reverse('list_all_and_create'),
            self.model,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["This field may not be blank."]})

    def test_creating_an_employee_without_department(self):
        self.model['department'] = ''
        response = self.client.post(
            reverse('list_all_and_create'),
            self.model,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"department": ["This field may not be blank."]})

    def test_creating_an_employee_without_email_name_and_department(self):
        self.model['name'] = ''
        self.model['email'] = ''
        self.model['department'] = ''
        response = self.client.post(
            reverse('list_all_and_create'),
            self.model,
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"name": ["This field may not be blank."],
                                           "email": ["This field may not be blank."],
                                           "department": ["This field may not be blank."]})

    def test_creating_am_employee_with_email_already_exists(self):
        first_response = self.client.post(
            reverse('list_all_and_create'),
            self.model,
            format="json")
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

        second_response = self.client.post(
            reverse('list_all_and_create'),
            self.model,
            format="json")

        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(second_response.json(), {'email': ['This field must be unique.']})


class EmployeeUpdateTestCase(TestCase):
    def setUp(self):
        self.data_employees = [
            {'name': 'Joao Jose', 'email': 'joao@test.com', 'department': 'TI'},
            {'name': 'Vinicius Morais', 'email': 'vini@test.com', 'department': 'TI'}
        ]
        self.employees = Employee.objects.bulk_create([Employee(**x) for x in self.data_employees])
        self.client = APIClient()

    def test_update_employee_with_success(self):
        update_employee = self.data_employees[1]
        update_employee['name'] = 'Vinicius'
        update_employee['email'] = 'vini2@test.com'

        response = self.client.put(
            reverse('detail_update_destroy', kwargs={'pk': 1}),
            update_employee, format='json'
        )

        updated_employee = Employee.objects.get(id=1)

        self.assertEqual(updated_employee.name, update_employee['name'])
        self.assertEqual(updated_employee.email, update_employee['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_employee_with_wrong_email(self):
        update_employee = self.data_employees[1]
        update_employee['email'] = 'joao@test'

        response = self.client.put(
            reverse('detail_update_destroy', kwargs={'pk': 1}),
            update_employee, format='json'
        )

        updated_employee = Employee.objects.get(id=1)

        self.assertNotEqual(updated_employee.email, update_employee['email'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_employee_with_wrong_name(self):
        update_employee = self.data_employees[1]
        update_employee['name'] = 'j'

        response = self.client.put(
            reverse('detail_update_destroy', kwargs={'pk': 1}),
            update_employee, format='json'
        )

        updated_employee = Employee.objects.get(id=1)

        self.assertNotEqual(updated_employee.name, update_employee['name'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_employee_with_wrong_id(self):
        update_employee = self.data_employees[1]

        response = self.client.put(
            reverse('detail_update_destroy', kwargs={'pk': 10}),
            update_employee, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': 'Not found.'})


class EmployeeDeleteTestCase(TestCase):
    def setUp(self):
        self.data_employees = [
            {'name': 'Joao Jose', 'email': 'joao@test.com', 'department': 'TI'},
            {'name': 'Vinicius Morais', 'email': 'vini@test.com', 'department': 'TI'}
        ]
        self.employees = Employee.objects.bulk_create([Employee(**x) for x in self.data_employees])
        self.client = APIClient()

    def test_deleting_employee_with_success(self):
        response = self.client.delete(reverse('detail_update_destroy', kwargs={'pk': 1}), format='json')

        employee_deleted = Employee.objects.filter(email=self.data_employees[0]).all()

        self.assertEqual(len(employee_deleted), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleting_employee_with_id_does_not_exist(self):
        response = self.client.delete(reverse('detail_update_destroy', kwargs={'pk': len(self.data_employees) + 10}),
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmployeeListTestCase(TestCase):
    def setUp(self):
        self.data_employees = [
            {'name': 'Joao Jose', 'email': 'joao@test.com', 'department': 'TI'},
            {'name': 'Vinicius Morais', 'email': 'vini@test.com.br', 'department': 'TI'}
        ]
        self.employees = Employee.objects.bulk_create([Employee(**x) for x in self.data_employees])
        self.client = APIClient()

    def test_listing_all_employees(self):
        response = self.client.get(reverse('list_all_and_create'))

        self.assertEqual(len(response.json()), len(self.data_employees))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listing_one_employee(self):
        employee_index = len(self.data_employees)
        response = self.client.get(reverse('detail_update_destroy', kwargs={'pk': employee_index}))

        self.assertEqual(response.json().get('name'), self.data_employees[employee_index - 1].get('name'))
        self.assertEqual(response.json().get('email'), self.data_employees[employee_index - 1].get('email'))
        self.assertEqual(response.json().get('department'), self.data_employees[employee_index - 1].get('department'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_listing_one_employee_that_does_not_exist(self):
        employee_index = len(self.data_employees) + 1
        response = self.client.get(reverse('detail_update_destroy', kwargs={'pk': employee_index}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': 'Not found.'})
