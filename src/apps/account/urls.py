from django.urls import path
from . import views

app_name = 'apps.account'
urlpatterns = [
    # login logout and register
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),

    path('user/<int:user_id>/detail', views.UserDetail.as_view(), name='user_detail'),
    path('user/<str:phonenumber>/is-exists', views.UserIsExists.as_view(), name='user_is_exists'),
    path('user/<str:phonenumber>/detail/json', views.UserDetailJson.as_view(), name='user_detail_json'),
]
