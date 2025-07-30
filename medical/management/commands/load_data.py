import os
from django.core.management.base import BaseCommand
from medical.services.data_loader import load_csv_to_mongo


class Command(BaseCommand):
    help = "Load cross.csv and long.csv into MongoDB"

    def handle(self, *args, **kwargs):
        base_path = os.path.join(os.getcwd(), 'csvs')

        cross_path = os.path.join(base_path, 'cross.csv')
        long_path = os.path.join(base_path, 'long.csv')

        load_csv_to_mongo(cross_path, mode="cross")
        load_csv_to_mongo(long_path, mode="long")

        self.stdout.write(self.style.SUCCESS("✅ Both CSV files loaded successfully!"))
