from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from recipe.serializers import (
    IngredientSerializer,
)


INGREDIEDNTS_URL = reverse('recipe:ingredient-list')


def detait_url(tag_id):
    return reverse('recipe:ingredient-detail', args=[tag_id])


def create_user(email='test@example.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)


class PublicIngredientApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(INGREDIEDNTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='testuser@gmail.com',
            password='passtest123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):

        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIEDNTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        user2 = create_user(email='mmmmmfg@example.com',)
        Ingredient.objects.create(user=user2, name='Salt')
        tag = Ingredient.objects.create(user=self.user, name='Kale')

        res = self.client.get(INGREDIEDNTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_ingredient(self):

        tag = Ingredient.objects.create(user=self.user, name='Salt')

        payload = {'name': 'Kale'}

        res = self.client.patch(detait_url(tag.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_ingredient(self):
        tag = Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.delete(detait_url(tag.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Ingredient.objects.filter(user=self.user)
        self.assertFalse(tags.exists())
