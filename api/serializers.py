from rest_framework import serializers
from django.db.models import Sum

from core.models import (
    PharmGroup,
    Medician,
    Kind,
    Country,
    Unit,
    Prescription,
    PrescriptionReturn,
    PrescriptionReturnThrough,
    PrescriptionReturnImage,
    PharmCompany,
    Store,
    Currency,
    Entrance,
    EntranceThrough,
    PaymentMethod,
    FinalRegister,
    Department,
    DoctorName,
    PatientName,
    PrescriptionThrough,
    City,
    Market,
    MedicineBarcode,
    DepartmentReturn,
    Revenue,
    PrescriptionImage,
    MedicineSaleDictionary,
    EntranceImage,
    User,
    MedicineWith,
    BigCompany,
    PurchaseList,
    MedicineConflict,
    PurchaseListManual,
    RevenueRecord,
)
import ast
import datetime

def get_num_days(start_date):
        today = datetime.date.today()
        num_days = (today - start_date).days
        return num_days

def log_entry_to_dict(log_entry):
    try:
        changes_dict = ast.literal_eval(str(log_entry.changes))
    except (ValueError, TypeError):
        changes_dict = log_entry.changes

    user = None
    if log_entry.actor_id:
        user = User.objects.get(pk=log_entry.actor_id)
        user_name = (
            f"{user.first_name} {user.last_name}"
            if user.first_name and user.last_name
            else str(user)
        )
    else:
        user_name = None
    return {
        "id": log_entry.id,
        "action": log_entry.action,
        "date": log_entry.timestamp,
        "user": log_entry.actor_id,
        "user_name": user_name,
        "changes": changes_dict,
    }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name")
        read_only_fields = ("username", "first_name")
        read_and_write_fields = ("id",)


class PharmGroupSeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = PharmGroup
        fields = "__all__"


class RevenueSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    employee_name = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()

    discount_money_value = serializers.SerializerMethodField()
    discount_percent_value = serializers.SerializerMethodField()
    zakat_value = serializers.SerializerMethodField()
    khairat_value = serializers.SerializerMethodField()
    rounded_value = serializers.SerializerMethodField()

    def get_total_value(self, revenue):
        total_value = revenue.revenuerecord_set.aggregate(
            total_value=Sum("amount")
        )["total_value"]
        return total_value or 0

    def get_discount_money_value(self, revenue):
        discount_money_value = revenue.revenuerecord_set.values('prescription').distinct().aggregate(
            discount_money_value=Sum("prescription__discount_money")
        )["discount_money_value"]
        return discount_money_value or 0

    def get_discount_percent_value(self, revenue):
        discount_percent_value = revenue.revenuerecord_set.values('prescription').distinct().aggregate(
            discount_percent_value=Sum("prescription__discount_percent")
        )["discount_percent_value"]
        return discount_percent_value or 0

    def get_zakat_value(self, revenue):
        zakat_value = revenue.revenuerecord_set.values('prescription').distinct().aggregate(zakat_value=Sum("prescription__zakat"))[
            "zakat_value"
        ]
        return zakat_value or 0

    def get_khairat_value(self, revenue):
        khairat_value = revenue.revenuerecord_set.values('prescription').distinct().aggregate(
            khairat_value=Sum("prescription__khairat")
        )["khairat_value"]
        return khairat_value or 0

    def get_rounded_value(self, revenue):
        rounded_value = revenue.revenuerecord_set.values('prescription').distinct().aggregate(
            rounded_value=Sum("prescription__rounded_number")
        )["rounded_value"]
        return rounded_value or 0

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    def get_employee_name(self, obj):
        return obj.employee.username

    class Meta:
        model = Revenue
        fields = "__all__"


class MarketSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = Market
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = City
        fields = "__all__"


class PurchaseListSerializer(serializers.ModelSerializer):
    market_1 = serializers.SerializerMethodField()
    market_2 = serializers.SerializerMethodField()
    market_3 = serializers.SerializerMethodField()
    company_1_name = serializers.SerializerMethodField()
    company_2_name = serializers.SerializerMethodField()
    company_3_name = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()

    def get_medicine_full(self, res):
        obj = res.medicine
        kind_name = ""
        country_name = ""
        big_company_name = ""
        generics = ""
        ml = ""
        weight = ""
        if obj.kind and obj.kind_english:
            kind_name = obj.kind.name_english + "."
        if obj.country:
            country_name = obj.country.name
        if obj.big_company:
            big_company_name = obj.big_company.name + " "
        if obj.generic_name:
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "}"
        if obj.ml:
            ml = obj.ml
        if obj.weight:
            weight = obj.weight

        return (
            kind_name
            + obj.brand_name
            + " "
            + obj.ml
            + " "
            + big_company_name
            + country_name
            + " "
            + weight
        )

    def get_market_1(self, obj):
        if obj.company_1.market:
            return obj.company_1.market.name
        else:
            return ""

    def get_market_2(self, obj):
        if obj.company_2.market:
            return obj.company_2.market.name
        else:
            return ""

    def get_market_3(self, obj):
        if obj.company_3.market:
            return obj.company_3.market.name
        else:
            return ""

    def get_company_1_name(self, obj):
        if obj.company_1:
            return obj.company_1.name
        return ""

    def get_company_2_name(self, obj):
        if obj.company_2:
            return obj.company_2.name
        return ""

    def get_company_3_name(self, obj):
        if obj.company_3:
            return obj.company_3.name
        return ""

    class Meta:
        model = PurchaseList
        fields = [
            "id",
            "medicine_full",
            "need_quautity",
            "company_1_name",
            "market_1",
            "price_1",
            "bonus_1",
            "date_1",
            "company_2_name",
            "market_2",
            "price_2",
            "bonus_2",
            "date_2",
            "company_3_name",
            "market_3",
            "price_3",
            "bonus_3",
            "date_3",
            "arrival_quantity",
            "shortaged",
        ]


class PurchaseListQuerySerializer(serializers.ModelSerializer):
    medicine_full = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    medicine_unsubmited = serializers.SerializerMethodField()

    def get_medicine_unsubmited(self, obj):
        return obj.unsubmited_existence

    def get_quantity(self, obj):
        return obj.maximum_existence - obj.existence

    def get_details(self, obj):
        queryset = (
            EntranceThrough.objects.filter(medician=obj.id)
            .order_by("-id")
            .values(
                "entrance__company__name",
                "entrance__company__market__name",
                "quantity_bonus",
                "each_price",
                "entrance__currency__name",
                "timestamp",
                "entrance__wholesale",
            )
        )[:3]
        return queryset

    def get_medicine_full(self, res):
        obj = res
        kind_name = ""
        country_name = ""
        big_company_name = ""
        generics = ""
        ml = ""
        weight = ""
        if obj.kind and obj.kind.name_english:
            kind_name = obj.kind.name_english + "."
        if obj.country:
            country_name = obj.country.name
        if obj.big_company:
            big_company_name = obj.big_company.name + " "
        if obj.generic_name:
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "}"
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
        )

    class Meta:
        model = Medician
        fields = [
            "id",
            "medicine_full",
            "quantity",
            "details",
            "medicine_unsubmited",
            "shorted",
            "existence",
        ]


class KindSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = Kind
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = Country
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    order_user_name = serializers.SerializerMethodField()
    prescription_image = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()

    def get_history(self, obj):
        history_list = obj.history.all()
        history_dicts = [log_entry_to_dict(entry) for entry in history_list]
        return history_dicts

    def get_prescription_image(self, obj):
        entrance_image_obj = PrescriptionImage.objects.filter(prescription=obj.id)
        json_entrance_image = PrescriptionImageSerializer(entrance_image_obj, many=True)
        return json_entrance_image.data

    def get_patient_name(self, obj):
        if obj.name:
            return str(obj.name.id) + "." + obj.name.name
    def get_order_user_name(self, obj):
        if obj.order_user:
            return obj.order_user.first_name

    def get_doctor_name(self, obj):
        if obj.doctor:
            return str(obj.doctor.id) + "." + obj.doctor.name

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    def get_department_name(self, obj):
        return obj.department.name

    class Meta:
        model = Prescription
        fields = "__all__"
        
class PrescriptionReturnSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    order_user_name = serializers.SerializerMethodField()
    prescription_image = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()

    def get_history(self, obj):
        history_list = obj.history.all()
        history_dicts = [log_entry_to_dict(entry) for entry in history_list]
        return history_dicts

    def get_prescription_image(self, obj):
        entrance_image_obj = PrescriptionReturnImage.objects.filter(prescription=obj.id)
        json_entrance_image = PrescriptionReturnImageSerializer(entrance_image_obj, many=True)
        return json_entrance_image.data

    def get_patient_name(self, obj):
        if obj.name:
            return str(obj.name.id) + "." + obj.name.name
    def get_order_user_name(self, obj):
        if obj.order_user:
            return obj.order_user.first_name

    def get_doctor_name(self, obj):
        if obj.doctor:
            return str(obj.doctor.id) + "." + obj.doctor.name

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    def get_department_name(self, obj):
        return obj.department.name

    class Meta:
        model = PrescriptionReturn
        fields = "__all__"



class PrescriptionExcelSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    order_user_name = serializers.SerializerMethodField()
    discount_value = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    def get_quantity(self, obj):
        # Count the number of related PrescriptionThrough instances
        return obj.prescriptionthrough_set.count()

    def get_discount_value (self, obj):
        grand_total = PrescriptionThrough.objects.filter(
            prescription_id=obj.id
            ).aggregate(grand_total=Sum('total_price'))['grand_total'] or 0
        discount_percent_value = grand_total * (obj.discount_percent / 100)
        discount_value = obj.discount_money + discount_percent_value
        return discount_value or 0

    def get_patient_name(self, obj):
        if obj.name:
            return str(obj.name.id) + "." + obj.name.name
    def get_order_user_name(self, obj):
        if obj.order_user:
            return obj.order_user.first_name

    def get_doctor_name(self, obj):
        if obj.doctor:
            return str(obj.doctor.id) + "." + obj.doctor.name

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    def get_department_name(self, obj):
        return obj.department.name

    class Meta:
        model = Prescription
        fields = ['id', 'prescription_number', 'patient_name', 'doctor_name', 'department_name', 'username', 'order_user_name', 'discount_money', 'discount_percent', 'discount_value', 'over_money', 'over_percent', 'khairat', 'zakat', 'rounded_number', 'purchased_value', 'purchase_payment_date', 'revenue', 'refund', 'timestamp', 'sold', 'quantity', 'created']


class DepartmentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = Department
        fields = "__all__"
        
class DepartmentReturnSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = DepartmentReturn
        fields = "__all__"


class BigCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = BigCompany
        fields = "__all__"
        
class MedicineSerializer(serializers.ModelSerializer):
    kind_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    kind_image = serializers.SerializerMethodField()
    country_image = serializers.SerializerMethodField()
    pharm_group_image = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), many=True
    )
    last_purchased_v1 = serializers.SerializerMethodField()
    
    def get_last_purchased_v1 (self, obj):
        try:
            latest_entrance = EntranceThrough.objects.filter(medician=obj.id).latest('timestamp')
            return latest_entrance.each_purchase_price
        except EntranceThrough.DoesNotExist:
            return ''

    def get_department_name(self, obj):
        if obj.department:
            return obj.department.name
        else:
            return ""

    def get_kind_image(self, obj):
        if obj.kind and obj.kind.image:
            return str(obj.kind.image)

    def get_country_image(self, obj):
        if obj.country and obj.country.image:
            return str(obj.country.image)
        else:
            return ""

    def get_pharm_group_image(self, obj):
        if obj.pharm_group and obj.pharm_group.image:
            return str(obj.pharm_group.image)
        else:
            return ""

    def get_medicine_full(self, res):
        obj = res

        # Initialize variables
        kind_name = (
            obj.kind.name_english + "." if obj.kind and obj.kind.name_english else ""
        )
        country_name = obj.country.name if obj.country else ""
        big_company_name = obj.big_company.name + " " if obj.big_company else ""
        generics = (
            "{" + str(",".join(map(str, obj.generic_name))) + "}"
            if obj.generic_name
            else ""
        )
        ml = obj.ml if obj.ml else ""
        weight = obj.weight if obj.weight else ""

        # Construct the full medicine name
        medicine_full = (
            kind_name
            + obj.brand_name
            + " "
            + ml
            + " "
            + big_company_name
            + country_name
            + " "
            + weight
        )
        return medicine_full

    def get_kind_name(self, obj):
        if obj.kind and obj.kind.name_english:
            return obj.kind.name_english
        else:
            return ""

    def get_country_name(self, obj):
        if obj.country:
            return obj.country.name
        else:
            return ""
        
    def get_company_name(self, obj):
        if obj.big_company:
            return obj.big_company.name
        else:
            return ""

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = Medician
        fields = "__all__"
        extra_kwargs = {"medicines": {"required": False}}
    class Meta:
        model = Medician
        fields = "__all__"


class StockSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    kind_name_english = serializers.SerializerMethodField()
    kind_name_persian = serializers.SerializerMethodField()
    ml = serializers.SerializerMethodField()
    pharm_group_name_persian = serializers.SerializerMethodField()
    pharm_group_name_english = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    big_company_name = serializers.SerializerMethodField()
    no_box = serializers.SerializerMethodField()
    no_pocket = serializers.SerializerMethodField()
    existence = serializers.SerializerMethodField()
    purchased_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    total_purchase = serializers.SerializerMethodField()
    total_sell = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id

    def get_medicine_full(self, obj):
        kind_name = obj.kind.name_english + "." if obj.kind and obj.kind.name_english else ""
        country_name = obj.country.name if obj.country else ""
        big_company_name = obj.big_company.name + " " if obj.big_company else ""
        generics = "{" + str(",".join(map(str, obj.generic_name))) + "}" if obj.generic_name else ""
        ml = obj.ml if obj.ml else ""
        weight = obj.weight if obj.weight else ""
        medicine_full = kind_name + obj.brand_name + " " + ml + " " + big_company_name + country_name + " " + weight
        return medicine_full

    def get_brand_name(self, obj):
        return obj.brand_name

    def get_kind_name_english(self, obj):
        return obj.kind.name_english if obj.kind else None

    def get_kind_name_persian(self, obj):
        return obj.kind.name_persian if obj.kind else None

    def get_ml(self, obj):
        return obj.ml

    def get_pharm_group_name_persian(self, obj):
        return obj.pharm_group.name_persian if obj.pharm_group else None

    def get_pharm_group_name_english(self, obj):
        return obj.pharm_group.name_english if obj.pharm_group else None

    def get_country_name(self, obj):
        return obj.country.name if obj.country else None

    def get_big_company_name(self, obj):
        return obj.big_company.name if obj.big_company else None

    def get_no_box(self, obj):
        return obj.no_box

    def get_no_pocket(self, obj):
        return obj.no_pocket

    def get_existence(self, obj):
        return obj.existence

    def get_purchased_price(self, obj):
        latest_entrance = EntranceThrough.objects.filter(medician=obj.id).order_by('-timestamp').first()
        return latest_entrance.each_purchase_price if latest_entrance else 0

    def get_total_purchase(self, obj):
        latest_entrance = EntranceThrough.objects.filter(medician=obj.id).order_by('-timestamp').first()
        if latest_entrance:
            return latest_entrance.each_purchase_price * obj.existence
        return 0

    def get_price(self, obj):
        return obj.price

    def get_total_sell(self, obj):
        return obj.price * obj.existence if obj.price and obj.existence else 0 

    class Meta:
        model = Medician
        fields = [
            'id', 
            'medicine_full', 
            'brand_name', 
            'kind_name_english', 
            'kind_name_persian', 
            'ml', 
            'pharm_group_name_persian', 
            'pharm_group_name_english', 
            'country_name', 
            'big_company_name', 
            'no_box', 
            'no_pocket', 
            'existence', 
            'purchased_price', 
            'price', 
            'total_purchase', 
            'total_sell'
        ]
        
        
class MedicianOrderSerializer(serializers.ModelSerializer):
    existence = serializers.SerializerMethodField()
    num_sell = serializers.SerializerMethodField()
    num_purchase = serializers.SerializerMethodField()
    pharm_group = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    medicine_no_box = serializers.SerializerMethodField()
    medicine_no_pocket = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    orderd_for = serializers.SerializerMethodField()
    start_report_date = serializers.SerializerMethodField()
    total_days_for_sale = serializers.SerializerMethodField()
    dictionary_sale = serializers.SerializerMethodField()
    total_sell = serializers.SerializerMethodField()
    
    def get_dictionary_sale( self, obj):
        dictionary_total = MedicineSaleDictionary.objects.filter(
            medician=obj
        ).aggregate(Sum('sale'))['sale__sum'] or 0
        
        return dictionary_total
    
    def get_total_days_for_sale (self, obj):
        request = self.context['request']
        start_date_str = request.query_params.get('start_date')
        if not start_date_str:
            start_date_str = datetime.date.today().replace(month=1, day=1).isoformat()  
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        total_days = get_num_days(start_date)
        
        return total_days
    
    def get_start_report_date (self, obj):
        request = self.context['request']
        start_date = request.query_params.get('start_date')

        if not start_date:
            start_date = datetime.date.today().replace(month=1, day=1).isoformat()           
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

        return start_date
    
    
    def get_orderd_for (self, obj):
        request = self.context['request']
        num_days = request.query_params.get('num_days')
        if not num_days:
            return 0
        return int(num_days)
    class Meta:
        model = Medician
        fields = ['id', 'medicine_full', 'medicine_no_box', 'pharm_group', 'medicine_no_pocket','existence',  'dictionary_sale','num_sell','total_sell', 'num_purchase', 'order', 'orderd_for', 'start_report_date', 'total_days_for_sale']

        
    def get_medicine_full (self, obj):
        kind_name = ""
        country_name = ""
        big_company_name = ""
        generics = ""
        ml = ""
        weight = ""
        if obj.kind and obj.kind.name_english:
            kind_name = obj.kind.name_english + "."
        if obj.country:
            country_name = obj.country.name
        if obj.big_company:
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
            + generics
            + big_company_name
            + country_name
            + " "
            + weight
        )  
        
                
    def get_existence (self, obj):
        return obj.existence
    
    
    def get_pharm_group (self, obj):
        result = ''
        if (obj.pharm_group):
            if (obj.pharm_group.name_english):
                result = obj.pharm_group.name_english
            elif (obj.pharm_group.name_persian):
                result = obj.pharm_group.name_persian
        
        return result

    def get_medicine_no_box (self, obj):
        return obj.no_box

    def get_medicine_no_pocket (self, obj):
        return obj.no_pocket
    
    def get_total_sell (self, obj):
        request = self.context['request']
        start_date = request.query_params.get('start_date')

        if not start_date:
            start_date = datetime.date.today().replace(month=1, day=1).isoformat()           
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        prescripion_through_total = PrescriptionThrough.objects.filter(
            medician=obj,
            timestamp__gte=start_date
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0
        dictionary_total = MedicineSaleDictionary.objects.filter(
            medician=obj
        ).aggregate(Sum('sale'))['sale__sum'] or 0
        result = float(prescripion_through_total) + float(dictionary_total)
        return result        
    
    def get_num_sell (self, obj):
        request = self.context['request']
        start_date = request.query_params.get('start_date')

        if not start_date:
            start_date = datetime.date.today().replace(month=1, day=1).isoformat()           
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        prescripion_through_total = PrescriptionThrough.objects.filter(
            medician=obj,
            timestamp__gte=start_date
        ).aggregate(Sum('quantity'))['quantity__sum'] or 0
        result = float(prescripion_through_total) 
        return result
        
    def get_num_purchase(self, obj):
        request = self.context['request']
        start_date = request.query_params.get('start_date')

        if not start_date:
            start_date = datetime.date.today().replace(month=1, day=1).isoformat()           
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        result = EntranceThrough.objects.filter(
            medician=obj,
            timestamp__gte=start_date
        ).aggregate(Sum('register_quantity'))['register_quantity__sum'] or 0

        return result
    

        
    def get_order(self, obj):
        request = self.context['request']
        num_days = request.query_params.get('num_days')
        start_date_str = request.query_params.get('start_date')
        if not start_date_str:
            start_date_str = datetime.date.today().replace(month=1, day=1).isoformat()  
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        total_days = get_num_days(start_date)
          
        if num_days:
            num_days = int(num_days)
            num_sell = self.get_total_sell(obj)
            result = (num_sell * num_days / total_days) - obj.existence
            if result > 0: 
                return round(result, 2)
            else:
                return 0
        else:
            return 0
        
        
class MedicineWithGetSerializer(serializers.ModelSerializer):
    additional = MedicineSerializer(many=True)
    class Meta:
        model = MedicineWith
        fields = "__all__"
        
class MedicineWithPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineWith
        fields = "__all__"


class MedicianSeralizer(serializers.ModelSerializer):
    kind_name = serializers.SerializerMethodField()
    country_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    kind_image = serializers.SerializerMethodField()
    country_image = serializers.SerializerMethodField()
    pharm_group_image = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), many=True
    )
    last_purchased_v1 = serializers.SerializerMethodField()
    add_medicine = MedicineWithGetSerializer(many=True, read_only=True)
    
    def get_last_purchased_v1 (self, obj):
        try:
            latest_entrance = EntranceThrough.objects.filter(medician=obj.id).latest('timestamp')
            return latest_entrance.each_purchase_price
        except EntranceThrough.DoesNotExist:
            return ''

    def get_department_name(self, obj):
        if obj.department:
            return obj.department.name
        else:
            return ""

    def get_kind_image(self, obj):
        if obj.kind and obj.kind.image:
            return str(obj.kind.image)

    def get_country_image(self, obj):
        if obj.country and obj.country.image:
            return str(obj.country.image)
        else:
            return ""

    def get_pharm_group_image(self, obj):
        if obj.pharm_group and obj.pharm_group.image:
            return str(obj.pharm_group.image)
        else:
            return ""

    def get_medicine_full(self, res):
        obj = res

        # Initialize variables
        kind_name = (
            obj.kind.name_english + "." if obj.kind and obj.kind.name_english else ""
        )
        country_name = obj.country.name if obj.country else ""
        big_company_name = obj.big_company.name + " " if obj.big_company else ""
        generics = (
            "{" + str(",".join(map(str, obj.generic_name))) + "}"
            if obj.generic_name
            else ""
        )
        ml = obj.ml if obj.ml else ""
        weight = obj.weight if obj.weight else ""

        # Construct the full medicine name
        medicine_full = (
            kind_name
            + obj.brand_name
            + " "
            + ml
            + " "
            + big_company_name
            + country_name
            + " "
            + weight
        )
        return medicine_full

    def get_kind_name(self, obj):
        if obj.kind and obj.kind.name_english:
            return obj.kind.name_english
        else:
            return ""

    def get_country_name(self, obj):
        if obj.country:
            return obj.country.name
        else:
            return ""

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = Medician
        fields = "__all__"
        extra_kwargs = {"medicines": {"required": False}}



class MedicineBarcodeDisplaySerializer(serializers.ModelSerializer):
    medicine = MedicianSeralizer()

    class Meta:
        model = MedicineBarcode
        fields = "__all__"


class MedicineBarcodeCreateUpdateSerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(queryset=Medician.objects.all())

    class Meta:
        model = MedicineBarcode
        fields = "__all__"


class MeidicainExcelSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    kind = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name_english",
    )
    pharm_group = serializers.SlugRelatedField(
        read_only=True, slug_field="name_english"
    )
    country = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Medician
        fields = "__all__"


class UnitSeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = Unit
        fields = "__all__"


class PharmCompanySeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    market_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()

    def get_market_name(self, obj):
        if obj.market:
            return obj.market.name
        else:
            return ""

    def get_city_name(self, obj):
        if obj.city:
            return obj.city.name
        else:
            return ""

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = PharmCompany
        fields = "__all__"





class MedicineConflictSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicineConflict
        fields = "__all__"


class EntranceSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    currency_name = serializers.SerializerMethodField()
    entrance_image = serializers.SerializerMethodField()
    entrance_total = serializers.SerializerMethodField()

    def get_entrance_total(self, obj):
        total = list(
            EntranceThrough.objects.filter(entrance=obj.id)
            .aggregate(Sum("total_purchaseـcurrency"))
            .values()
        )[0]
        return total

    def get_entrance_image(self, obj):
        entrance_image_obj = EntranceImage.objects.filter(entrance=obj.id)
        json_entrance_image = EntranceImageSeriazlier(entrance_image_obj, many=True)
        return json_entrance_image.data

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    def get_currency_name(self, obj):
        return obj.currency.name

    class Meta:
        model = Entrance
        fields = "__all__"


class EntranceImageSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = EntranceImage
        fields = "__all__"


class PrescriptionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionImage
        fields = "__all__"
        
class PrescriptionReturnImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionReturnImage
        fields = "__all__"


class EntranceThroughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    medicine_min_expire = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    medicine_existence = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    entrance_department = serializers.SerializerMethodField()
    
    def get_entrance_department(self, obj):
        if(obj.entrance.final_register):
            return obj.entrance.final_register.name
        return ''
    
    def get_company_name (self, res):
        if ( res.entrance.company):
            return res.entrance.company.name
        else:
            return ''
        
    def get_medicine_existence (self, res):
        if ( res.medician):
            if (res.medician.existence):
                return res.medician.existence
        else:
            return 0

    def get_description(self, res):
        return res.entrance.description

    def get_medicine_full(self, res):
        obj = res.medician
        kind_name = ""
        country_name = ""
        big_company_name = ""
        generics = ""
        ml = ""
        weight = ""
        if obj.kind and obj.kind.name_english:
            kind_name = obj.kind.name_english + "."
        if obj.country:
            country_name = obj.country.name
        if obj.big_company:
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
        )

    def get_medicine_min_expire(self, obj):
        return obj.medician.min_expire_date

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = EntranceThrough
        fields = "__all__"


class EntranceThroughExpiresSerializer(serializers.ModelSerializer):
    medician = MedicianSeralizer()

    class Meta:
        model = EntranceThrough
        fields = ("medician",)


class StoreSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = Store
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = Currency
        fields = "__all__"


class PaymentMethodSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = PaymentMethod
        fields = "__all__"


class FinalRegisterSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = FinalRegister
        fields = "__all__"


class RevenueRecordSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    prescription_number = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    
    
    discount_money = serializers.SerializerMethodField()
    def get_discount_money(self, obj):
        if (obj.prescription and obj.prescription.discount_money):
            return obj.prescription.discount_money
        if (obj.prescription_return and obj.prescription_return.discount_money):
            return obj.prescription_return.discount_money
        else:
            return 0
        
    discount_percent = serializers.SerializerMethodField()
    def get_discount_percent(self, obj):
        if (obj.prescription and obj.prescription.discount_percent):
            return obj.prescription.discount_percent
        if (obj.prescription_return and obj.prescription_return.discount_percent):
            return obj.prescription_return.discount_percent
        else:
            return 0
    khairat = serializers.SerializerMethodField()
    def get_khairat(self, obj):
        if (obj.prescription and obj.prescription.khairat):
            return obj.prescription.khairat
        if (obj.prescription_return and obj.prescription_return.khairat):
            return obj.prescription_return.khairat
        else:
            return 0
    zakat = serializers.SerializerMethodField()
    def get_zakat(self, obj):
        if (obj.prescription and obj.prescription.zakat):
            return obj.prescription.zakat
        if (obj.prescription_return and obj.prescription_return.zakat):
            return obj.prescription_return.zakat
        else:
            return 0
    rounded_number = serializers.SerializerMethodField()
    def get_rounded_number(self, obj):
        if (obj.prescription and obj.prescription.rounded_number):
            return obj.prescription.rounded_number
        if (obj.prescription_return and obj.prescription_return.rounded_number):
            return obj.prescription_return.rounded_number
        else:
            return 0
    

    def get_patient_name(self, obj):
        if (obj.prescription and obj.prescription.name):
            return obj.prescription.name.name
        if (obj.prescription_return and obj.prescription_return.name):
            return obj.prescription_return.name.name
        else:
            return 0

    def get_prescription_number(self, obj):
        if(obj.prescription):
            return obj.prescription.prescription_number
        if(obj.prescription_return):
            return obj.prescription_return.prescription_number
        else: return ''

    def get_department_name(self, obj):
        if(obj.prescription):
            return obj.prescription.department.name
        if(obj.prescription_return):
            return obj.prescription_return.department.name
        else: return ''

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = RevenueRecord
        fields = "__all__"


class DoctorNameSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    code_name = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    def get_code_name(self, obj):
        return str(obj.id) + "." + obj.name

    class Meta:
        model = DoctorName
        fields = "__all__"


class PatientNameSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    code_name = serializers.SerializerMethodField()

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    def get_code_name(self, obj):
        return str(obj.id) + "." + obj.name

    class Meta:
        model = PatientName
        fields = "__all__"


class PurchaseListManualSerializer(serializers.ModelSerializer):
    medicine_full = serializers.SerializerMethodField()
    existence = serializers.SerializerMethodField()
    details_1 = serializers.SerializerMethodField()
    details_2 = serializers.SerializerMethodField()
    details_3 = serializers.SerializerMethodField()

    def get_details_1(self, obj):
        queryset = (
            EntranceThrough.objects.filter(medician=obj.medicine)
            .order_by("-id")
            .values(
                "entrance__company__name",
                "entrance__company__market__name",
                "quantity_bonus",
                "each_price_factor",
                "entrance__currency__name",
                "timestamp",
                "entrance__wholesale",
            )
        )[0:1]
        data = list(queryset)
        return data

    def get_details_2(self, obj):
        queryset = (
            EntranceThrough.objects.filter(medician=obj.medicine)
            .order_by("-id")
            .values(
                "entrance__company__name",
                "entrance__company__market__name",
                "quantity_bonus",
                "each_price_factor",
                "entrance__currency__name",
                "timestamp",
                "entrance__wholesale",
            )
        )[1:2]
        data = list(queryset)
        return data

    def get_details_3(self, obj):
        queryset = (
            EntranceThrough.objects.filter(medician=obj.medicine)
            .order_by("-id")
            .values(
                "entrance__company__name",
                "entrance__company__market__name",
                "quantity_bonus",
                "each_price_factor",
                "entrance__currency__name",
                "timestamp",
                "entrance__wholesale",
            )
        )[2:3]
        data = list(queryset)
        return data

    def get_existence(self, obj):
        return obj.medicine.existence

    def get_medicine_full(self, res):
        obj = res.medicine
        kind_name = ""
        country_name = ""
        big_company_name = ""
        generics = ""
        ml = ""
        weight = ""
        if obj.kind and obj.kind.name_english:
            kind_name = obj.kind.name_english + "."
        if obj.country:
            country_name = obj.country.name
        if obj.big_company:
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
            + generics
            + big_company_name
            + country_name
            + " "
            + weight
        ) 

    class Meta:
        model = PurchaseListManual
        fields = "__all__"


class PrescriptionThroughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    medicine_cautions = serializers.SerializerMethodField()
    medicine_usage = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    medicine_no_box = serializers.SerializerMethodField()
    medicine_no_quantity = serializers.SerializerMethodField()
    prescription_number = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    medicine_existence = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    
    def get_patient_name (self, res):
        if (res.prescription and res.prescription.name):
            return res.prescription.name.name
        else:
            return ''

    def get_medicine_existence(self, res):
        if res.medician and res.medician.existence:
            return res.medician.existence
        else:
            """"""

    def get_department_name(self, res):
        return res.prescription.department.name

    def get_prescription_number(self, res):
        return res.prescription.prescription_number

    def get_medicine_full(self, res):
        obj = res.medician
        kind_name = ""
        country_name = ""
        big_company_name = ""
        generics = ""
        ml = ""
        weight = ""
        if obj.kind and obj.kind.name_english:
            kind_name = obj.kind.name_english + "."
        if obj.country:
            country_name = obj.country.name
        if obj.big_company:
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
            + generics
            + big_company_name
            + country_name
            + " "
            + weight
        )

    def get_medicine_cautions(self, obj):
        if obj.medician.cautions:
            return obj.medician.cautions
        else:
            return ""

    def get_medicine_no_box(self, obj):
        if obj.medician.no_box:
            return obj.medician.no_box
        else:
            return ""

    def get_medicine_no_quantity(self, obj):
        if obj.medician.no_pocket:
            return obj.medician.no_pocket
        else:
            return ""

    def get_medicine_usage(self, obj):
        if obj.medician.usages:
            return obj.medician.usages
        else:
            return ""

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = PrescriptionThrough
        fields = "__all__"
        
class PrescriptionThroughReturnSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    medicine_cautions = serializers.SerializerMethodField()
    medicine_usage = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    medicine_no_box = serializers.SerializerMethodField()
    medicine_no_quantity = serializers.SerializerMethodField()
    prescription_number = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    medicine_existence = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    
    def get_patient_name (self, res):
        if (res.prescription and res.prescription.name):
            return res.prescription.name.name
        else:
            return ''

    def get_medicine_existence(self, res):
        if res.medician and res.medician.existence:
            return res.medician.existence
        else:
            """"""

    def get_department_name(self, res):
        return res.prescription.department.name

    def get_prescription_number(self, res):
        return res.prescription.prescription_number

    def get_medicine_full(self, res):
        obj = res.medician
        kind_name = ""
        country_name = ""
        big_company_name = ""
        generics = ""
        ml = ""
        weight = ""
        if obj.kind and obj.kind.name_english:
            kind_name = obj.kind.name_english + "."
        if obj.country:
            country_name = obj.country.name
        if obj.big_company:
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
            + generics
            + big_company_name
            + country_name
            + " "
            + weight
        )

    def get_medicine_cautions(self, obj):
        if obj.medician.cautions:
            return obj.medician.cautions
        else:
            return ""

    def get_medicine_no_box(self, obj):
        if obj.medician.no_box:
            return obj.medician.no_box
        else:
            return ""

    def get_medicine_no_quantity(self, obj):
        if obj.medician.no_pocket:
            return obj.medician.no_pocket
        else:
            return ""

    def get_medicine_usage(self, obj):
        if obj.medician.usages:
            return obj.medician.usages
        else:
            return ""

    def get_username(self, res):
        if res.user and res.user.first_name:
            return res.user.first_name
        else:
            return ""

    class Meta:
        model = PrescriptionReturnThrough
        fields = "__all__"


class TrazSerializer(serializers.Serializer):
    entrances = EntranceThroughSerializer(many=True)
    prescriptions = PrescriptionThroughSerializer(many=True)


class MedicineMinimumSerializer (serializers.Serializer):
    medicine_id = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    kind_persian = serializers.SerializerMethodField()
    kind_english = serializers.SerializerMethodField()
    pharm_group_persian = serializers.SerializerMethodField()
    pharm_group_english = serializers.SerializerMethodField()
    existence = serializers.SerializerMethodField()
    minimum = serializers.SerializerMethodField()
    maximum = serializers.SerializerMethodField()
    need = serializers.SerializerMethodField()
    details_1 = serializers.SerializerMethodField()
    details_2 = serializers.SerializerMethodField()
    details_3 = serializers.SerializerMethodField()
    
    def get_kind_persian (self, obj):
        if (obj.kind):
            if (obj.kind.name_persian):
                return obj.kind.name_persian
        return ''
    
    def get_kind_english (self, obj):
        if (obj.kind):
            if (obj.kind.name_english):
                return obj.kind.name_english
        return ''
    
    def get_pharm_group_persian (self, obj):
        if (obj.pharm_group):
            if (obj.pharm_group.name_persian):
                return obj.pharm_group.name_persian
        return ''
    def get_pharm_group_english (self, obj):
        if (obj.pharm_group):
            if (obj.pharm_group.name_english):
                return obj.pharm_group.name_english
        return ''
    
    def get_need (self, obj):
        if (obj.maximum_existence):   
            return float(obj.maximum_existence) - float(obj.existence)
        return ''
    
    def get_medicine_id (self, obj):
        return obj.id

    def get_details_1(self, obj):
        queryset = (
            EntranceThrough.objects.filter(medician=obj.id)
            .order_by("-id")
            .values(
                "entrance__company__name",
                "entrance__company__market__name",
                "quantity_bonus",
                "each_price_factor",
                "entrance__currency__name",
                "timestamp",
                "entrance__wholesale",
            )
        )[0:1]
        data = list(queryset)
        return data

    def get_details_2(self, obj):
        queryset = (
            EntranceThrough.objects.filter(medician=obj.id)
            .order_by("-id")
            .values(
                "entrance__company__name",
                "entrance__company__market__name",
                "quantity_bonus",
                "each_price_factor",
                "entrance__currency__name",
                "timestamp",
                "entrance__wholesale",
            )
        )[1:2]
        data = list(queryset)
        return data

    def get_details_3(self, obj):
        queryset = (
            EntranceThrough.objects.filter(medician=obj.id)
            .order_by("-id")
            .values(
                "entrance__company__name",
                "entrance__company__market__name",
                "quantity_bonus",
                "each_price_factor",
                "entrance__currency__name",
                "timestamp",
                "entrance__wholesale",
            )
        )[2:3]
        data = list(queryset)
        return data

    def get_existence(self, obj):
        return obj.existence
    
    def get_minimum(self, obj):
        return obj.minmum_existence
    
    def get_maximum(self, obj):
        return obj.maximum_existence

    def get_medicine_full(self, res):
        obj = res
        kind_name = ""
        country_name = ""
        big_company_name = ""
        generics = ""
        ml = ""
        weight = ""
        if obj.kind and obj.kind.name_english:
            kind_name = obj.kind.name_english + "."
        if obj.country:
            country_name = obj.country.name
        if obj.big_company:
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
        )

    class Meta:
        model = Medician
        fields = "__all__"