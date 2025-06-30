from django.urls import path
from main_app.views import pages_views as views


urlpatterns = [
   path('sign-to-text/', views.sign_to_text_view, name='sign_to_text'),]