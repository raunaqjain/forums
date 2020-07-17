from django.test import TestCase
from django import forms
from ..templatetags.form_tags import field_type, input_class

class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ('name', 'password')

class FieldTypeTests(TestCase):
    def test_field_widget_type(self):
        form = ExampleForm()
        self.assertEquals(field_type(form['name']), 'TextInput')
        self.assertEquals(field_type(form['password']), 'PasswordInput')

class InputClassTests(TestCase):
    def test_unbound_field_initial_state(self):
        form = ExampleForm()
        self.assertEquals(input_class(form['name']), 'form-control ')
    
    def test_valid_bound_field(self):
        form = ExampleForm({'name': "raunaq", 'password': "213"})
        self.assertEquals(input_class(form['name']), 'form-control is_valid')
        self.assertEquals(input_class(form['password']), 'form-control ')

    def test_invalid_bound_field(self):
        form = ExampleForm({'name': '', 'password': '213'})
        self.assertEquals(input_class(form['name']), 'form-control is_invalid')


    