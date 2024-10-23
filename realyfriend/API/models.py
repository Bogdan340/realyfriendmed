from django.db import models

class info_company(models.Model):
    name = models.CharField(max_length=50)
    slogan = models.CharField(max_length=100)
    city = models.CharField(max_length=20)

class address_company(models.Model):
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    number = models.IntegerField()
    opening_hours = models.CharField(max_length=10)

class services_company(models.Model):
    ID_string = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    show = models.BooleanField(default=True)

class reviews_company(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    estimation = models.IntegerField()
    reviews_text = models.TextField(max_length=500)

class connection_info_company(models.Model):
    number_phone = models.CharField(max_length=10)
    email = models.CharField(max_length=10)
    vk = models.CharField(max_length=100)

class techniques_company(models.Model):
    date = models.DateTimeField()
    number_phone = models.CharField(max_length=10)
    FCS = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    ID_string = models.CharField(max_length=50)
    status = models.BooleanField()
