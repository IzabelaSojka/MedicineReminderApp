from django.db import models
from django.contrib.auth.models import User

class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(("Nazwa"),max_length=100)
    time = models.CharField(("Godzina wzięcia"),max_length=255, null=True, blank=True)
    dose = models.IntegerField(("Jednorazowa dawka"), null=True, blank=True)
    doses = models.IntegerField(("Liczba dostępnych dawek"), null=True, blank=True)
    package = models.IntegerField(("Liczba posiadanych opakowań"), null=True, blank=True)
    how_much = models.IntegerField(("Wielkość opakowania"), null=True, blank=True)
    mail = models.EmailField(("Email"), null=True, blank=True)
    leaflet = models.CharField(("Ulotka"),max_length=100, null=True, blank=True)
    description = models.TextField(("Notatka"), null=True, blank=True)
    notification1 = models.IntegerField(("Powiadomienie1"), null=True, blank=True)
    notification2 = models.IntegerField(("Powiadomienie2"), null=True, blank=True)

    def __str__(self):
        return self.name


class Medicine_Database(models.Model):

    name = models.CharField(("Nazwa Leku"), max_length=255)
    name2 = models.CharField(("Nazwa powszechnie stosowana"), max_length=255)
    power = models.CharField(("Moc"), max_length=255)
    form = models.CharField(("Postać farmaceutyczna"), max_length=255)
    active_substance = models.CharField(("Substancja czynna"), max_length=255)
    leaflet = models.CharField(("Ulotka"), max_length=100, null=True, blank=True)
    characteristics = models.CharField(("Charakterystyka"), max_length=255)

    def __str__(self):
        return self.name
