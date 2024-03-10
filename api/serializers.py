from rest_framework import serializers
from django.core import serializers as core_serializers
import io
from django.db.models import F
from django.db.models import Sum

from core.models import PharmGroup, Medician, Kind, Country, Unit, Prescription, PharmCompany, \
    Store, Currency, Entrance, EntranceThrough, PaymentMethod, FinalRegister, Department, DoctorName, PatientName, PrescriptionThrough, \
    Outrance, OutranceThrough, City, Market,MedicineBarcode, Revenue, PrescriptionImage, RevenueTrough, EntranceImage, User, MedicineWith, BigCompany, MedicineConflict, PurchaseList, PurchaseListManual

from django_jalali.serializers.serializerfield import JDateField, JDateTimeField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')
        read_only_fields = ('username', 'first_name')
        read_and_write_fields = ('id',)


class PharmGroupSeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = PharmGroup
        fields = '__all__'


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
        total_value = revenue.prescription_set.aggregate(total_value=Sum('grand_total'))['total_value']
        return total_value or 0

    def get_discount_money_value(self, revenue):
        discount_money_value = revenue.prescription_set.aggregate(discount_money_value=Sum('discount_money'))['discount_money_value']
        return discount_money_value or 0

    def get_discount_percent_value(self, revenue):
        discount_percent_value = revenue.prescription_set.aggregate(discount_percent_value=Sum('discount_percent'))['discount_percent_value']
        return discount_percent_value or 0

    def get_zakat_value(self, revenue):
        zakat_value = revenue.prescription_set.aggregate(zakat_value=Sum('zakat'))['zakat_value']
        return zakat_value or 0

    def get_khairat_value(self, revenue):
        khairat_value = revenue.prescription_set.aggregate(khairat_value=Sum('khairat'))['khairat_value']
        return khairat_value or 0

    def get_rounded_value(self, revenue):
        rounded_value = revenue.prescription_set.aggregate(rounded_value=Sum('rounded_number'))['rounded_value']
        return rounded_value or 0

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    def get_employee_name(self, obj):
        return obj.employee.username

    class Meta:
        model = Revenue
        fields = '__all__'


class RevenueTrhoughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    prescription_number = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    prescription_user = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    zakat = serializers.SerializerMethodField()
    khairat = serializers.SerializerMethodField()
    rounded = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()

    def get_patient_name(self, obj):
        if (obj.prescription.name):
            return str(obj.prescription.name.id) + "." + obj.prescription.name.name

    def get_prescription_user(self, obj):
        return obj.prescription.user.username

    def get_discount(self, obj):
        return obj.prescription.discount_percent

    def get_zakat(self, obj):
        return obj.prescription.zakat

    def get_khairat(self, obj):
        return obj.prescription.khairat

    def get_rounded(self, obj):
        return obj.prescription.rounded_number

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    def get_prescription_number(self, obj):
        return obj.prescription.prescription_number

    def get_grand_total(self, obj):
        return obj.prescription.grand_total

    def get_department(self, obj):
        return obj.prescription.department.name

    prescription = serializers.PrimaryKeyRelatedField(
        queryset=Prescription.objects.all()
    )

    class Meta:
        model = RevenueTrough
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = Market
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = City
        fields = '__all__'


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
        big_company_name = ''
        generics = ''
        ml = ''
        weight = ''
        if (obj.kind and obj.kind_english):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "}"
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + obj.ml + ' ' + big_company_name + country_name + " " + weight

    def get_market_1(self, obj):
        if (obj.company_1.market):
            return obj.company_1.market.name
        else:
            return ""

    def get_market_2(self, obj):
        if (obj.company_2.market):
            return obj.company_2.market.name
        else:
            return ""

    def get_market_3(self, obj):
        if (obj.company_3.market):
            return obj.company_3.market.name
        else:
            return ""

    def get_company_1_name(self, obj):
        if (obj.company_1):
            return obj.company_1.name
        return ""

    def get_company_2_name(self, obj):
        if (obj.company_2):
            return obj.company_2.name
        return ""

    def get_company_3_name(self, obj):
        if (obj.company_3):
            return obj.company_3.name
        return ""

    class Meta:
        model = PurchaseList
        fields = ['id', 'medicine_full', 'need_quautity', 'company_1_name', 'market_1', 'price_1', 'bonus_1', 'date_1', 'company_2_name',
                  'market_2', 'price_2', 'bonus_2', 'date_2', 'company_3_name', 'market_3', 'price_3', 'bonus_3', 'date_3', 'arrival_quantity', 'shortaged']


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
        queryset = (EntranceThrough.objects.filter(medician=obj.id).order_by("-id").values('entrance__company__name',
                    'entrance__company__market__name', 'quantity_bonus', 'each_price', 'entrance__currency__name', 'timestamp', 'entrance__wholesale'))[:3]
        return queryset

    def get_medicine_full(self, res):
        obj = res
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ''
        ml = ''
        weight = ''
        if (obj.kind and obj.kind.name_english):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "}"
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + ml + ' ' + big_company_name + country_name + " " + weight

    class Meta:
        model = Medician
        fields = ['id', 'medicine_full', 'quantity',
                  'details', 'medicine_unsubmited', 'shorted', 'existence']




class KindSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = Kind
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = Country
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    prescription_image = serializers.SerializerMethodField()
    
    
    def get_prescription_image(self, obj):
        entrance_image_obj = PrescriptionImage.objects.filter(prescription=obj.id)
        json_entrance_image = PrescriptionImageSerializer(
            entrance_image_obj, many=True)
        return json_entrance_image.data

    def get_patient_name(self, obj):
        if (obj.name):
            return str(obj.name.id) + "." + obj.name.name

    def get_doctor_name(self, obj):
        if (obj.doctor):
            return str(obj.doctor.id) + "." + obj.doctor.name

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    def get_department_name(self, obj):
        return obj.department.name

    class Meta:
        model = Prescription
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = Department
        fields = '__all__'


class BigCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = BigCompany
        fields = '__all__'




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
        queryset=Department.objects.all(), many=True)

    def get_department_name(self, obj):
        if (obj.department):
            return obj.department.name
        else:
            ""


    def get_kind_image(self, obj):
        if (obj.kind and obj.kind.image):
            return str(obj.kind.image)

    def get_country_image(self, obj):
        if (obj.country and obj.country.image):
            return str(obj.country.image)
        else:
            return ""

    def get_pharm_group_image(self, obj):
        if (obj.pharm_group and obj.pharm_group.image):
            return str(obj.pharm_group.image)
        else:
            return ""

    def get_medicine_full(self, res):
        obj = res
        
        # Initialize variables
        kind_name = obj.kind.name_english + "." if obj.kind and obj.kind.name_english else ""
        country_name = obj.country.name if obj.country else ""
        big_company_name = obj.big_company.name + " " if obj.big_company else ""
        generics = "{" + str(",".join(map(str, obj.generic_name))) + "}" if obj.generic_name else ""
        ml = obj.ml if obj.ml else ""
        weight = obj.weight if obj.weight else ""
        
        # Construct the full medicine name
        medicine_full = (
            kind_name +
            obj.brand_name + ' ' +
            ml + ' ' +
            big_company_name +
            country_name + " " +
            weight
        )
        return medicine_full

    def get_kind_name(self, obj):
        if obj.kind:
            return obj.kind.name_english
        else:
            return ""

    def get_country_name(self, obj):
        if obj.country:
            return obj.country.name
        else:
            return ""

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = Medician
        fields = '__all__'
        extra_kwargs = {'medicines': {'required': False}}

class MedicineBarcodeSerializer(serializers.ModelSerializer):
    medician = serializers.SerializerMethodField()

    def get_medician (self, obj):
        entrance_image_obj = obj.medicine
        json_entrance_image = MedicianSeralizer(
            entrance_image_obj)
        return json_entrance_image.data
    class Meta:
        model = MedicineBarcode
        fields = '__all__'


class MeidicainExcelSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    kind = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name_english',
    )
    pharm_group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name_english'
    )
    country = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Medician
        fields = '__all__'


class UnitSeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = Unit
        fields = '__all__'


class PharmCompanySeralizer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    market_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()

    def get_market_name(self, obj):
        if (obj.market):
            return obj.market.name
        else:
            return ''

    def get_city_name(self, obj):
        if (obj.city):
            return obj.city.name
        else:
            return ''

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = PharmCompany
        fields = '__all__'


class MedicineWithSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicineWith
        fields = '__all__'


class MedicineConflictSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicineConflict
        fields = '__all__'


class EntranceSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    currency_name = serializers.SerializerMethodField()
    entrance_image = serializers.SerializerMethodField()
    entrance_total = serializers.SerializerMethodField()

    def get_entrance_total (self, obj):
        total = list(EntranceThrough.objects.filter(entrance=obj.id).aggregate(Sum('total_purchaseـcurrency')).values())[0]
        return total

    def get_entrance_image(self, obj):
        entrance_image_obj = EntranceImage.objects.filter(entrance=obj.id)
        json_entrance_image = EntranceImageSeriazlier(
            entrance_image_obj, many=True)
        return json_entrance_image.data

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    def get_currency_name(self, obj):
        return obj.currency.name

    class Meta:
        model = Entrance
        fields = '__all__'


class EntranceImageSeriazlier(serializers.ModelSerializer):
    class Meta:
        model = EntranceImage
        fields = '__all__'
class PrescriptionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionImage
        fields = '__all__'


class EntranceThroughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    medicine_min_expire = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_description (self, res):
        return res.entrance.description

    def get_medicine_full(self, res):
        obj = res.medician
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ''
        ml = ''
        weight = ''
        if (obj.kind and obj.kind.name_english):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "} "
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + ml + ' ' + big_company_name + country_name + " " + weight

    def get_medicine_min_expire(self, obj):
        return obj.medician.min_expire_date

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = EntranceThrough
        fields = '__all__'


class EntranceThroughExpiresSerializer(serializers.ModelSerializer):
    medician = MedicianSeralizer()

    class Meta:
        model = EntranceThrough
        fields = ('medician',)


class StoreSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = Store
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = Currency
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class FinalRegisterSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = FinalRegister
        fields = '__all__'


class DoctorNameSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    code_name = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    def get_code_name(self, obj):
        return str(obj.id) + "." + obj.name

    class Meta:
        model = DoctorName
        fields = '__all__'


class PatientNameSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    code_name = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    def get_code_name(self, obj):
        return str(obj.id) + "." + obj.name

    class Meta:
        model = PatientName
        fields = '__all__'


class PurchaseListManualSerializer (serializers.ModelSerializer):
    medicine_full = serializers.SerializerMethodField()
    existence = serializers.SerializerMethodField()
    details_1 = serializers.SerializerMethodField()
    details_2 = serializers.SerializerMethodField()
    details_3 = serializers.SerializerMethodField()

    def get_details_1(self, obj):
        queryset = (EntranceThrough.objects.filter(medician=obj.medicine).order_by("-id").values('entrance__company__name',
                    'entrance__company__market__name', 'quantity_bonus', 'each_price', 'entrance__currency__name', 'timestamp', 'entrance__wholesale'))[0:1]
        data = list(queryset)
        return data

    def get_details_2(self, obj):
        queryset = (EntranceThrough.objects.filter(medician=obj.medicine).order_by("-id").values('entrance__company__name',
                    'entrance__company__market__name', 'quantity_bonus', 'each_price', 'entrance__currency__name', 'timestamp', 'entrance__wholesale'))[1:2]
        data = list(queryset)
        return data

    def get_details_3(self, obj):
        queryset = (EntranceThrough.objects.filter(medician=obj.medicine).order_by("-id").values('entrance__company__name',
                    'entrance__company__market__name', 'quantity_bonus', 'each_price', 'entrance__currency__name', 'timestamp', 'entrance__wholesale'))[2:3]
        data = list(queryset)
        return data

    def get_existence(self, obj):
        return obj.medicine.existence

    def get_medicine_full(self, res):
        obj = res.medicine
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ""
        ml = ''
        weight = ''
        if (obj.kind and obj.kind.name_english):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "} "
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + ml + ' ' + big_company_name + country_name + " " + weight

    class Meta:
        model = PurchaseListManual
        fields = '__all__'


class PrescriptionThroughSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    medicine_cautions = serializers.SerializerMethodField()
    medicine_usage = serializers.SerializerMethodField()
    medicine_full = serializers.SerializerMethodField()
    medicine_no_box = serializers.SerializerMethodField()
    medicine_no_quantity = serializers.SerializerMethodField()
    prescription_number = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()

    def get_department_name (self, res):
        return res.prescription.department.name

    def get_prescription_number (self, res):
        return res.prescription.prescription_number

    def get_medicine_full(self, res):
        obj = res.medician
        kind_name = ""
        country_name = ""
        big_company_name = ''
        generics = ""
        ml = ''
        weight = ''
        if (obj.kind and obj.kind.name_english):
            kind_name = obj.kind.name_english + "."
        if (obj.country):
            country_name = obj.country.name
        if (obj.big_company):
            big_company_name = obj.big_company.name + " "
        if (obj.generic_name):
            generics = "{" + str(",".join(map(str, obj.generic_name))) + "} "
        if (obj.ml):
            ml = obj.ml
        if (obj.weight):
            weight = obj.weight

        return kind_name + obj.brand_name + ' ' + ml + ' ' + generics + big_company_name + country_name + " " + weight

    def get_medicine_cautions(self, obj):
        if (obj.medician.cautions):
            return obj.medician.cautions
        else:
            return ""
        
    def get_medicine_no_box(self, obj):
        if (obj.medician.no_box):
            return obj.medician.no_box
        else:
            return ""
        
    def get_medicine_no_quantity(self, obj):
        if (obj.medician.no_pocket):
            return obj.medician.no_pocket
        else:
            return ""


    def get_medicine_usage(self, obj):
        if (obj.medician.usages):
            return obj.medician.usages
        else:
            return ""

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = PrescriptionThrough
        fields = '__all__'


class OutranceSerializer (serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = Outrance
        fields = '__all__'


class OutranceThroughSerializer (serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, res):
        if (res.user and res.user.first_name):
            return res.user.first_name
        else: return ''

    class Meta:
        model = OutranceThrough
        fields = '__all__'


class TrazSerializer (serializers.Serializer):
    entrances = EntranceThroughSerializer(many=True)
    prescriptions = PrescriptionThroughSerializer(many=True)
