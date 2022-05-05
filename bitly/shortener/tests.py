from django.test import TestCase
from django.urls import reverse

from .models import Shortener


class ShortenerTests(TestCase):
    TEST_URL = 'https://www.google.com'

    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_new_url(self):
        response = self.client.post(reverse('home'), {'url': self.TEST_URL})
        self.assertEquals(response.status_code, 200)
        self.assertIn('new_url', response.context)
        self.assertEqual(response.context['existing_url'], self.TEST_URL)
        self.assertEqual(response.context['times_followed'], 0)
        self.assertFalse(response.context['errors'])

    def test_existing_url(self):
        existing = Shortener.objects.create(url=self.TEST_URL)
        response = self.client.post(reverse('home'), {'url': self.TEST_URL})
        self.assertEquals(response.status_code, 200)
        self.assertIn(existing.code, response.context['new_url'])
        self.assertEqual(response.context['existing_url'], self.TEST_URL)
        self.assertEqual(response.context['times_followed'], 0)
        self.assertFalse(response.context['errors'])
        response = self.client.get(response.context['new_url'])
        self.assertRedirects(response, self.TEST_URL, status_code=302, fetch_redirect_response=False)

    def test_counter_increment(self):
        existing = Shortener.objects.create(url=self.TEST_URL)
        self.assertEqual(existing.times_followed, 0)
        response = self.client.get(reverse('redirect', kwargs={'code': existing.code}))
        self.assertRedirects(response, self.TEST_URL, status_code=302, fetch_redirect_response=False)
        changed = Shortener.objects.get(url=self.TEST_URL)
        self.assertEqual(changed.times_followed, 1)
        response = self.client.post(reverse('home'), {'url': self.TEST_URL})
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.context['times_followed'], 1)
