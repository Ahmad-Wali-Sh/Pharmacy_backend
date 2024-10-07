from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete, pre_save
from auditlog.models import LogEntry
from django.contrib.contenttypes.models import ContentType
import json
from django.core.serializers.json import DjangoJSONEncoder
from . import models
from django.db.models import Sum
from django.db import transaction

@receiver([post_delete, post_save], sender=models.RevenueRecord)
def calcualting_purchase_value (sender, instance, **kwargs):
    
    if(instance.prescription):        
        purchased_total = (
            models.RevenueRecord.objects.filter(prescription=instance.prescription)
            .aggregate(Sum("amount"))
            .get("amount__sum", 0)
        )
        
        if purchased_total:
            instance.prescription.purchased_value = purchased_total
            instance.prescription.refund = instance.prescription.grand_total - purchased_total
        else:
            instance.prescription.purchased_value = 0
            instance.prescription.refund = instance.prescription.grand_total
        
        instance.prescription.save()
            
    if(instance.prescription_return):
        purchased_total = (
            models.RevenueRecord.objects.filter(prescription_return=instance.prescription_return)
            .aggregate(Sum("amount"))
            .get("amount__sum", 0)
        )
        
        if purchased_total:
            instance.prescription_return.purchased_value = purchased_total
            instance.prescription_return.refund = instance.prescription_return.grand_total - purchased_total
        else:
            instance.prescription_return.purchased_value = 0
            instance.prescription_return.refund = instance.prescription_return.grand_total

        instance.prescription_return.save()
    


@receiver(post_delete, sender=models.PrescriptionThrough)
def deleting_prescriptionThrough(sender, instance, **kwargs):

    prescription_through_total = list(
        models.PrescriptionThrough.objects.filter(
            prescription_id=instance.prescription.id
        )
        .aggregate(Sum("total_price"))
        .values()
    )[0]
    discount_percent = float(instance.prescription.discount_percent)
    over_percent = float(instance.prescription.over_percent)
    if prescription_through_total:
        discount_amount = prescription_through_total * (discount_percent / 100)
        over_amount = prescription_through_total * (over_percent / 100)
        grand_total = (
            float(prescription_through_total)
            - discount_amount
            - float(instance.prescription.zakat)
            - float(instance.prescription.khairat)
            - float(instance.prescription.discount_money)
            + float(instance.prescription.rounded_number)
            + over_amount
            + float(instance.prescription.over_money)
        )
    else:
        grand_total = 0

    if prescription_through_total and grand_total:
        instance.prescription.grand_total = round(grand_total, 0)

    else:
        instance.prescription.grand_total = 0
        
    purchased_total = (
           models.RevenueRecord.objects.filter(prescription=instance.prescription, prescription_return__isnull=True)
            .aggregate(total=Sum("amount"))
            .get("total") or 0
        )

    if purchased_total:
        instance.prescription.purchased_value = purchased_total
        instance.prescription.refund = instance.prescription.grand_total - purchased_total
    else:
        instance.prescription.purchased_value = 0
        instance.prescription.refund = instance.prescription.grand_total

    instance.prescription.save()
    
@receiver(post_delete, sender=models.PrescriptionReturnThrough)
def deleting_prescriptionReturnThrough(sender, instance, **kwargs):

    prescription_through_total = list(
        models.PrescriptionReturnThrough.objects.filter(
            prescription_id=instance.prescription.id
        )
        .aggregate(Sum("total_price"))
        .values()
    )[0]
    discount_percent = float(instance.prescription.discount_percent)
    over_percent = float(instance.prescription.over_percent)
    if prescription_through_total:
        discount_amount = prescription_through_total * (discount_percent / 100)
        over_amount = prescription_through_total * (over_percent / 100)
        grand_total = -(
            float(prescription_through_total)
            - discount_amount
            - float(instance.prescription.zakat)
            - float(instance.prescription.khairat)
            - float(instance.prescription.discount_money)
            + float(instance.prescription.rounded_number)
            + over_amount
            + float(instance.prescription.over_money)
        )
    else:
        grand_total = 0

    if prescription_through_total and grand_total:
        instance.prescription.grand_total = round(grand_total, 0)

    else:
        instance.prescription.grand_total = 0
        
    purchased_total = (
        models.RevenueRecord.objects.filter(prescription_return=instance.prescription, prescription__isnull=True)
        .aggregate(Sum("amount"))
        .get("amount__sum", 0)
    )

    if purchased_total:
        instance.prescription.purchased_value = purchased_total
        instance.prescription.refund = instance.prescription.grand_total - purchased_total
    else:
        instance.prescription.purchased_value = 0
        instance.prescription.refund = instance.prescription.grand_total

    instance.prescription.save()


def get_medicine_full(res):
    obj = res
    kind_name = ""
    country_name = ""
    big_company_name = ""
    generics = ""
    ml = ""
    weight = ""
    if obj.kind and obj.kind.name_english:
        kind_name = obj.kind.name_english + "."
    if obj.country and obj.country.name:
        country_name = obj.country.name
    if obj.big_company and obj.big_company.name:
        big_company_name = obj.big_company.name + " "
    if obj.generic_name:
        generics = "{" + str(",".join(map(str, obj.generic_name))) + "} "
    if obj.ml:
        ml = obj.ml
    if obj.weight:
        weight = obj.weight

    return (
        kind_name
        + obj.brand_name
        + " "
        + ml
        + " "
        + big_company_name
        + country_name
        + " "
        + weight
    ).strip()


def get_prescription_through_data(prescription_through):
    return {
        "medician_id": prescription_through.medician_id,
        "quantity": prescription_through.quantity,
        "medician_name": get_medicine_full(prescription_through.medician),
        "each_price": prescription_through.each_price,
        "total_price": prescription_through.total_price,
    }


@receiver(pre_save, sender=models.PrescriptionThrough)
@receiver(pre_delete, sender=models.PrescriptionThrough)
def prescription_through_changed(sender, instance, **kwargs):
    if kwargs.get("raw", False):
        return

    changes = {}

    if instance.pk:
        try:
            previous_instance = models.PrescriptionThrough.objects.get(pk=instance.pk)
        except models.PrescriptionThrough.DoesNotExist:
            # This is a new instance, so we don't have previous data
            changes = dict(
                prescription_through=dict(new=get_prescription_through_data(instance)),
            )
        else:
            current_data = get_prescription_through_data(instance)
            previous_data = get_prescription_through_data(previous_instance)

            if (
                previous_data["medician_id"] != current_data["medician_id"]
                or previous_data["quantity"] != current_data["quantity"]
                or previous_data["each_price"] != current_data["each_price"]
                or previous_data["total_price"] != current_data["total_price"]
            ):
                changes = dict(
                    prescription_through=dict(old=previous_data, new=current_data),
                )

        if changes:
            LogEntry.objects.create(
                object_id=instance.prescription_id,
                content_type=ContentType.objects.get_for_model(instance.prescription),
                actor_id=instance.prescription.user_id,
                action=(
                    1 if previous_instance else 0
                ),  # Action flag for update or creation
                changes=json.dumps(changes, cls=DjangoJSONEncoder),
            )

    elif kwargs.get("signal") == pre_delete:
        changes = dict(
            prescription_through=dict(old=get_prescription_through_data(instance)),
        )

        LogEntry.objects.create(
            object_id=instance.prescription_id,
            content_type=ContentType.objects.get_for_model(instance.prescription),
            actor_id=instance.prescription.user_id,
            action=2,  # Action flag for deletion
            changes=json.dumps(changes, cls=DjangoJSONEncoder),
        )


@receiver(post_save, sender=models.PrescriptionThrough)
def prescription_through_post_save(sender, instance, created, **kwargs):
    if kwargs.get("raw", False):
        return

    if created:
        changes = dict(
            prescription_through=dict(new=get_prescription_through_data(instance)),
        )

        LogEntry.objects.create(
            object_id=instance.prescription_id,
            content_type=ContentType.objects.get_for_model(instance.prescription),
            actor_id=instance.prescription.user_id,
            action=0,  # Action flag for creation
            changes=json.dumps(changes, cls=DjangoJSONEncoder),
        )
    else:
        try:
            previous_instance = models.PrescriptionThrough.objects.get(pk=instance.pk)
        except models.PrescriptionThrough.DoesNotExist:
            pass
        else:
            current_data = get_prescription_through_data(instance)
            previous_data = get_prescription_through_data(previous_instance)

            if (
                previous_data["medician_id"] != current_data["medician_id"]
                or previous_data["quantity"] != current_data["quantity"]
                or previous_data["each_price"] != current_data["each_price"]
                or previous_data["total_price"] != current_data["total_price"]
            ):
                changes = dict(
                    prescription_through=dict(old=previous_data, new=current_data),
                )

                LogEntry.objects.create(
                    object_id=instance.prescription_id,
                    content_type=ContentType.objects.get_for_model(
                        instance.prescription
                    ),
                    actor_id=instance.prescription.user_id,
                    action=1,  # Action flag for update
                    changes=json.dumps(changes, cls=DjangoJSONEncoder),
                )


@receiver(post_delete, sender=models.PrescriptionThrough)
def prescription_through_post_delete(sender, instance, **kwargs):
    if kwargs.get("raw", False):
        return

    changes = dict(
        prescription_through=dict(old=get_prescription_through_data(instance)),
    )

    LogEntry.objects.create(
        object_id=instance.prescription_id,
        content_type=ContentType.objects.get_for_model(instance.prescription),
        actor_id=instance.prescription.user_id,
        action=2,  # Action flag for deletion
        changes=json.dumps(changes, cls=DjangoJSONEncoder),
    )


@receiver([post_save, post_delete], sender=models.EntranceThrough)
@receiver([post_save, post_delete], sender=models.PrescriptionThrough)
@receiver([post_save, post_delete], sender=models.PrescriptionReturnThrough)
def update_medician_existence(sender, instance, **kwargs):
    medician = instance.medician
    
    with transaction.atomic(): 
        
        post_save.disconnect(update_medician_existence, sender=models.EntranceThrough)
        post_save.disconnect(update_medician_existence, sender=models.PrescriptionThrough)
        post_save.disconnect(update_medician_existence, sender=models.PrescriptionReturnThrough)
        
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
        prescription_sum = (
            prescription_sum_query if prescription_sum_query is not None else 0
        )
        prescription_return_sum = prescription_return_sum_query if prescription_return_sum_query is not None else 0

        existence = entrance_sum - prescription_sum + prescription_return_sum
        if existence is None:
            existence = 0
        medician.existence = round(existence, 1)

        if existence >= medician.unsubmited_existence:
            medician.unsubmited_existence = 0

        medician.save()
        
        post_save.connect(update_medician_existence, sender=models.EntranceThrough)
        post_save.connect(update_medician_existence, sender=models.PrescriptionThrough)
        post_save.connect(update_medician_existence, sender=models.PrescriptionReturnThrough)
    
    
