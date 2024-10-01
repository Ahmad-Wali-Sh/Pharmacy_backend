from django.core.management.base import BaseCommand
from django.db.models import Sum
from core import models  # Replace with the correct import for your models

class Command(BaseCommand):
    help = 'Recalculate medician existence for all medicines'

    def handle(self, *args, **kwargs):
        medicines = models.Medician.objects.all()  # Replace 'Medician' with your model name for medicines

        for medician in medicines:
            entrance_sum_query = (
                models.EntranceThrough.objects.filter(medician_id=medician.id)
                .aggregate(Sum("register_quantity"))
                .get("register_quantity__sum", 0)
            )
            prescription_sum_query = (
                models.PrescriptionThrough.objects.filter(medician_id=medician.id)
                .aggregate(Sum("quantity"))
                .get("quantity__sum", 0)
            )
            prescription_return_sum_query = (
                models.PrescriptionReturnThrough.objects.filter(medician_id=medician.id)
                .aggregate(Sum("quantity"))
                .get("quantity__sum", 0)
            )

            entrance_sum = entrance_sum_query if entrance_sum_query is not None else 0
            prescription_sum = prescription_sum_query if prescription_sum_query is not None else 0
            prescription_return_sum = prescription_return_sum_query if prescription_return_sum_query is not None else 0

            existence = entrance_sum - prescription_sum + prescription_return_sum
            existence = round(existence, 1)

            if existence >= medician.unsubmited_existence:
                medician.unsubmited_existence = 0

            medician.existence = existence
            medician.save()

        self.stdout.write(self.style.SUCCESS('Successfully recalculated existence for all medicines.'))