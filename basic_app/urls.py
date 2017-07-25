from django.conf.urls import url
from basic_app import views

from .views import IndexView, SettingsView, UsersList110, UsersList110Json


#TEMPLATE URLS
app_name = 'basic_app'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^settings/$', SettingsView.as_view(), name="user_settings"),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^datatables_110$', UsersList110.as_view(), name="datatables_110"),
    url(r'^users_data_110/$', UsersList110Json.as_view(), name="users_list_json_110"),
    url(r'^profiles/create/$', views.profile_create, name='profile_create'),
    url(r'^export/csv/$', views.export, name='export_users_csv'),
    url(r'^import/csv/$', views.import_data, name='import'),

    url(r'^profiles/$', views.ProfileHandsome.as_view(), name='vasya kolya'),
    url(r'^profiles/delete/$', views.ProfileDelete.as_view(), name='profile_delete'),
    url(r'^profiles/create/$', views.ProfileCreate.as_view(), name='profile_create'),


    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
    url(r'^verokey_create/$', views.vero_key_create, name='verokey_create'),
    url(r'^table_sort$', views.TableSortData.as_view(), name='table_sort'),
]

