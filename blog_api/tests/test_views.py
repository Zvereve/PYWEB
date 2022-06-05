import unittest

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from blog.models import Note


class TestNoteListCreateAPIView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Создаем двух пользователей и  по две записи"""
        user1 = User.objects.create(username="test1@test.ru", password="test1password")
        user2 = User.objects.create(username="test2@test.ru", password="test2password")

        Note.objects.bulk_create([
            Note(title="test1", author=user1, public=False),
            Note(title="test2", author=user1, public=True),
            Note(title="test3", author=user2, public=False),
            Note(title="test4", author=user2, public=True),
        ])

        cls.user1 = user1
        cls.user2 = user2

    def test_list_objects(self):
        """Проверка на чтение Только своих записей"""
        self.client.force_login(user=self.user1)
        url = "/notes/"
        resp = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        response_data = resp.data
        self.assertEqual(3, len(response_data))

    def test_view_note(self):
        """Проверка на чтение одной своей записи"""
        self.client.force_login(user=self.user1)
        url = "/notes/1/"
        resp = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        response_data = resp.data
        self.assertEqual(9, len(response_data))

    def test_view_note_old_public(self):
        """Проверка на чтение одной чужой публичной записи"""
        self.client.force_login(user=self.user1)
        url = "/notes/4/"
        resp = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, resp.status_code)

        response_data = resp.data
        self.assertEqual(9, len(response_data))

    def test_view_note_old_not_public(self):
        """Проверка на чтение одной чужой не публичной записи"""
        self.client.force_login(user=self.user1)
        url = "/notes/3/"
        resp = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)

#   def test_empty_list_objects(self):
#        self.client.force_login(user=self.user1)
#        url = "/notes/"
#        resp = self.client.get(url)

#        expected_status_code = status.HTTP_200_OK
#        self.assertEqual(expected_status_code, resp.status_code)

#        response_data = resp.data
#        expected_data = []
#        self.assertEqual(expected_data, response_data)

    def test_create_objects(self):
        """Тест на создание запись"""
        self.client.force_login(user=self.user1)
        new_title = "test_title"
        data = {
            "title": new_title
        }
        url = "/notes/"
        resp = self.client.post(url, data=data,)
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)

        Note.objects.get(title=new_title)  # self.assertTrue(Note.objects.exists(title=new_title))

    def test_put_update_user_old(self):
        """Тест на изменение чужой записи"""
        self.client.force_login(user=self.user1)
        note_other = 4
        url = f"/notes/{note_other}/"
        resp = self.client.put(url, data={"title": "New_title"},)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_update(self):
        """Тест на изменение своей записи"""
        self.client.force_login(user=self.user1)
        note_other = 1
        url = f"/notes/{note_other}/"
        resp = self.client.put(url, data={"title": "New_title"}, )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delite(self):
        """Тест на удаление своей записи"""
        self.client.force_login(user=self.user1)
        note_other = 1
        url = f"/notes/{note_other}/"
        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delite_user_old(self):
        """Тест на удаление чужой записи"""
        self.client.force_login(user=self.user1)
        note_other = 3
        url = f"/notes/{note_other}/"
        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

