from django.db import models
from django.urls import reverse #чтобы генерировать URLs by reversing the URL patterns
import datetime as dt
#from datetime import date, datetime
# Create your models here.
class Relation(models.Model):
    # Связь компании по направлению деятельности: металлообработка металлургия ЗМК лист шлифовка сборка экструзия сварка
    name = models.CharField(max_length=30, help_text="Relation: металлообработка металлургия ЗМК..")
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=30, help_text="Регион компании")
    def __str__(self):
        return self.name

def clean_img_url(url): # костыль, чтобы подготовить ссылки на картинки, чтобы они правильно обображались
    if url.startswith('crm'): url=url[3:]
    else: url='/'+url
    return url

class Account(models.Model):
    #img_acc = models.FileField(upload_to='crm/static/imgacc/', default='static/imgacc/0.png')
    img_acc = models.CharField(max_length=32, default='static/imgacc/0.png')
    def get_img_url(self):
        return clean_img_url(str(self.img_acc))
    code = models.CharField(max_length=6) # GASPRO
    company_name = models.CharField(max_length=100)
    parent_acc_id = models.PositiveSmallIntegerField(null=True, blank=True)
    inn = models.CharField(max_length=10, blank=True)
    www = models.CharField(max_length=100, blank=True)
    tel1 = models.CharField(max_length=50, blank=True)
    tel2 = models.CharField(max_length=50, blank=True)
    email1 = models.EmailField(max_length=50, blank=True)
    email2 = models.EmailField(max_length=50, blank=True)


    ## owner = models.ForeignKey('UserName', on_delete=models.SET_NULL, null=True)

    # выбор типа поставщик производитель и тд
    TYPE_CHOICES = ( ('C', 'CUSTOMER'), ('D', 'DEALER'), ('P', 'PRODUCER'), ('S', 'SERVIS'), )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='C',)

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    relation = models.CharField(max_length=150, blank=True)

    create_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)

    class Meta: # Класс мета задает сортировку по умолчанию
        ordering = ['-mod_date']

    def get_absolute_url(self):
        return reverse('account-detail', args=[str(self.id)])
    def get_update_url(self):
        return reverse('account-detail', args=[str(self.id)])+'/update/'

    def __str__(self):
        return self.company_name

    def get_fin_by_inn(self):
        import sqlite3
        conn_fin_data = sqlite3.connect("./fin_data.db")
        cursor_fin_data = conn_fin_data.cursor()
        cursor_fin_data.execute('SELECT year, revenue FROM inn_revenue WHERE inn = ?', (self.inn,))
        fin_data = cursor_fin_data.fetchall()
        cursor_fin_data.close()
        fin_data_mln = list()
        for entry in fin_data:
            fin_data_mln.append((entry[0],int(entry[1])//1000)) # переводим фин данные в млн руб
        return fin_data_mln

    def get_local_time(self):
        region_id = self.region.id
        kalt = {39}
        samt = {30, 34, 63, 64, 73, 18}
        yekt = {2, 45, 56, 59, 66, 72, 74, 86, 89}
        omst = {55}
        krat = {4, 17, 19, 22, 24, 42, 54, 70}
        irkt = {3, 38}
        yakt = {14, 28, 75}
        vlat = {25, 27, 79}
        magt = {65}
        pett = {87, 41}
        time_zone = 3
        if region_id in kalt: time_zone = 2
        if region_id in samt: time_zone = 4
        if region_id in yekt: time_zone = 5
        if region_id in omst: time_zone = 6
        if region_id in krat: time_zone = 7
        if region_id in irkt: time_zone = 8
        if region_id in yakt: time_zone = 9
        if region_id in vlat: time_zone = 10
        if region_id in magt: time_zone = 11
        if region_id in pett: time_zone = 12

        local_time = str((dt.datetime.utcnow() + dt.timedelta(hours=time_zone)).time())[:-10]

        return local_time


class Contact(models.Model):
    # модель описания контактов
    #img_cont = models.FileField(upload_to='crm/static/imgcont/', default='static/imgcont/0.png')
    img_cont = models.CharField(max_length=32, default='static/imgcont/0.png')
    def get_img_url(self):
        return clean_img_url(str(self.img_cont))

    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50, blank=True)
    middlename = models.CharField(max_length=50, blank=True)
    job = models.CharField(max_length=100, blank=True) # должность
    appeal = models.CharField(max_length=100, blank=True) # обращение в РодПадеж

    tel1 = models.CharField(max_length=50, blank=True)
    tel2 = models.CharField(max_length=50, blank=True)
    email1 = models.EmailField(max_length=50, blank=True)
    email2 = models.EmailField(max_length=50, blank=True)

    parent_acc = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    ## owner = models.ForeignKey('UserName', on_delete=models.SET_NULL, null=True)

    # выбор пола
    SEX_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='M',)
    create_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)

    class Meta: # Класс мета задает сортировку по умолчанию
        ordering = ['-mod_date']

    def __str__(self):
        return '%s, %s' % (self.surname, self.firstname)

    def get_absolute_url(self):
        return reverse('contact-detail', args=[str(self.id)])
    def get_update_url(self):
        return reverse('contact-detail', args=[str(self.id)])+'/update/'


class Project(models.Model): # модель описания проектов
    #img_proj = models.FileField(upload_to='crm/static/imgproj/', default='static/imgproj/0.png')
    img_proj = models.CharField(max_length=32, default='static/imgproj/0.png')
    def get_img_url(self):
        return clean_img_url(str(self.img_proj))

    name = models.CharField(max_length=200)
    parent_acc = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    parent_cont = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    producer_id = models.PositiveSmallIntegerField(null=True, blank=True)
    agent_id = models.PositiveSmallIntegerField(null=True, blank=True)

    ## owner = models.ForeignKey('UserName', on_delete=models.SET_NULL, null=True)

    create_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)

    TYPE_CHOICES = ( ('A', 'ACTIVE'), ('C', 'CLOSED'), ('F', 'FINISHED'), )
    status = models.CharField(max_length=1, choices=TYPE_CHOICES, default='A',)

    class Meta: # Класс мета задает сортировку по умолчанию
        ordering = ['-mod_date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])
    def get_update_url(self):
        return reverse('project-detail', args=[str(self.id)])+'/update/'

class Note(models.Model):
    parent_acc = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    parent_cont = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    parent_proj = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    reminder_date = models.DateField(default=dt.date.today)
    class Meta: # Класс мета задает сортировку по умолчанию
        ordering = ['-reminder_date']
    def get_absolute_url(self):
        return reverse('note_detail', args=[str(self.id)])
    def get_update_url(self):
        return reverse('note_detail', args=[str(self.id)])+'/update/'
