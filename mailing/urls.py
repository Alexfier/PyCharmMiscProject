from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (DisabledMailingView, HomeView, MailingCreateView, MailingDeleteView, MailingDetailsView,
                           MailingListView, MailingReportView, MailingSendView, MailingUpdateView, MainPageView,
                           MessageCreateView, MessageDeleteView, MessageDetailsView, MessageListView,
                           MessageUpdateView, RecipientCreateView, RecipientDeleteView, RecipientDetailsView,
                           RecipientListView, RecipientUpdateView)

app_name = MailingConfig.name

urlpatterns = [
    path('recipients/', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>/', RecipientDetailsView.as_view(), name='recipient'),
    path("new/recipient/", RecipientCreateView.as_view(), name="recipient_create"),
    path("update/recipient/<int:pk>/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("delete/recipient/<int:pk>/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailsView.as_view(), name='message'),
    path("new/message/", MessageCreateView.as_view(), name="message_create"),
    path("update/message/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("delete/message/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailsView.as_view(), name='mailing'),
    path("new/mailing/", MailingCreateView.as_view(), name="mailing_create"),
    path("update/mailing/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("delete/mailing/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailing_send/<int:pk>/", MailingSendView.as_view(), name="mailing_send"),
    path("mailing_report/<int:pk>/", MailingReportView.as_view(), name="mailing_report"),
    path("main_page/", MainPageView.as_view(), name="main_page"),
    path("", HomeView.as_view(), name="home"),
    path("disabling_mailing/<int:pk>/", DisabledMailingView.as_view(), name="disabling_mailing"),
]
