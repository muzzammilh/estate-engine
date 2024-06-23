from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import PropertyForm, UnitForm
from .models import City, Image, Property, State, SubLocality, Unit


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property_object = self.get_object()

        property_images = Image.objects.filter(property=property_object)
        units = Unit.objects.filter(property=property_object)

        unit_images = Image.objects.filter(unit__in=units)

        context['property_images'] = property_images
        context['unit_images'] = unit_images
        return context


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('property_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        for file in self.request.FILES.getlist('images'):
            Image.objects.create(property=self.object, image=file)
        return response


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('property_list')

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        self.object = self.get_object()

        for file in self.request.FILES.getlist('images'):
            Image.objects.create(property=self.object, image=file)

        return super().form_valid(form)


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

    def get_success_url(self):
        return reverse_lazy('property_detail', kwargs={'pk': self.object.property.pk})

    def form_valid(self, form):
        property = get_object_or_404(Property, pk=self.kwargs['property_pk'], owner=self.request.user)

        form.instance.property = property
        response = super().form_valid(form)

        for file in self.request.FILES.getlist('images'):
            Image.objects.create(unit=self.object, image=file)

        return response


class UnitUpdateView(LoginRequiredMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = 'properties/unit_form.html'

    def get_success_url(self):
        return reverse_lazy('property_detail', kwargs={'pk': self.object.property.pk})

    def get_queryset(self):
        return Unit.objects.filter(property__owner=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)

        for file in self.request.FILES.getlist('images'):
            Image.objects.create(unit=self.object, image=file)

        return response


class UnitDeleteView(LoginRequiredMixin, DeleteView):
    model = Unit
    template_name = 'properties/unit_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('property_detail', kwargs={'pk': self.object.property.pk})

    def get_queryset(self):
        return Unit.objects.filter(property__owner=self.request.user)


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


class PropertyImageDeleteView(DeleteView):
    def get(self, request, *args, **kwargs):
        image_id = kwargs.get('image_id')
        image = get_object_or_404(Image, pk=image_id)
        property_id = image.property.pk
        image.delete()
        return redirect('property_detail', pk=property_id)


class UnitImageDeleteView(DeleteView):
    def get(self, request, *args, **kwargs):
        image_id = kwargs.get('image_id')
        image = get_object_or_404(Image, pk=image_id)
        unit = image.unit
        image.delete()
        property_id = unit.property.pk if unit.property else None
        if property_id:
            return redirect('property_detail', pk=property_id)
