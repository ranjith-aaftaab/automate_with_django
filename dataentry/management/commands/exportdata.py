from django.core.management.base import BaseCommand
from django.apps import apps
import csv
import datetime

class Command(BaseCommand):
    help = 'Export data from the database to a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Model name to export')

    def handle(self, *args, **kwargs):
        model = None
        model_name = kwargs['model_name'].capitalize()

        # Search through all the installed apps in Django
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                pass

        if not model:
            self.stderr.write(f"Model {model_name} could not be found")
            return

        # Fetch data from the database
        data = model.objects.all()

        # Creating timestamp for CSV file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # Define CSV file name
        file_path = f'exported_{model_name}_data_{timestamp}.csv'

        # Open the CSV file and write the data       
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the CSV header
            writer.writerow([field.name for field in model._meta.fields])

            # Write data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported successfully'))
