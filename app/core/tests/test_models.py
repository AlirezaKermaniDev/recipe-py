from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'text@example.com'
        password = 'testpass1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalizr_email_address(self):
        sampleEmail = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, excepted in sampleEmail:
            user = get_user_model().objects.create_user(email, "123456")
            self.assertEqual(user.email, excepted)

    def test_raise_error_when_email_is_blank(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                "",
                "123456"
            )

    def test_create_superuser(self):

        user = get_user_model().objects.create_superuser(
            'text@example.com', "123456",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):

        user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass222',
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Simple food name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Simple recipe description',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass222',
        )

        tag = models.Tag.objects.create(
            user=user,
            name='Vegan',
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredients(self):
        user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass222',
        )

        tag = models.Ingredient.objects.create(
            user=user,
            name='Ingredients name',
        )

        self.assertEqual(str(tag), tag.name)
