from typing import Any
from django.core.management.base import BaseCommand
from django_seed import Seed
from core.models import Kind, User

class Command(BaseCommand):
    help = 'Seed Database Tables'
    
    def handle(self, *args, **options):
        seeder = Seed.seeder()
        # Customize the seeding process here
        seeder.add_entity(Kind, 20, {
            'user': User.objects.get(username='admin'),
            'name_english': lambda x: seeder.faker.name(),
            'name_persian': '',
            'image': '',
            'description':'',
        })
        inserted_pks = seeder.execute()
        self.stdout.write(self.style.SUCCESS('Database Successfully Seeded!'))






