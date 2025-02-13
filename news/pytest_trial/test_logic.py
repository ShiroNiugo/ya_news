import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from news.models import Comment, News
from news.forms import BAD_WORDS, WARNING


User  = get_user_model()


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client):
    news = News.objects.create(title='Заголовок', text='Текст')
    url = reverse('news:detail', args=(news.id,))
    form_data = {'text': 'Текст комментария'}
    response = client.post(url, data=form_data)
    assert response.status_code == 302
    assert Comment.objects.count() == 0

@pytest.mark.django_db
def test_user_can_create_comment(client, user):
    news = News.objects.create(title='Заголовок', text='Текст')
    url = reverse('news:detail', args=(news.id,))
    form_data = {'text': 'Текст комментария'}
    client.force_login(user)
    response = client.post(url, data=form_data)
    assert response.status_code == 302
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == 'Текст комментария'
    assert comment.news == news
    assert comment.author == user

@pytest.mark.django_db
def test_user_cant_use_bad_words(client, user):
    news = News.objects.create(title='Заголовок', text='Текст')
    url = reverse('news:detail', args=(news.id,))
    form_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    client.force_login(user)
    response = client.post(url, data=form_data)
    assert response.status_code == 200
    assert WARNING in response.context['form'].errors['text']
    assert Comment.objects.count() == 0

@pytest.mark.django_db
def test_user_can_edit_comment(client, user):
    news = News.objects.create(title='Заголовок', text='Текст')
    comment = Comment.objects.create(news=news, author=user, text='Текст комментария')
    url = reverse('news:edit', args=(comment.id,))
    form_data = {'text': 'Обновлённый комментарий'}
    client.force_login(user)
    response = client.post(url, data=form_data)
    assert response.status_code == 302
    comment.refresh_from_db()
    assert comment.text == 'Обновлённый комментарий'

@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(client, user, another_user):
    news = News.objects.create(title='Заголовок', text='Текст')
    comment = Comment.objects.create(news=news, author=another_user, text='Текст комментария')
    url = reverse('news:edit', args=(comment.id,))
    form_data = {'text': 'Обновлённый комментарий'}
    client.force_login(user)
    response = client.post(url, data=form_data)
    assert response.status_code == 404
    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'

@pytest.mark.django_db
def test_user_can_delete_comment(client, user):
    news = News.objects.create(title='Заголовок', text='Текст')
    comment = Comment.objects.create(news=news, author=user, text='Текст комментария')
    url = reverse('news:delete', args=(comment.id,))
    client.force_login(user)
    response = client.delete(url)
    assert response.status_code == 302
    assert Comment.objects.count() == 0

@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(client, user, another_user):
    news = News.objects.create(title='Заголовок', text='Текст')
    comment = Comment.objects.create(news=news, author=another_user, text='Текст комментария')
    url = reverse('news:delete', args=(comment.id,))
    client.force_login(user)
    response = client.delete(url)
    assert response.status_code == 404
    assert Comment.objects.count() == 1

@pytest.fixture
def user():
    return User.objects.create(username='user')

@pytest.fixture
def another_user():
    return User.objects.create(username='another_user')