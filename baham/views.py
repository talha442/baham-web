from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse

from baham.enum_types import VehicleType
from baham.models import Contract, VehicleModel, Vehicle


# Create your views here.
def view_home(request):
    template = loader.get_template('home.html')
    context = {
        'navbar': 'home',
    }
    return HttpResponse(template.render(context, request))


def view_aboutus(request):
    template = loader.get_template('aboutus.html')
    context = {
        'navbar': 'aboutus',
    }
    return HttpResponse(template.render(context, request))


def view_vehicles(request):
    template = loader.get_template('vehicles.html')
    vehicles = VehicleModel.objects.filter(voided=0).order_by('vendor')
    context = {
        'navbar': 'vehicles',
        'vehicles': vehicles
    }
    return HttpResponse(template.render(context, request))


def create_vehicle(request):
    template = loader.get_template('createvehicle.html')
    context = {
        'navbar': 'vehicles',
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
    vehicle_model = VehicleModel(vendor=_vendor, model=_model, type=_type, capacity=_capacity)
    vehicle_model.save()
    return HttpResponseRedirect(reverse('vehicles'))


def edit_vehicle(request, uuid):
    template = loader.get_template('editvehicle.html')
    vehicle_model = VehicleModel.objects.filter(uuid=uuid).first()
    context = {
        'navbar': 'vehicles',
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
    if vehicle_model:
        vehicle_model.vendor = _vendor
        vehicle_model.model = _model
        vehicle_model.type = _type
        vehicle_model.capacity = _capacity
        vehicle_model.update(udpated_by=request.user)
    else:
        return HttpResponseBadRequest('No record found for given UUID!')
    return HttpResponseRedirect(reverse('vehicles'))


def delete_vehicle(request, uuid):
    # If the user is not a staff member then disallow
    if not request.user.is_staff:
        return HttpResponseBadRequest('Delete not allowed for non-staff users.')
    vehicle_models = VehicleModel.objects.filter(uuid=uuid)
    if not vehicle_models:
        return HttpResponseBadRequest('Vehicle model with given UUID not found!')
    vehicle_model = vehicle_models.first()
    # Soft delete if there are already vehicles in contract
    vehicles = Vehicle.objects.filter(model=vehicle_model)
    if vehicles:
        vehicle_model.void_reason = "Voided by user."
        vehicle_model.delete()
    return HttpResponseRedirect(reverse('vehicles'))
