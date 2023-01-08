from django.urls import path 

from .views import PrescriptionView, PharmGroupView, CountryView, KindView

urlpatterns = [ 
    path('prescription', PrescriptionView.as_view()),
    path('kind', KindView.as_view()),
    path('pharm-groub', PharmGroupView.as_view()),
    path('country', CountryView.as_view())
]