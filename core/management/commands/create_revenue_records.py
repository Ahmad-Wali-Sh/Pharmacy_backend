from django.core.management.base import BaseCommand
from core.models import Prescription, RevenueRecord

class Command(BaseCommand):
    help = 'Create revenue records for prescriptions with sold=True'

    def handle(self, *args, **options):
        prescriptions = Prescription.objects.filter(sold=True)

        for prescription in prescriptions:
            RevenueRecord.objects.create(
                revenue=prescription.revenue,
                user=prescription.revenue.user,
                amount=prescription.purchased_value,
                prescription=prescription,
                record_type='system'
            )

        self.stdout.write(self.style.SUCCESS('Revenue records created successfully'))
