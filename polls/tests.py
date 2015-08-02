import datetime
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase
from polls.models import Poll

class PollMethodTests(TestCase):

    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)
        
    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return False for polls whose pub_date
        is older than 1 day
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)
            
    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() should return True for polls whose pub_date
        is within the last day
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)
    
class PollViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        """
        If no polls exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_a_past_poll(self):
        """
        Polls with a pub_date in the past should be displayed on the index page.
        """
        Poll.objects.create(question="Past poll.",pub_date=timezone.now() + datetime.timedelta(days=-30))
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )

    def test_index_view_with_a_future_poll(self):
        """
        Polls with a pub_date in the future should not be displayed on the
        index page.
        """
        Poll.objects.create(question="Future poll.",pub_date=timezone.now() + datetime.timedelta(days=30))
        response = self.client.get(reverse('index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        """
        Even if both past and future polls exist, only past polls should be
        displayed.
        """
        Poll.objects.create(question="Past poll.",pub_date=timezone.now() + datetime.timedelta(days=-30))
        Poll.objects.create(question="Future poll.",pub_date=timezone.now() + datetime.timedelta(days=30))
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past poll.>']
        )

    def test_index_view_with_two_past_polls(self):
        """
        The polls index page may display multiple polls.
        """
        Poll.objects.create(question="Past poll 1.",pub_date=timezone.now() + datetime.timedelta(days=-30))
        Poll.objects.create(question="Past poll 2.",pub_date=timezone.now() + datetime.timedelta(days=-5))
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
             ['<Poll: Past poll 2.>', '<Poll: Past poll 1.>']
        )

class PollIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        """
        The detail view of a poll with a pub_date in the future should
        return a 404 not found.
        """
        future_poll = Poll.objects.create(question="Future poll.",pub_date=timezone.now() + datetime.timedelta(days=5))
        response = self.client.get(reverse('detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        """
        The detail view of a poll with a pub_date in the past should display
        the poll's question.
        """
        past_poll = Poll.objects.create(question="Past poll.",pub_date=timezone.now() + datetime.timedelta(days=-5))
        response = self.client.get(reverse('detail', args=(past_poll.id,)))
        self.assertContains(response, past_poll.question, status_code=200)