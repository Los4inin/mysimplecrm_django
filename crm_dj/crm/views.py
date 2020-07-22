from django.shortcuts import render

# Create your views here.
from .models import Account, Contact, Project, Relation, Region, Note
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
import datetime

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_accounts=Account.objects.all().count()
    num_contacts=Contact.objects.all().count()
    num_projects=Project.objects.all().count()
    num_notes=Note.objects.all().count()

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_accounts':num_accounts,'num_contacts':num_contacts,'num_projects':num_projects},
    )

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class ContactListView(LoginRequiredMixin, generic.ListView):
    login_url = '/users/login/'
    permission_denied_message = 'To view information in CRM please Log-In'
    model = Contact
    paginate_by = 30 # 30 записей на страницу
class ContactDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/users/login/'
    permission_denied_message = 'To view information in CRM please Log-In'
    model = Contact

class ProjectListView(LoginRequiredMixin, generic.ListView):
    login_url = '/users/login/'
    permission_denied_message = 'To view information in CRM please Log-In'
    model = Project
    paginate_by = 30 # 30 записей на страницу
class ProjectActiveListView(ProjectListView):
    queryset = Project.objects.filter(status='A')


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/users/login/'
    permission_denied_message = 'To view information in CRM please Log-In'
    model = Project

class AccountListView(LoginRequiredMixin, generic.ListView):
    login_url = '/users/login/'
    permission_denied_message = 'To view information in CRM please Log-In'
    model = Account
    paginate_by = 30 # 30 записей на страницу
class AccountDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/users/login/'
    permission_denied_message = 'To view information in CRM please Log-In'
    model = Account


class AccountCreate(CreateView):
    model = Account
    fields = '__all__'
    success_url = reverse_lazy('accounts')

class AccountUpdate(UpdateView):
    model = Account
    fields = '__all__'
    success_url = reverse_lazy('accounts')

class ContactCreate(CreateView):
    model = Contact
    fields = '__all__'
    success_url = reverse_lazy('contacts')

class ContactUpdate(UpdateView):
    model = Contact
    fields = '__all__'
    success_url = reverse_lazy('contacts')

class ProjectCreate(CreateView):
    model = Project
    fields = '__all__'
    success_url = reverse_lazy('projects')

class ProjectUpdate(UpdateView):
    model = Project
    fields = '__all__'
    success_url = reverse_lazy('projects')

from django.db.models import Q


class AccountSearchView(generic.ListView):
    model = Account
    template_name = 'account_search.html'

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        q_title = query.title()
        q_upper = query.upper()
        object_list = Account.objects.filter(
            Q(company_name__icontains=query) | Q(code__icontains=query) | Q(company_name__icontains=q_title)
        | Q(company_name__icontains=q_upper) | Q(relation__icontains=query))
        return object_list

class ContactSearchView(generic.ListView):
    model = Contact
    template_name = 'contact_search.html'

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        q_title = query.title()
        object_list = Contact.objects.filter(
            Q(surname__icontains=query) | Q(firstname__icontains=query) |
            Q(surname__icontains=q_title) | Q(firstname__icontains=q_title)
        )
        return object_list

class ProjectSearchView(generic.ListView):
    model = Project
    template_name = 'project_search.html'

    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        q_title = query.title()
        object_list = Project.objects.filter(
            Q(name__icontains=query) | Q(name__icontains=q_title))
        return object_list

class NoteListView(LoginRequiredMixin, generic.ListView):
    login_url = '/users/login/'
    permission_denied_message = 'To view information in CRM please Log-In'
    model = Note
    paginate_by = 30 # 30 записей на страницу
class NoteTodayListView(NoteListView):
    queryset = Note.objects.filter(reminder_date=datetime.date.today())

class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/users/login/'
    permission_denied_message = 'To view information in CRM please Log-In'
    model = Note

class NoteCreate(CreateView):
    model = Note
    fields = '__all__'
    success_url = reverse_lazy('notes')

class NoteUpdate(UpdateView):
    model = Note
    fields = '__all__'
    success_url = reverse_lazy('notes')
