from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from messagin_service.models import Recipient, Message, Mailings
from django.urls import reverse_lazy
from messagin_service.forms import ClientForm

class HomeListView(ListView):
    model = Recipient
    template_name = 'messagin_service/home.html'


class ClientListView(ListView):
    model = Recipient
    template_name = 'messagin_service/client_list.html'


class ClientCreateView(CreateView):
    model = Recipient
    form_class = ClientForm
    template_name = 'messagin_service/client_form.html'
    success_url = reverse_lazy('messagin_service:client_list')


class ClientUpdateView(UpdateView):
    model = Recipient
    form_class = ClientForm
    template_name = 'messagin_service/client_form.html'
    success_url = reverse_lazy('messagin_service:client_list')


class ClientDeleteView(DeleteView):
    model = Recipient
    template_name = "messagin_service/client_confirm_delete.html"
    success_url = reverse_lazy('messagin_service:client_list')


class MessageListView(ListView):
    model = Message
    template_name = 'messagin_service/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'messagin_service/message_form.html'
    success_url = reverse_lazy('messagin_service:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'messagin_service/message_form.html'
    success_url = reverse_lazy('messagin_service:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "messagin_service/message_confirm_delete.html"
    success_url = reverse_lazy('messagin_service:message_list')


class MailingsListView(ListView):
    model = Mailings
    template_name = 'messagin_service/mailings_list.html'


class MailingsCreateView(CreateView):
    model = Mailings
    fields = ['date_first', 'date_end', 'status', 'message', 'recipient']
    template_name = 'messagin_service/mailings_form.html'
    success_url = reverse_lazy('messagin_service:mailings_list')


class MailingsUpdateView(UpdateView):
    model = Mailings
    fields = ['date_first', 'date_end', 'status', 'message', 'recipient']
    template_name = 'messagin_service/mailings_form.html'
    success_url = reverse_lazy('messagin_service:mailings_list')


class MailingsDeleteView(DeleteView):
    model = Mailings
    template_name = "messagin_service/mailings_confirm_delete.html"
    success_url = reverse_lazy('messagin_service:mailings_list')
