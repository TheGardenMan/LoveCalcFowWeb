from django.urls import path
from LoveCalcApp import views
urlpatterns = [
    path('',views.register),
    path('dashboard/',views.dashboard),
    path('dashboard/<secret_hash_of_owner>',views.dashboard),
    path('calc/',views.calculate),
    path('calc/<owner_id>',views.calculate),

]
