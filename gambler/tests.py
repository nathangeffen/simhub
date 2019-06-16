import time
import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from scheduler import settings
from scheduler import views


class JobTestCase(TestCase):
    clients = []

    def setUp(self):
        settings.MAX_JOBS_WAITING = 3
        settings.ZOMBIE_REMOVAL_QUEUE_SIZE = 1
        settings.NO_PING_TIMEOUT = 15
        self.clients = []
        for i in range(8):
            self.clients.append(Client())

    def test_queues(self):
        for c in self.clients:
            response = c.get(reverse("gambler:gambler_form"))
            self.assertEqual(response.status_code, 200)
            response = c.post(reverse("gambler:gambler_form"), {
                "start_amount": 10,
                "num_tests": 50,
                "num_gambles": 1000,
                "num_players": 10
            })
        self.assertEqual(len(views.JobView()._running), 2)
        self.assertEqual(len(views.JobView()._waiting), 3)
        time.sleep(1)
        self.assertEqual(len(views.JobView()._running), 0)
        self.assertEqual(len(views.JobView()._waiting), 0)

    def test_timeout(self):
        settings.TIMEOUT = 1
        for c in self.clients:
            response = c.get(reverse("gambler:gambler_form"))
            self.assertEqual(response.status_code, 200)
            response = c.post(reverse("gambler:gambler_form"), {
                "start_amount": 10,
                "num_tests": 5000,
                "num_gambles": 100000,
                "num_players": 10
            })
        self.assertEqual(len(views.JobView()._running), 2)
        self.assertEqual(len(views.JobView()._waiting), 3)
        time.sleep(3)
        self.assertEqual(len(views.JobView()._running), 0)
        self.assertEqual(len(views.JobView()._waiting), 0)

    def test_zombies(self):
        self.assertEqual(len(views.JobView()._job_queue) > 0, True)
        settings.NO_PING_TIMEOUT = 1
        views.JobView().remove_zombies()
        self.assertEqual(len(views.JobView()._job_queue), 0)

    def test_fetch(self):
        settings.TIMEOUT = 10
        settings.NO_PING_TIMEOUT = 15
        c = self.clients[0]
        response = c.get(reverse("gambler:gambler_form"))
        self.assertEqual(response.status_code, 200)
        response = c.post(reverse("gambler:gambler_form"), {
            "start_amount": 10,
            "num_tests": 500,
            "num_gambles": 1000,
            "num_players": 10
        })
        time.sleep(2)
        response = c.get(reverse("gambler:gambler_fetch"))
        self.assertEqual(response.status_code, 200)
        dict = json.loads(response.content)
        self.assertEqual('lines' in dict and len(dict['lines']) > 0, True)
