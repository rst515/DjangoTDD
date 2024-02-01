from django.test import TestCase

from .forms import NewTaskForm, UpdateTaskForm
from .models import Task


class TaskModelTest(TestCase):
    def test_task_model_exists(self):
        tasks = Task.objects.count()

        self.assertEqual(tasks, 0)

    def test_model_has_string_representation(self):
        task = Task.objects.create(title="First task")

        self.assertEqual(str(task), task.title)


class IndexPageTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="First task")

    def test_index_page_returns_200(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'task/index.html')
        self.assertEqual(response.status_code, 200)

    def test_index_page_has_tasks(self):
        response = self.client.get('/')

        self.assertContains(response, self.task.title)


class DetailPageTest(TestCase):
    def setUp(self):
        self.task1 = Task.objects.create(title="First task", description="First task description")
        self.task2 = Task.objects.create(title="Second task", description="Second task description")

    def test_detail_page_returns_200(self):
        response = self.client.get(f'/{self.task1.id}/')

        self.assertTemplateUsed(response, 'task/detail.html')
        self.assertEqual(response.status_code, 200)

    def test_detail_page_has_correct_content(self):
        response = self.client.get(f'/{self.task1.id}/')

        self.assertContains(response, self.task1.title)
        self.assertContains(response, self.task1.description)

        self.assertNotContains(response, self.task2.title)
        self.assertNotContains(response, self.task2.description)


class NewPageTest(TestCase):
    def setUp(self):
        self.form = NewTaskForm

    def test_new_page_returns_200(self):
        response = self.client.get('/new/')

        self.assertTemplateUsed(response, 'task/new.html')
        self.assertEqual(response.status_code, 200)

    def test_form_is_valid(self):
        self.assertTrue(issubclass(self.form, NewTaskForm))
        self.assertTrue('title' in self.form.Meta.fields)
        self.assertTrue('description' in self.form.Meta.fields)

        form = self.form({
            'title': 'Title',
            'description': 'A description',
        })

        self.assertTrue(form.is_valid())

    def test_new_page_form_rendering(self):
        response = self.client.get('/new/')

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')

        # test invalid form
        invalid_data = {
            'title': '',
            'description': 'A description',
        }
        response = self.client.post('/new/', data=invalid_data)

        self.assertContains(response, '<ul class="errorlist">')
        self.assertContains(response, 'This field is required.')

        # test valid form is saved and page redirects
        valid_data = {
            'title': 'Title',
            'description': 'A description',
        }
        response = self.client.post('/new/', data=valid_data)

        self.assertRedirects(response, expected_url='/')
        self.assertEqual(Task.objects.count(), 1)


class UpdatePageTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='First task')
        self.form = UpdateTaskForm

    def test_update_page_returns_200(self):
        response = self.client.get(f'/{self.task.id}/update/')

        self.assertTemplateUsed(response, 'task/update.html')
        self.assertEqual(response.status_code, 200)

    def test_form_is_valid(self):
        self.assertTrue(issubclass(self.form, UpdateTaskForm))
        self.assertTrue('title' in self.form.Meta.fields)
        self.assertTrue('description' in self.form.Meta.fields)

        form = self.form({
            'title': 'Title',
            'description': 'A description',
        },
            instance=self.task
        )

        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(self.task.title, 'Title')

    def test_invalid_form(self):
        form = self.form({
            'title': '',
            'description': 'A description',
        },
            instance=self.task
        )

        self.assertFalse(form.is_valid())

    def test_update_page_form_rendering(self):
        response = self.client.get(f'/{self.task.id}/update/')

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')

        # test invalid form
        invalid_data = {
            'id': self.task.id,
            'title': '',
            'description': 'A description',
        }
        response = self.client.post(f'/{self.task.id}/update/', data=invalid_data, instance=self.task)

        self.assertContains(response, '<ul class="errorlist">')
        self.assertContains(response, 'This field is required.')

        # test valid form is saved and page redirects
        valid_data = {
            'title': 'Title',
            'description': 'A description',
        }
        response = self.client.post(f'/{self.task.id}/update/', data=valid_data, instance=self.task)

        self.assertRedirects(response, expected_url='/')
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Title')


class DeletePageTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='First task')

    def test_delete_page_success(self):
        self.assertEqual(Task.objects.count(), 1)

        response = self.client.get(f'/{self.task.id}/delete/')

        self.assertRedirects(response, expected_url='/')
        self.assertEqual(Task.objects.count(), 0)
