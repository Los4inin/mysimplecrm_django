from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^contacts/$', views.ContactListView.as_view(), name='contacts'),
    url(r'^contact/(?P<pk>\d+)$', views.ContactDetailView.as_view(), name='contact-detail'),
    url(r'^contact/create/$', views.ContactCreate.as_view(), name='contact_create'),
    url(r'^contact/(?P<pk>\d+)/update/$', views.ContactUpdate.as_view(), name='contact_update'),

    url(r'^projects/$', views.ProjectListView.as_view(), name='projects'),
    url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project-detail'),
    url(r'^project/create/$', views.ProjectCreate.as_view(), name='project_create'),
    url(r'^project/(?P<pk>\d+)/update/$', views.ProjectUpdate.as_view(), name='project_update'),

    url(r'^projects_active/$', views.ProjectActiveListView.as_view(), name='projects_active'),

    url(r'^accounts/$', views.AccountListView.as_view(), name='accounts'),
    url(r'^account/(?P<pk>\d+)$', views.AccountDetailView.as_view(), name='account-detail'),
    url(r'^account/create/$', views.AccountCreate.as_view(), name='account_create'),
    url(r'^account/(?P<pk>\d+)/update/$', views.AccountUpdate.as_view(), name='account_update'),

    url(r'^accounts/search/', views.AccountSearchView.as_view(), name='account_search'),
    url(r'^contacts/search/', views.ContactSearchView.as_view(), name='contact_search'),
    url(r'^projects/search/', views.ProjectSearchView.as_view(), name='project_search'),

    url(r'^notes/$', views.NoteListView.as_view(), name='notes'),
    url(r'^notes_today/$', views.NoteTodayListView.as_view(), name='notes_today'),
    url(r'^note/(?P<pk>\d+)$', views.NoteDetailView.as_view(), name='note_detail'),
    url(r'^note/create/$', views.NoteCreate.as_view(), name='note_create'),
    url(r'^note/(?P<pk>\d+)/update/$', views.NoteUpdate.as_view(), name='note_update'),
]
