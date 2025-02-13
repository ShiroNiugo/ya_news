import pytest
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from news.models import Comment, News
from news.forms import CommentForm

User = get_user_model()


@pytest.mark.django_db
class TestContent:
    def test_news_count_on_home_page(self, client):
        """Количество новостей на главной странице — не более 10."""
        for i in range(15):
            News.objects.create(title=f'Новость {i}', text='Просто текст')
        url = reverse('news:home')
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert 'object_list' in response.context
        object_list = response.context['object_list']
        assert len(object_list) <= 10

    def test_news_order_on_home_page(self, client):
        """Новости отсортированы от самой свежей к самой старой. Свежие новости в начале списка."""
        for i in range(10):
            News.objects.create(title=f'Новость {i}', text='Просто текст')
        url = reverse('news:home')
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert 'object_list' in response.context
        object_list = response.context['object_list']
        dates = [news.date for news in object_list]
        assert dates == sorted(dates, reverse=True)

    def test_comments_order_on_detail_page(self, client, user):
        """Комментарии на странице отдельной новости отсортированы в хронологическом порядке: старые в начале списка, новые — в конце."""
        news = News.objects.create(title='Новость', text='Просто текст')
        for i in range(10):
            Comment.objects.create(news=news, author=user, text=f'Комментарий {i}')
        url = reverse('news:detail', args=[news.id])
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert 'news' in response.context
        news = response.context['news']
        comments = news.comment_set.all()
        dates = [comment.created for comment in comments]
        assert dates == sorted(dates)

    def test_comment_form_on_detail_page_for_anonymous_user(self, client):
        """Анонимному пользователю недоступна форма для отправки комментария на странице отдельной новости."""
        news = News.objects.create(title='Новость', text='Просто текст')
        url = reverse('news:detail', args=[news.id])
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert 'form' not in response.context

    def test_comment_form_on_detail_page_for_authorized_user(self, client, user):
        """Авторизованному пользователю доступна форма для отправки комментария на странице отдельной новости."""
        client.force_login(user)
        news = News.objects.create(title='Новость', text='Просто текст')
        url = reverse('news:detail', args=[news.id])
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert 'form' in response.context
        form = response.context['form']
        assert isinstance(form, CommentForm)