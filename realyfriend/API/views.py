from django.shortcuts import render, redirect
from django.http import JsonResponse
from pathlib import Path
import random
import json
import datetime
import phonenumbers
import re
from .models import info_company, address_company, services_company, reviews_company, connection_info_company, techniques_company

def getpagecontent(request):
    # infoCompanyObject = info_company.objects.get(id=random.randint(1, len(info_company.objects.all()))) Рандомыный выбор города, слогона
    if request.GET.get("page") == "services" and request.GET.get("type") == "services":
        servicesCompany = services_company.objects.all()
        servicesList = []
        filterUser = request.GET.get("typefilter")
        for i in servicesCompany:
            if i.show:
                servicesList.append({"name": i.name, "price": i.price, "id": i.ID_string})
        while True:
            prices = []
            counter = 0
            for i, v in enumerate(servicesList):
                if v["price"] > servicesList[i if i+1 == len(servicesList) else i+1]["price"]:
                    temp = v
                    servicesList[i] = servicesList[i if i+1 == len(servicesList) else i+1]
                    servicesList[i if i+1 == len(servicesList) else i+1] = temp
                else:
                    counter += 1
                prices.append(v["price"])
            if counter == len(servicesList):
                break
        if not filterUser in ["minToMaxPrice", "maxToMinPrice"]:
            return JsonResponse({"status": "error", "error": f"Invalid filter \"{filterUser}\""})
        if not request.GET.get("fromPrice") is None:
            temp = servicesList
            servicesList = []
            for i, v in enumerate(temp):
                if v["price"] >= int(request.GET.get("fromPrice")):
                    # print(v["price"], "<", request.GET.get("fromPrice"))
                    # print(len(servicesList))
                    servicesList.append(v)
                    # print(len(servicesList))
                    # print("_________________")
        if not request.GET.get("toPrice") is None:
            temp = servicesList
            servicesList = []
            for i, v in enumerate(temp):
                if v["price"] <= int(request.GET.get("toPrice")):
                    # print(v["price"], ">", request.GET.get("toPrice"))
                    # print(len(servicesList))
                    servicesList.append(v)
                    # print(len(servicesList))
                    # print("_________________")
        if filterUser == "maxToMinPrice":
            servicesList = servicesList[::-1]
        htmlResponce = ""
        for i in servicesList:
            htmlResponce += f'<div class="service-container"><div class="left-content"><h1 class="service-container__name">{i['name']}</h1></div><div class="right-content"><h2 class="service-container__price">{i['price']} р.</h2><button class="btn small_btn" onclick="servicesSign(\'{i["id"]}\')">Записаться</button></div></div>'
        return JsonResponse({"status": "successfully", "html": htmlResponce, "max": max(prices) if request.GET.get("toPrice") is None else int(request.GET.get("toPrice")), "min": min(prices) if request.GET.get("fromPrice") is None else int(request.GET.get("fromPrice"))})
    
    if request.GET.get("page") == "reviews" and request.GET.get("type") == "reviews":
        randomReviews = []
        allReviews = reviews_company.objects.all()
        for i in range(5):
            while True:
                randIndex = random.randint(0, 9)
                if allReviews[randIndex] in randomReviews: 
                    continue
                randomReviews.append(allReviews[randIndex])
                break
        html = ""
        for i in randomReviews:
            html += f'<div class="review"><div class="up-panel"><h1 class="review__name-person">{i.last_name} {i.first_name}</h1><h2 class="review__estimation">{i.estimation}/5</h2></div><div class="down-panel"><p class="review__text-review">{i.reviews_text}</p></div></div>'
        return JsonResponse({"status": "successfully", "html": html})
    infoCompanyObject = info_company.objects.get(id=4)
    servicesCompany = services_company.objects.all()

    addressHtml = "\n".join([f"<h2 class='text-content__address'>г.{i.city}, ул.{i.street}, д.{i.number}. c {i.opening_hours.split()[0]} до {i.opening_hours.split()[1]}</h2>" for i in address_company.objects.all()])
    info = connection_info_company.objects.all()[0]
    addressHtml += f"\n<br>\n<h2 class='text-content__address'><a href='{info.vk}'>VK</a> {info.email} {info.number_phone}</h2>" 
    
    servicesHtml = ""

    for i in servicesCompany:
        if i.show:
            servicesHtml += f''
    
    contextDict = {"main": {"nameCompany": f"{infoCompanyObject.name}", "sloganCompany": f"{infoCompanyObject.slogan}", "cityCompany": f"{infoCompanyObject.city}"},
                   "aboutas": {"nameCompany": f"{infoCompanyObject.name}", "sloganCompany": f"{infoCompanyObject.slogan}", "cityCompany": f"{infoCompanyObject.city}", "addressHtml": addressHtml},
                   "services": {"nameCompany": f"{infoCompanyObject.name}", "sloganCompany": f"{infoCompanyObject.slogan}", "cityCompany": f"{infoCompanyObject.city}", "servicesHTML":servicesHtml},
                   "reviews": {"nameCompany": f"{infoCompanyObject.name}", "sloganCompany": f"{infoCompanyObject.slogan}", "cityCompany": f"{infoCompanyObject.city}"},
                   }
    try:
        html = render(request, request.GET.get("page")+".html", context=contextDict[request.GET.get("page")]).content.decode()
        css = open(str(Path(__file__).resolve().parent)+"\\css\\"+request.GET.get("page")+".css").read()
    except KeyError as e:
        return JsonResponse({"status": "error", "error": "invalid http request"})
    return JsonResponse({"status": "successfully",  "html": html, "css": css})

def getservices(request):
    if request.GET.get("serviceID") != None :
        try:
            service = services_company.objects.get(ID_string=request.GET.get("serviceID"))
        except:
            return JsonResponse({"status":"error", "error":"invalid serviceID"})
        date = datetime.datetime.now()
        return JsonResponse({"status":"successfully", "name": service.name, "price": service.price, "date": [i.date for i in techniques_company.objects.all()], "newSign": f"{date.year}-{date.month}-{date.day+1}"})
    
def adminpanel(request):
    if not request.user.is_superuser:
        return JsonResponse({"status":"error", "error": "Превышение прав"})
    if not request.GET.get("delete") is None and request.GET.get("delete").isdigit():
        try:
            techniques_company.objects.get(id=int(request.GET.get("delete"))).delete()
        except:
            return redirect('/adminpanel')
    infoCompanyObject = info_company.objects.get(id=4)
    services = services_company.objects.all()
    techniques = techniques_company.objects.all()
    htmlServices = ""
    htmlTechniques= ""
    for i in techniques:
        obj = services_company.objects.get(ID_string=i.ID_string)
        htmlTechniques += f"<div class='service'><h3>{i.FCS.split()[0]} {i.FCS.split()[1][0]}. {i.FCS.split()[2][0]}</h3><h3>{obj.name}.</h3><h3>{datetime.datetime.strftime(i.date, "%H:%M %d.%m.%Y")}</h3><a href='/adminpanel?delete={i.id}'>Удалить</a><input type='checkbox' name='{i.ID_string}' class='checkbox-services' {'checked' if i.status == 1 else ''}></div>"
    for i in services:
        htmlServices += f"<div class='service'><h1>{i.name}</h1><h2>{i.price} р.</h2><input type='checkbox' name='{i.ID_string}' class='checkbox-services' {'checked' if i.show == 1 else ''}></div>"
    return render(request, "adminpanel.html", context={"nameCompany": f"{infoCompanyObject.name}", "sloganCompany": f"{infoCompanyObject.slogan}", "cityCompany": f"{infoCompanyObject.city}", "services": htmlServices, "techniques": htmlTechniques})
    
def setservices(request):
    if not request.user.is_superuser:
        return JsonResponse({"status":"error", "error": "Превышение прав"})
    servicesCompany = services_company.objects.all()
    for i in servicesCompany:
        if request.POST.get(i.ID_string, "") == "on":
            i.show = 1
            i.save()
        else:
            i.show = 0
            i.save()
    return redirect('/adminpanel')

def newsign(request):
    POST = json.loads(request.read().decode("utf8"))
    try:
        date = datetime.datetime.strptime(POST["date"]+" "+POST["time"], "%Y-%m-%d %H:%M")
    except:
        return JsonResponse({"status":"error", "error": "Неправильнно формат даты или времени"})
    counterFCS = 0
    counterName = 0
    for i in str(POST["FCS"]):
        if i.lower() in "фывапролджэйцукенгшщзхъячсмитьбю- .":
            counterFCS += 1
    for i in str(POST["name"]):
        if i.lower() in "фывапролджэйцукенгшщзхъячсмитьбю- asdfghjklqwertyuiopzxcvbnm":
            counterName += 1
    if not phonenumbers.is_possible_number(phonenumbers.parse(POST["phone"])):
        return JsonResponse({"status":"error", "error": "Неправильнно введённ телефон"})
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', POST["email"]):
        return JsonResponse({"status":"error", "error": "Неправильнно введённ email"})
    elif counterFCS != len(POST["FCS"]):
        return JsonResponse({"status":"error", "error": "Неправильнно введенно ФИО"})
    elif counterName != len(POST["name"]):
        return JsonResponse({"status":"error", "error": "Неправильнно имя питомца"})
    elif datetime.datetime.now() > date:
        return JsonResponse({"status":"error", "error": "Дата каходится в прошлом"})
    for i in techniques_company.objects.all():
        print(i.ID_string)
        print(POST["ID_string"])
        print()
        if i.ID_string == POST["ID_string"]:
            dateCo = i.date
            if not ((dateCo.replace(tzinfo=None) - date > datetime.timedelta(hours=1)) if dateCo.replace(tzinfo=None) > date else (date - dateCo.replace(tzinfo=None) > datetime.timedelta(hours=1))):
                return JsonResponse({"status":"error", "error": f"В {datetime.datetime.strftime(dateCo, '%H:%M')} есть запись"})
    newTechniques = techniques_company.objects.create(date=datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:00"), number_phone=POST["phone"], FCS=POST["FCS"], name=POST["name"], email=POST["email"], ID_string=POST["ID_string"], status=0)
    return JsonResponse({"status":"successfully"})

def settechniques(request):
    if not request.user.is_superuser:
        return JsonResponse({"status":"error", "error": "Превышение прав"})
    techniquesCompany = techniques_company.objects.all()
    for i in techniquesCompany:
        if request.POST.get(i.ID_string, "") == "on":
            print(i.ID_string)
            i.status = 1
            i.save()
        else:
            i.status = 0
            i.save()
    return redirect("/adminpanel")

def errorNotF(request, exception):
    return redirect("/")