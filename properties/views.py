from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from contracts.models import TenancyContract
from gallery.forms import DocFormSet, ImageFormSet
from gallery.models import Image

from .forms import (PropertyForm, TableUnitFilterForm, TenantUnitFilterForm,
                    UnitForm)
from .models import City, Document, Property, State, SubLocality, Unit


class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_list.html'

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'properties/property_detail.html'

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class UnitDetailView(DetailView):
    model = Unit
    template_name = 'properties/unit_detail.html'
    context_object_name = 'unit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('property_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, queryset=Image.objects.none())
        else:
            context['image_formset'] = ImageFormSet(queryset=Image.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()
            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.content_object = self.object
                    image.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(form)


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('property_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, queryset=self.object.images.all())
        else:
            context['image_formset'] = ImageFormSet(queryset=self.object.images.all())
        return context

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.content_object = self.object
                    image.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(form)


class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = 'properties/property_confirm_delete.html'
    success_url = reverse_lazy('property_list')

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class UnitCreateView(LoginRequiredMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'properties/unit_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, queryset=Image.objects.none())
        else:
            context['image_formset'] = ImageFormSet(queryset=Image.objects.none())
        return context

    def get_success_url(self):
        return reverse_lazy('property_detail', kwargs={'pk': self.object.property.pk})

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        property = get_object_or_404(Property, pk=self.kwargs['property_pk'], owner=self.request.user)
        form.instance.property = property
        if image_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()
            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.content_object = self.object
                    image.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(form)


class UnitUpdateView(LoginRequiredMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'properties/unit_form.html'

    def get_success_url(self):
        return reverse_lazy('property_detail', kwargs={'pk': self.object.property.pk})

    def get_queryset(self):
        return Unit.objects.filter(property__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, queryset=self.object.images.all())
        else:
            context['image_formset'] = ImageFormSet(queryset=self.object.images.all())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.content_object = self.object
                    image.save()
            return redirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(form)


class UnitDeleteView(LoginRequiredMixin, DeleteView):
    model = Unit
    template_name = 'properties/unit_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('property_detail', kwargs={'pk': self.object.property.pk})

    def get_queryset(self):
        return Unit.objects.filter(property__owner=self.request.user)


class AvailableUnitsView(ListView):
    model = Unit
    template_name = 'properties/available_units.html'
    context_object_name = 'units'

    def get_queryset(self):
        queryset = Unit.objects.filter(is_available_for_rent=True)
        form = TenantUnitFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['country']:
                queryset = queryset.filter(property__country=form.cleaned_data['country'])
            if form.cleaned_data['state']:
                queryset = queryset.filter(property__state=form.cleaned_data['state'])
            if form.cleaned_data['city']:
                queryset = queryset.filter(property__city=form.cleaned_data['city'])
            if form.cleaned_data['sub_locality']:
                queryset = queryset.filter(property__sub_locality=form.cleaned_data['sub_locality'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TenantUnitFilterForm(self.request.GET)
        return context


# view for document uploads
class UploadDocumentsView(View):
    DocFormSet = DocFormSet

    def get(self, request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)
        formset = self.DocFormSet(queryset=Image.objects.none())

        existing_pending_document = Document.objects.filter(unit=unit, tenant=request.user, status='pending').first()

        if existing_pending_document:
            messages.warning(request, "You have already applied for this unit.")
            return redirect('user_applied_units')

        return render(request, 'properties/upload_documents.html', {'unit': unit, 'formset': formset})

    def post(self, request, unit_id):
        unit = get_object_or_404(Unit, pk=unit_id)

        existing_pending_document = Document.objects.filter(unit=unit, tenant=request.user, status='pending').first()

        if existing_pending_document:
            messages.warning(request, "You have already applied for this unit.")
            return redirect('user_applied_units')

        existing_rejected_document = Document.objects.filter(unit=unit, tenant=request.user, status='rejected').first()

        if existing_rejected_document:
            new_document = Document(unit=unit, tenant=request.user, status='pending')
            new_document.save()
        else:
            new_document = Document(unit=unit, tenant=request.user, status='pending')
            new_document.save()

        formset = self.DocFormSet(request.POST, request.FILES)

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.content_object = new_document
                instance.save()

            messages.success(request, "Documents uploaded successfully.")
            return redirect('user_applied_units')

        messages.error(request, "There was an error uploading your documents. Please try again.")
        return render(request, 'properties/upload_documents.html', {'unit': unit, 'formset': formset})


# view for the units user applied
class TenantAppliedUnitsView(ListView):
    template_name = 'properties/tenant_applied_units.html'
    context_object_name = 'applied_units'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        filter_form = TableUnitFilterForm(self.request.GET)

        documents = Document.objects.filter(tenant=user)

        if filter_form.is_valid():
            property_id = filter_form.cleaned_data.get('property')
            unit_id = filter_form.cleaned_data.get('unit')

            if property_id:
                documents = documents.filter(unit__property_id=property_id)

            if unit_id:
                documents = documents.filter(unit_id=unit_id)

        applied_units = [
            {
                'unit': document.unit,
                'status': document.status,
            }
            for document in documents
        ]

        return applied_units

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = TableUnitFilterForm(self.request.GET)
        context['filter_form'] = filter_form
        return context


# view for unit applied by tenants
class UnitAppliedTenantsView(ListView):
    template_name = 'properties/unit_applied_tenants.html'
    context_object_name = 'applied_tenants'
    paginate_by = 5

    def get_queryset(self):
        unit_id = self.kwargs.get('unit_id')
        unit = get_object_or_404(Unit, pk=unit_id)
        documents = Document.objects.filter(unit=unit)

        applied_tenants = []
        for document in documents:
            tenant = get_object_or_404(get_user_model(), id=document.tenant_id)
            document_images = Image.objects.filter(content_type=ContentType.objects.get_for_model(Document), object_id=document.id)
            tenant_info = {
                'tenant': tenant,
                'status': document.status,
                'document_images': document_images,
                'document_id': document.id
            }
            applied_tenants.append(tenant_info)
        return applied_tenants

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unit_id = self.kwargs.get('unit_id')
        unit = get_object_or_404(Unit, pk=unit_id)
        context['unit'] = unit
        context['documents'] = Document.STATUS_CHOICES
        return context


# view for status changes
class UpdateDocumentStatusView(View):
    def post(self, request, document_id, *args, **kwargs):
        status = request.POST.get('status')
        document = get_object_or_404(Document, id=document_id)

        if status == 'approved':
            existing_approved_documents = Document.objects.filter(unit=document.unit, status='approved').exclude(id=document.id)
            if existing_approved_documents.exists():
                message = "Another tenant has already been approved for this unit."
                return JsonResponse({'message': message, 'status': 'error', 'new_status': document.status})

            else:
                if TenancyContract.objects.filter(unit=document.unit, tenant=document.tenant).exists():
                    message = "You have already been approved for this unit."
                    return JsonResponse({'message': message, 'status': 'error', 'new_status': document.status})

                TenancyContract.objects.create(
                    unit=document.unit,
                    tenant=document.tenant,
                    owner=document.unit.property.owner,
                )
                document.unit.is_available_for_rent = False
                document.unit.resident = document.tenant
                document.unit.save()

        document.status = status
        document.save()
        unit = document.unit
        if status == 'rejected' or status == 'pending':
            if Document.objects.filter(unit=unit, status='approved').exclude(id=document.id).exists():
                unit.is_available_for_rent = False
            else:
                unit.is_available_for_rent = True
                unit.resident = None
            unit.save()

            TenancyContract.objects.filter(unit=unit, tenant=document.tenant).delete()

        message = f"Document status updated to '{status}'."
        return JsonResponse({'message': message, 'status': 'success', 'new_status': status})


# to dislay all units of owner
class OwnerAllUnitsListView(ListView):
    model = Unit
    template_name = 'properties/owner_all_units.html'
    context_object_name = 'units'
    paginate_by = 20

    def get_queryset(self):
        queryset = Unit.objects.filter(property__owner=self.request.user)
        form = TableUnitFilterForm(self.request.GET)

        if form.is_valid() and form.cleaned_data.get('property'):
            queryset = queryset.filter(property=form.cleaned_data['property'])

        if form.is_valid() and form.cleaned_data.get('unit'):
            queryset = queryset.filter(id=form.cleaned_data['unit'].id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TableUnitFilterForm(self.request.GET, user=self.request.user)
        return context


# to display all unit that are not rented out
class OwnerAvailableUnitsView(ListView):
    model = Unit
    template_name = 'properties/owner_available_units.html'
    context_object_name = 'units'
    paginate_by = 20

    def get_queryset(self):
        queryset = Unit.objects.filter(property__owner=self.request.user, is_available_for_rent=True)
        self.filter_form = TableUnitFilterForm(self.request.GET, user=self.request.user)

        if self.filter_form.is_valid() and self.filter_form.cleaned_data.get('property'):
            queryset = queryset.filter(property=self.filter_form.cleaned_data['property'])

        if self.filter_form.is_valid() and self.filter_form.cleaned_data.get('unit'):
            queryset = queryset.filter(id=self.filter_form.cleaned_data['unit'].id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TableUnitFilterForm(self.request.GET, user=self.request.user)
        return context


# to display all unit that are rented out
class OwnerRentedOutUnitsView(ListView):
    model = Unit
    template_name = 'properties/owner_rentedout_units.html'
    context_object_name = 'units'
    paginate_by = 20

    def get_queryset(self):
        queryset = Unit.objects.filter(property__owner=self.request.user, is_available_for_rent=False)
        self.filter_form = TableUnitFilterForm(self.request.GET, user=self.request.user)

        if self.filter_form.is_valid() and self.filter_form.cleaned_data.get('property'):
            queryset = queryset.filter(property=self.filter_form.cleaned_data['property'])

        if self.filter_form.is_valid() and self.filter_form.cleaned_data.get('unit'):
            queryset = queryset.filter(id=self.filter_form.cleaned_data['unit'].id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TableUnitFilterForm(self.request.GET, user=self.request.user)
        return context


def load_states(request):
    country_id = request.GET.get('country_id')
    states = State.objects.filter(country_id=country_id).order_by('name')
    return JsonResponse(list(states.values('id', 'name')), safe=False)


def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)


def load_sub_localities(request):
    city_id = request.GET.get('city_id')
    sub_localities = SubLocality.objects.filter(city_id=city_id).order_by('name')
    return JsonResponse(list(sub_localities.values('id', 'name')), safe=False)


def load_units(request):
    property_id = request.GET.get('property_id')
    units = Unit.objects.filter(property_id=property_id).values('id', 'unit_number')
    return JsonResponse(list(units), safe=False)
