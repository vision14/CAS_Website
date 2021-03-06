from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Argentina/', views.argentina, name='argentina'),
    path('Australia/', views.australia, name='australia'),
    path('Brazil/', views.brazil, name='brazil'),
    path('Canada/', views.canada, name='canada'),
    path('China/', views.china, name='china'),
    path('Germany/', views.germany, name='germany'),
    path('India/', views.india, name='india'),
    path('Iran/', views.iran, name='iran'),
    path('Italy/', views.italy, name='italy'),
    path('Mexico/', views.mexico, name='mexico'),
    path('Philippines/', views.philippines, name='philippines'),
    path('Russia/', views.russia, name='russia'),
    path('South_Africa/', views.south_africa, name='south_africa'),
    path('Spain/', views.spain, name='spain'),
    path('UK/', views.uk, name='uk'),
    path('USA/', views.usa, name='usa'),
    path('World_Table/', views.world_table, name='world_table'),
    path('Argentina_Table/', views.argentina_table, name='argentina_table'),
    path('Australia_Table/', views.australia_table, name='australia_table'),
    path('Brazil_Table/', views.brazil_table, name='brazil_table'),
    path('Canada_Table/', views.canada_table, name='canada_table'),
    path('china_Table/', views.china_table, name='china_table'),
    path('Germany_Table/', views.germany_table, name='germany_table'),
    path('India_Table/', views.india_table, name='india_table'),
    path('Iran_Table/', views.iran_table, name='iran_table'),
    path('Italy_Table/', views.italy_table, name='italy_table'),
    path('Mexico_Table/', views.mexico_table, name='mexico_table'),
    path('Philippines_Table/', views.philippines_table, name='philippines_table'),
    path('Russia_Table/', views.russia_table, name='russia_table'),
    path('South_Africa_Table/', views.south_africa_table, name='south_africa_table'),
    path('Spain_Table/', views.spain_table, name='spain_table'),
    path('UK_Table/', views.uk_table, name='uk_table'),
    path('USA_Table/', views.usa_table, name='usa_table'),
]
