from django.core.management.base import BaseCommand
from dataentry.models import Student
class Command(BaseCommand):
    help = "insert data to the DataBase"

    def handle(self,*args,**kwargs):
        dataset = [
            {'roll_no':100,'name':'randy','age':19},
            {'roll_no':103,'name':'ray','age':21},
            {'roll_no':104,'name':'manji','age':22},
            {'roll_no':105,'name':'san','age':22},
            
        ]
        for data in dataset:
            roll_no=data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()
            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'],name=data['name'],age=data['age'])
                self.stdout.write(self.style.SUCCESS("Data Inserted Successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"Student with roll_no {roll_no} already exits"))
