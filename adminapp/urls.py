from django.urls import path
from adminapp import views
from .views import AccessKeyListView
from .apiviews import GetActiveAccessKey

app_name = 'adminapp'

urlpatterns = [
    path('feed/', AccessKeyListView.as_view(), name='access_key_list'),
    path('generate/<int:school_id>/', views.access_key_generate, name='access_key_generate'),
    path('update/<int:access_key_id>/', views.access_key_update, name='access_key_update'),
    path('revoke/<int:access_key_id>/', views.revoke_key, name='access_key_revoke'),
    path('acess_key_info/', GetActiveAccessKey.as_view(), name='access_key_info'),
    
]