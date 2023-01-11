from django.core.mail import send_mail

from .models import Car, Service


def header(request):
    def warning():
        for car in Car.objects.all():
            mileage_to_service = (car.service_interval -
                                  (car.mileage - car.last_service_mileage))
            if mileage_to_service <= 3000:
                if not Service.objects.filter(
                        car=car, service_type="OIL", is_active=True):
                    new_service = Service(
                        car=car, service_type="OIL",
                        description="REMINDER",
                        is_active=True)
                    new_service.save()
                    send_mail(
                        f'REMINDER! Oil change for {car} in {mileage_to_service} km',
                        'This message was created automatically by Fleet Manager System',
                        'from@this.email',
                        ['to@this.email'],
                        fail_silently=True,
                    )
            elif mileage_to_service <= 1000:
                pass

        if Service.objects.all().filter(is_active=True):
            return True
        return False

    context = {
        'menu': Car.objects.all(),
        'warning': warning(),
    }
    return context
