from datetime import datetime
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.views.generic.list import ListView


from .models import Car, Refuel, Service
from .forms import AddCarForm, RefuelForm, ServiceForm

# Create your views here.


def starting_page(request):
    cars = Car.objects.all()
    context = {"cars": cars}
    return render(request, "cars/index.html", context)


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User was created")
            return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, "Something went wrong!")

    else:
        
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "cars/register.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return HttpResponseRedirect(reverse("starting-page"))
        else:
            messages.warning(request, "Something went wrong!")
            return render(request, "cars/login.html", {
                "alert": "warning",
                "alert_message": "Invalid username or password"
            })
    else:
        return render(request, "cars/login.html")


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out.")
    return HttpResponseRedirect(reverse("starting-page"))


@login_required
def car_details(request, slug):
    car = Car.objects.get(slug=slug)
    services = Service.objects.filter(car=car)
    refuels = Refuel.objects.filter(car=car)
    mileage_to_service = car.service_interval - (car.mileage - car.last_service_mileage)
    context = {"car": car,
               "refuels": refuels,
               "services": services,
               "mileage_to_service": mileage_to_service}
    return render(request, "cars/car-details.html", context)


@login_required
def add_car(request):
    if request.method == 'POST':
        form = AddCarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.save()
            messages.success(request, f"{car} been added.")
            return HttpResponseRedirect(reverse("starting-page"))
    else:
        form = AddCarForm()
    context = {"form": form}
    return render(request, "cars/add-car.html", context)


@login_required
def delete_car(request, slug):
    car = Car.objects.get(slug=slug)
    if request.method == 'POST':
        car.delete()
        messages.error(request, f"{car} has been deleted.")
        return HttpResponseRedirect(reverse('starting-page'))
    context = {'car': car}
    return render(request, 'cars/car-delete.html', context)


@login_required
def refuel(request):
    if request.method == 'POST':
        form = RefuelForm(request.POST)
        if form.is_valid():
            refuel = form.save(commit=False)
            refuel.save()
            messages.success(request, f"{refuel.car} - Refuel informations has been successfully added.")
            return HttpResponseRedirect(reverse("starting-page"))
    else:
        form = RefuelForm()
    context = {"form": form}
    return render(request, "cars/refuel-car.html", context)


@login_required
def report(request):
    service_form = ServiceForm(request.POST)
    if request.method == 'POST':
        if service_form.is_valid():
            service_form = service_form.save(commit=False)
            service_form.save()
            messages.success(request, "Service has been reported.")
            return HttpResponseRedirect(reverse("starting-page"))
    else:
        service_form = ServiceForm()
    context = {"service_form": service_form}
    return render(request, "cars/report.html", context)


@login_required
def service_done(request, id):
    service = Service.objects.get(id=id)
    if request.method == 'GET':
        service.is_active = False
        service.mileage = service.car.mileage
        service.date_fixed = datetime.today()
        if service.service_type == "OIL":
            car = service.car
            car.last_service_mileage = car.mileage
            car.save()
        service.save()
        messages.success(request, f"{service.car} - Service has been done.")
    return HttpResponseRedirect(reverse("starting-page"))


@login_required
def services(request):
    def active_services():
        services = Service.objects.filter(
                        is_active=True
                    ).values(
                        'car__slug', 'car__brand', 'car__model'
                    ).annotate(
                        times=Count('car'))
        return services
    context = {"active_services": active_services}
    return render(request, "cars/services.html", context)
