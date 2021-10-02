from django.urls import path
from api import views

urlpatterns = [
    path('driver-standings/<slug:year_slug>/', views.getF1DriverStandings),
    path('constructor-standings/<slug:year_slug>/', views.getF1ConstructorStandings),
    path('drivers/<slug:year_slug>/', views.getF1Drivers),
    path('constructors/<slug:year_slug>/', views.getF1Constructors),
    path('circuits/<slug:year_slug>/', views.getF1Circuits),
    path('seasons/', views.getF1Seasons),
    path('results/<slug:year_slug>/', views.getF1Results),
    path('results/<slug:year_slug>/<slug:round_slug>/', views.getF1ResultsRound),
    path('qualifying/<slug:year_slug>/<slug:round_slug>/', views.getF1QualifyingResults),
    path('schedule/<slug:year_slug>/', views.getF1Schedule),
]
