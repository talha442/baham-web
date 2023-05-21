from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Q

from baham.enum_types import VehicleType
from baham.models import VehicleModel


# Create your views here.
def render_login(request, message=None):
    template = loader.get_template('login.html')
    context = {
        'message': message
    }
    return HttpResponse(template.render(context, request))


def view_home(request):
    if not request.user.is_authenticated:
        return render_login(request)
    template = loader.get_template('home.html')
    context = {
        'navbar': 'home',
        'is_superuser': request.user.is_superuser,
    }
    return HttpResponse(template.render(context, request))


def login(request):
    _username = request.POST.get("username")
    _username = _username.lower()
    _password = request.POST.get("password")
    user = User.objects.filter(Q(username=_username) | Q(email=_username)).first()
    if not user:
        return render_login(request, message='User not found. Please check the username/email.')
    if user.check_password(_password):
        auth.login(request, user)
        return HttpResponseRedirect(reverse('home'))
    return render_login(request, message='Invalid password!')


def logout(request):
    auth.logout(request)
    return render_login(request, message='Invalid password!')


def view_aboutus(request):
    template = loader.get_template('aboutus.html')
    context = {
        'navbar': 'aboutus',
        'is_superuser': request.user.is_superuser,
    }
    return HttpResponse(template.render(context, request))


def view_vehicles(request):
    template = loader.get_template('vehicles.html')
    vehicles = VehicleModel.objects.filter(voided=0).order_by('vendor')
    context = {
        'navbar': 'vehicles',
        'is_superuser': request.user.is_superuser,
        'vehicles': vehicles
    }
    return HttpResponse(template.render(context, request))


def create_vehicle(request):
    template = loader.get_template('createvehicle.html')
    context = {
        'navbar': 'vehicles',
        'is_superuser': request.user.is_superuser,
        'vehicle_types': [(t.name, t.value) for t in VehicleType]
    }
    return HttpResponse(template.render(context, request))


def save_vehicle(request):
    _vendor = request.POST.get('vendor')
    _model = request.POST.get('model')
    _type = request.POST.get('type')
    _capacity = int(request.POST.get('capacity'))
    if not _vendor or not _model:
        return HttpResponseBadRequest('Manufacturer and Model name fields are mandatory!')
    if not _capacity or _capacity < 2:
        _capacity = 2 if _type == VehicleType.MOTORCYCLE else 4
    vehicleModel = VehicleModel(vendor=_vendor, model=_model, type=_type, capacity=_capacity)
    vehicleModel.save()
    return HttpResponseRedirect(reverse('vehicles'))


def delete_vehicle(request, uuid):
    if not request.user.is_staff:
        return HttpResponseBadRequest('You are not authorized for this operation!')
    vehicle_model = VehicleModel.objects.filter(uuid=uuid).first()
    if not vehicle_model:
        return HttpResponseBadRequest('This object does not exit!')
    vehicle_model.delete()
    return HttpResponseRedirect(reverse('vehicles'))


def edit_vehicle(request, uuid):
    template = loader.get_template('editvehicle.html')
    vehicle_model = VehicleModel.objects.filter(uuid=uuid).first()
    if not vehicle_model:
        return HttpResponseBadRequest('This object does not exit!')
    context = {
        'navbar': 'vehicles',
        'is_superuser': request.user.is_superuser,
        'vehicle_types': [(t.name, t.value) for t in VehicleType],
        'vehicle': vehicle_model
    }
    return HttpResponse(template.render(context, request))


def update_vehicle(request):
    _uuid = request.POST.get('uuid')
    _vendor = request.POST.get('vendor')
    _model = request.POST.get('model')
    _type = request.POST.get('type')
    _capacity = int(request.POST.get('capacity'))
    if not _vendor or not _model:
        return HttpResponseBadRequest('Manufacturer and Model name fields are mandatory!')
    if not _capacity or _capacity < 2:
        _capacity = 2 if _type == VehicleType.MOTORCYCLE else 4
    vehicle_model = VehicleModel.objects.filter(uuid=_uuid).first()
    if not vehicle_model:
        return HttpResponseBadRequest('Requested object does not exist!')
    vehicle_model.vendor = _vendor
    vehicle_model.model = _model
    vehicle_model.type = _type
    vehicle_model.capacity = _capacity
    vehicle_model.update(update_by=request.user)
    return HttpResponseRedirect(reverse('vehicles'))
