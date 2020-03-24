# coding: utf-8
from django.core.management import BaseCommand
from datetime import datetime, timezone
from tasks.models import TodoItem


class Command(BaseCommand):
    help = u"Display not yet completed tasks' dates"


    def add_arguments(self, parser):
        parser.add_argument('--warning-days', dest='warn_days', type=int, default=5)


    def handle(self, *args, **options):
        now = datetime.now(timezone.utc)
        for item in TodoItem.objects.filter(is_completed=False):
            if (now - item.created).days >= options['warn_days']:
                print("Old task:", item, item.created)