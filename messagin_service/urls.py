from django.urls import path
from messagin_service.apps import MessaginServiceConfig
from messagin_service.views import (HomeListView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
                                    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
                                    MailingsListView, MailingsCreateView, MailingsUpdateView, MailingsDeleteView)

app_name = MessaginServiceConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailings/', MailingsListView.as_view(), name='mailings_list'),
    path('mailings/create/', MailingsCreateView.as_view(), name='mailings_create'),
    path('mailings/<int:pk>/update/', MailingsUpdateView.as_view(), name='mailings_update'),
    path('mailings/<int:pk>/delete/', MailingsDeleteView.as_view(), name='mailings_delete')
]
