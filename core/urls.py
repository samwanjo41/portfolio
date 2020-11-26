from django.urls import path
from core.views import home, ProjectDetailView, premium, project, checkout

urlpatterns = [
    path('', home, name='home'),
    path('project/<int:pk>/', project, name='project'),
    path('premium/', premium, name='premium'),
    path('checkout/', checkout, name='checkout')
   
]