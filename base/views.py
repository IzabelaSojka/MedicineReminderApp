from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from .models import Medicine, Medicine_Database
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
import datetime, json, requests, csv
from django.core.mail import send_mail
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse


email_from = settings.EMAIL_HOST_USER

resgistration  = ['eJpFgoCQTvLEt2mw23z1E2:APA91bFw025vdOxma7LIZxeKrGRrT92iMWNrRWsda36LKKNj7teGVILMJrBor2shqk59Bp36aKFbj4bdkOFOZpzbVYASCtbQO6P1-aEHkTqbOcelDuWeHN9AfMbL3VEbROj6Q27WXU8X']

def send_notification(registration_ids, message_title, message_desc):
    fcm_api = "AAAArdMC7LQ:APA91bGuyDN5NnRPVkl5FPMIdMMiaY1hTa_KoaSqGVlu7gVDl7BgwXg9f9Y84ugnOBcL6L-EPxHVvOUvEEE3SJnz8NbejtNzWGirsb5xjafP9TyZ8CLogDcvbi3GjpGmGkeaZoiG79pV"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key=' + fcm_api}

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "notification": {
            "body": message_desc,
            "title": message_title,
            "icon": "https://static.ktomalek.pl/blog/zdjecie/leki-zagrozone-brakiem-dostepnosci-maj-2018.jpg",
        }
    }

    result = requests.post(url, data=json.dumps(payload), headers=headers)
    print(result.json())

def load_database():
    with open('files/Rejestr_Produktow_Leczniczych_calosciowy_stan_na_dzien_20220108.csv', 'r',
              encoding='utf8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        medicines = []
        for row in csvreader:
            medicine = Medicine_Database(
                name=row[1],
                name2=row[2],
                power=row[3],
                form=row[4],
                active_substance=row[5],
                leaflet=row[6],
                characteristics=row[7]
            )
            medicines.append(medicine)
            if len(medicines) > 10000:
                Medicine_Database.objects.bulk_create(medicines)
                medicines = []
        if medicines:
            Medicine_Database.objects.bulk_create(medicines)


def check(data):
    info = 0
    with open('files/Rejestr_Produktow_Leczniczych_calosciowy_stan_na_dzien_20220108.csv', 'r',
              encoding='utf8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')

        for row in csvreader:
            if data == row['Nazwa Produktu Leczniczego']:
                info = 1
                break
    return info


def leaflet_search(data):
    leaflet = ''
    with open('files/Rejestr_Produktow_Leczniczych_calosciowy_stan_na_dzien_20220108.csv', 'r',
              encoding='utf8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')

        for row in csvreader:
            if data == row['Nazwa Produktu Leczniczego']:
                leaflet = row['Ulotka']
                break

    return leaflet


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('medicines')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('medicines')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('medicines')
        return super(RegisterPage, self).get(*args, **kwargs)


class MedicineList(LoginRequiredMixin, ListView):
    model = Medicine
    context_object_name = 'medicines'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medicines'] = context['medicines'].filter(user=self.request.user)
        return context


class MedicineDetail(LoginRequiredMixin, DetailView):
    model = Medicine
    context_object_name = 'medicines'


class MedicineCreate(LoginRequiredMixin, CreateView):
    model = Medicine
    fields = ['name', 'time', 'dose', 'package', 'how_much', 'description', 'mail']
    success_url = reverse_lazy('medicines')

    def form_valid(self, form):
        if check(form.instance.name) == 1:
            form.instance.leaflet = leaflet_search(form.instance.name)
            form.instance.user = self.request.user
            if form.instance.how_much != 0 and form.instance.package != 0:
                form.instance.doses = form.instance.how_much * form.instance.package
            messages.success(self.request, "success")
            # email(form.instance.mail, form.instance.name)
            return super(MedicineCreate, self).form_valid(form)
        else:
            messages.success(self.request, "warning")
            return super(MedicineCreate, self).form_invalid(form)


class MedicineEdit(LoginRequiredMixin, UpdateView):
    model = Medicine
    fields = ['time', 'dose', 'package', 'how_much', 'description']
    success_url = reverse_lazy('medicines')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.doses = form.instance.how_much * form.instance.package

        return super(MedicineEdit, self).form_valid(form)


class MedicineDelete(LoginRequiredMixin, DeleteView):
    model = Medicine
    context_object_name = 'medicines'
    success_url = reverse_lazy('medicines')


def send_email():
    model = Medicine.objects.all()
    now = datetime.datetime.now()
    time_2 = now.strftime('%H:%M')
    for element in model:
        if element.time != '' and element.mail != '':
            if time_2 == element.time:
                subject = 'You need to take the medicine: ' + element.name
                message = 'Hello, \n\nReminder of the medicine \nYour description this medicine: ' + element.description + '\n\nRegards'
                send_mail(subject, message, email_from, [element.mail, ])


class MedicineDatabaseList(ListView):
    model = Medicine_Database
    context_object_name = 'medicinesDatabase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['medicinesDatabase'] = context['medicinesDatabase'].filter(name__startswith=search_input)

        context['search_input'] = search_input
        return context


class MedicineDatabaseDetail(DetailView):
    model = Medicine_Database
    context_object_name = 'medicinesDatabase'

def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/9.6.6/firebase-app-compat.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/9.6.6/firebase-messaging-compat.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyAJDi3BCXf5wwG2DznqSHwc4pweV9UTfl8",' \
           '        authDomain: "djangoproject1-38221.firebaseapp.com",' \
           '        projectId: "djangoproject1-38221",' \
           '        storageBucket: "djangoproject1-38221.appspot.com",' \
           '        messagingSenderId: "746569526452",' \
           '        appId: "1:746569526452:web:ebcf8c50cc08a6320bbbe1",' \
           '        measurementId: "G-0SYDDVQ6VP"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.onMessage((payload) => {' \
           '    console.log( payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")


def verif_notification():
    model = Medicine.objects.all()
    now = datetime.datetime.now()
    now = now.strftime('%H:%M')
    for element in model:
        time = str(element.time)
        if now in time:
            subject = 'Musisz wziąć lek: ' + element.name
            message = 'Dawka: ' + str(element.dose)
            send_mail(subject, message, email_from, [element.mail, ])
            send_notification(resgistration, subject, message)
            element.doses = element.doses - element.dose
            doses2 = element.doses / element.dose
            element.notification1 = 1
            if doses2 <= 5:
                subject = 'KONIEC LEKU: ' + element.name
                message = 'Liczba pozostałych dawek: ' + str(doses2)
                send_mail(subject, message, email_from, [element.mail, ])
                send_notification(resgistration, subject, message)
                element.notification2 = 1
        else:
            element.notification1 = 0
            element.notification2 = 0
        element.save()


sched = BackgroundScheduler(daemon=True)
sched.add_job(verif_notification, 'interval', seconds=60)
sched.start()

