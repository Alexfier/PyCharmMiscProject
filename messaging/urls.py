from django.urls import path
from .views import (
    AttemptListView,
    ClientCreateView,
    ClientDeleteView,  # Добавлено
    ClientListView,
    ClientUpdateView,  # Добавлено
    DisableMailingView,
    FinishMailingView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingSendView,
    MailingUpdateView,  # Добавлено
    MessageCreateView,
    MessageDeleteView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
    MessagingHomeView,
    ToggleUserStatusView,
    UserListView,
    UserMailingsView,
)
from .apps import MessagingConfig

app_name = MessagingConfig.name

urlpatterns = [
    # Mailing URLs
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path(
        "mailings/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailings/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("mailings/<int:pk>/send/", MailingSendView.as_view(), name="mailing_send"),
    path(
        "mailings/<int:pk>/disable/",
        DisableMailingView.as_view(),
        name="disable_mailing",
    ),
    path(
        "mailings/<int:pk>/finish/", FinishMailingView.as_view(), name="finish_mailing"
    ),
    path("mailings/", UserMailingsView.as_view(), name="user_mailings"),
    # Client URLs
    path("clients/", ClientListView.as_view(), name="client_list"),
    path("clients/create/", ClientCreateView.as_view(), name="client_create"),
    path("clients/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    # Message URLs
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path(
        "messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    # Attempt URLs
    path("attempts/", AttemptListView.as_view(), name="attempt_list"),
    # User URLs
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/toggle/", ToggleUserStatusView.as_view(), name="toggle_user"),
    # Home URL
    path("", MessagingHomeView.as_view(), name="home"),
]
