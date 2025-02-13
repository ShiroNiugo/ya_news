import pytest
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse


User  = get_user_model()


@pytest.mark.django_db
class TestRoutes:
    def test_home_page_availability(self, client):
        """Главная страница доступна анонимному пользователю."""
        url = reverse('news:home')
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_notes_pages_availability(self, client, user):
        """Аутентифицированному пользователю доступна страница со списком заметок notes/."""
        client.force_login(user)
        url = reverse('news:notes')
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_done_page_availability(self, client, user):
        """Аутентифицированному пользователю доступна страница успешного добавления заметки done/."""
        client.force_login(user)
        url = reverse('news:done')
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_add_page_availability(self, client, user):
        """Аутентифицированному пользователю доступна страница добавления новой заметки add/."""
        client.force_login(user)
        url = reverse('news:add')
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_detail_page_availability(self, client, user, another_user):
        """Страницы отдельной заметки доступны только автору заметки."""
        client.force_login(user)
        url = reverse('news:detail', args=[1])
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

        client.force_login(another_user)
        url = reverse('news:detail', args=[1])
        response = client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_edit_page_availability(self, client, user, another_user):
        """Страницы редактирования заметки доступны только автору заметки."""
        client.force_login(user)
        url = reverse('news:edit', args=[1])
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

        client.force_login(another_user)
        url = reverse('news:edit', args=[1])
        response = client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_page_availability(self, client, user, another_user):
        """Страницы удаления заметки доступны только автору заметки."""
        client.force_login(user)
        url = reverse('news:delete', args=[1])
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

        client.force_login(another_user)
        url = reverse('news:delete', args=[1])
        response = client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_redirect_for_anonymous_client(self, client):
        """При попытке перейти на страницу списка заметок, страницу успешного добавления записи, страницу добавления заметки, отдельной заметки, редактирования или удаления заметки анонимный пользователь перенаправляется на страницу логина."""
        login_url = reverse('users:login')
        for name in ('news:notes', 'news:done', 'news:add', 'news:detail', 'news:edit', 'news:delete'):
            url = reverse(name, args=[1])
            response = client.get(url)
            redirect_url = f'{login_url}?next={url}'
            assert response.status_code == HTTPStatus.FOUND
            assert response.url == redirect_url

    def test_auth_pages_availability(self, client, user):
        """Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям."""
        for name in ('users:signup', 'users:login', 'users:logout'):
            url = reverse(name)
            response = client.get(url)
            assert response.status_code == HTTPStatus.OK

            client.force_login(user)
            response = client.get(url)
            assert response.status_code == HTTPStatus.OK