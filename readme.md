# TDD with Django
This repo demos basic TDD for a Django tasks app with CRUD.  

The set-up and example tests are from https://www.youtube.com/watch?v=REhBTwubGzo
### Quick setup 
NB A new virtual environment is recommended.
1. Install the python packages  
`pip install -r requirements.txt`  

2. Run the tests in `task/tests.py` using the following command in the terminal:  
`pytest` to run with pytest, or `python manage.py test`

### Steps to set-up and start using TDD from scratch
1. Create a new project and install Django  
`pip install Django`
  

2. Create the Django project  
`django-admin startproject tddtesting`  
`cd tddtesting`


3. Create the app  
`python manage.py startapp task`


4. Create a test in `task/tests.py`  
```
from django.test import TestCase

from .models import Task


class TaskModelTest(TestCase):
    def test_task_model_exists(self):
        tasks = Task.objects.count()

        self.assertEqual(tasks, 0)
```

5. Run tests, they will fail as the model hasn't been created yet  
`python manage.py test`


6. Create the `test` model in `task/models.py`  
```
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
```
7. Make database migrations and migrate  
`python manage.py makemigrations`  
`python manage.py migrate`


8. Run the tests again, they should pass now  
`python manage.py test`


### Using pytest instead 
Includes benefit of clearer output   

`pip install pytest-django`  
Also recommended for better output:  
`pip install pytest-sugar pytest-clarity`

Create a pytest.ini file in the project root, replacing <app_name> with the name of the app, e.g. tddtesting.  
```
# -- FILE: pytest.ini (or tox.ini)
[pytest]
DJANGO_SETTINGS_MODULE = <app_name>.settings
# -- recommended but optional:
python_files = tests.py test_*.py *_tests.py
```
Run tests with command:  
`pytest -vv` instead of `python manage.py test`  
`-vv` gives verbose output