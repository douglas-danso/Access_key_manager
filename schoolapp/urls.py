from django.urls import path

from schoolapp import views
app_name = 'schoolapp'

urlpatterns = [
    path('access-keys/<int:school_id>/',views.access_key_list, name='access_key_list'),
    # path('school/', views.school_view, name='school'),
    path('purchase/<int:school_id>/', views.purchase_key, name='purchase_key'),
    
] 

