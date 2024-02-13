from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('richmond/', views.richmond, name='richmond'),
    path('kingston/', views.kingston, name='kingston'),
    path('elmbridge/', views.elmbridge, name='elmbridge'),
    path('southwark/', views.southwark, name='southwark'),
    path('guildford/', views.guildford, name='guildford'),
    path('epsom/', views.epsom, name='epsom'),
    path('woking/', views.woking, name='woking'),
    path('bromley/', views.bromley, name='bromley'),
    path('merton/', views.merton, name='merton'),
    path('lewisham/', views.lewisham, name='lewisham'),
    path('kensington_chelsea/', views.kensington_chelsea, name='kensington_chelsea'),
    path('hammersmith_fulham/', views.hammersmith_fulham, name='hammersmith_fulham'),
    path('view_results/<int:pk>/', views.view_results, name='view_results'),
    path('reviews', views.reviews, name='reviews'),
    path('delete_scrape/<int:pk>/', views.delete_scrape, name='delete_scrape'),
    path('download_spreadsheet/<int:pk>/', views.download_spreadsheet, name='download_spreadsheet'),
    path('pricing', views.pricing, name='pricing'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('bots', views.results, name='bots'),
    path('deleteword/<int:pk>/<str:redirect_to>/', views.deleteword, name='deleteword'),
]