import os
import csv
from itertools import islice

from AdjustHome import settings
from django.core.management.base import BaseCommand, CommandError
from metrics_api.models import Metric


class Command(BaseCommand):
    help = 'Migrate data in Metric Model'

    def handle(self, *args, **options):
        try:
            with open(os.path.join(settings.BASE_DIR, 'data/dataset.csv'), 'r') as csv_file:
                data_reader = csv.reader(csv_file, delimiter=',')
                batch_size = 10000
                next(data_reader)
                while True:
                    batch = [
                        Metric(
                            date=row[0], channel=row[1], country=row[2], os=row[3],
                            impressions=row[4], clicks=row[5], installs=row[6], spend=row[7], revenue=row[8]
                        )
                        for row in islice(data_reader, batch_size)
                    ]
                    if not batch:
                        break
                    Metric.objects.bulk_create(batch, batch_size)
            metric_count = Metric.objects.count()
        except Exception:
            raise CommandError('Exception occurred while creating objects.')
        self.stdout.write(self.style.SUCCESS('Successfully executed! {} objects added'.format(metric_count)))
