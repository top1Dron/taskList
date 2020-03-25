#  coding: utf-8
from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = f"Display top 25 users with most count of tasks"

    def handle(self, *args, **kwargs):
        maxCount = {}
        counter = 0
        for u in User.objects.all():
            for t in u.tasks.all():
                try:
                    maxCount[u] += 1
                except:
                    maxCount[u] = 1
                counter += 1
        maxCount = sorted(maxCount.items(), key=lambda item: item[1], reverse=True)

        i = 0
        for k, v in maxCount:
            print(f"{k} - {v}")
            i += 1
            if i >= 24:
                break

        print(f'Total tasks in db = {counter}')

        key, value = maxCount[4]
        print(f'№5 user in db with most count of tasks: {key} - {value}')

        maxCount = {}
        counter = 0
        for u in User.objects.all():
            for t in u.tasks.filter(is_completed=False):
                try:
                    maxCount[u] += 1
                except:
                    maxCount[u] = 1
        maxCount = sorted(maxCount.items(), key=lambda  item: item[1])
        for k, v in maxCount:
            if v >= 20:
                break
            else:
                print(f"{k} - {v}")
        key, value = maxCount[::-1][1]
        print(f'The second user by not completed tasks: {key} - {value}')