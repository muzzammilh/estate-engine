from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from properties.forms import OwnerUnitFilterForm
from properties.models import Document, Unit
from users.models import User

from .forms import TenancyContractForm
from .models import TenancyContract


# view for making contract
class TenancyContractCreateView(View):
    template_name = 'contracts/contract_create.html'
    success_url = reverse_lazy('approved_tenants')

    def get(self, request, tenant_id):
        tenant = get_object_or_404(User, id=tenant_id)
        owner = request.user
        unit_id = request.GET.get('unit_id')

        if unit_id:
            unit = get_object_or_404(Unit, id=unit_id)
            document = Document.objects.filter(tenant=tenant, unit=unit, status='approved').first()
            if document:
                tenancy_contract = TenancyContract.objects.filter(tenant=tenant, owner=owner, unit=unit).first()
                if tenancy_contract:
                    form = TenancyContractForm(instance=tenancy_contract)
                else:
                    initial_data = {'tenant': tenant, 'owner': owner, 'unit': unit}
                    form = TenancyContractForm(initial=initial_data)
            else:
                form = TenancyContractForm()
        else:
            form = TenancyContractForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request, tenant_id):
        tenant = get_object_or_404(User, id=tenant_id)
        owner = request.user
        form = TenancyContractForm(request.POST)
        if form.is_valid():
            existing_contract = TenancyContract.objects.filter(tenant=tenant, unit=form.cleaned_data['unit']).first()

            if existing_contract:
                existing_contract.delete()
                messages.warning(request, 'New contract created successfully.')

            contract = form.save(commit=False)
            contract.tenant = tenant
            contract.owner = owner
            contract.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


# for active contracts
class ActiveContractsView(ListView):
    template_name = 'contracts/active_contracts.html'
    context_object_name = 'contracts'

    def get_queryset(self):
        owner = self.request.user
        queryset = TenancyContract.objects.filter(owner=owner, active=True)

        property_id = self.request.GET.get('property')
        unit_id = self.request.GET.get('unit')
        if property_id:
            queryset = queryset.filter(unit__property_id=property_id)
        if unit_id:
            queryset = queryset.filter(unit_id=unit_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = OwnerUnitFilterForm(user=self.request.user, data=self.request.GET)
        return context


# for all contracts
class AllContractsView(ListView):
    template_name = 'contracts/all_contracts.html'
    context_object_name = 'contracts'

    def get_queryset(self):
        owner = self.request.user
        queryset = TenancyContract.objects.filter(owner=owner)

        property_id = self.request.GET.get('property')
        unit_id = self.request.GET.get('unit')
        if property_id:
            queryset = queryset.filter(unit__property_id=property_id)
        if unit_id:
            queryset = queryset.filter(unit_id=unit_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = OwnerUnitFilterForm(user=self.request.user, data=self.request.GET)
        return context


# update contract
class ContractUpdateView(UpdateView):
    model = TenancyContract
    form_class = TenancyContractForm
    template_name = 'contracts/contract_update.html'
    success_url = reverse_lazy('all_contracts')

    def form_valid(self, form):
        messages.success(self.request, 'Contract updated successfully.')
        return super().form_valid(form)


# delete contract
class ContractDeleteView(DeleteView):
    model = TenancyContract
    success_url = reverse_lazy('all_contracts')
    template_name = 'contracts/contract_delete.html'
    http_method_names = ['get', 'post']

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


# to show active contracts of the tenant
class TenantActiveContractsView(ListView):
    model = TenancyContract
    template_name = 'contracts/tenant_active_contracts.html'
    context_object_name = 'contracts'

    def get_queryset(self):
        tenant = get_object_or_404(User, pk=self.kwargs['tenant_id'])
        return TenancyContract.objects.filter(tenant=tenant, active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tenant'] = get_object_or_404(User, pk=self.kwargs['tenant_id'])
        return context


# to show contracts for user
class TenantContractsView(ListView):
    template_name = 'contracts/tenant_contracts_list.html'
    context_object_name = 'contracts'

    def get_queryset(self):
        return TenancyContract.objects.filter(tenant=self.request.user)


# for detail of contract
class ContractDetailView(DetailView):
    model = TenancyContract
    template_name = 'contracts/contract_detail.html'
    context_object_name = 'contract'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract = self.object
        context['unit'] = contract.unit
        context['property'] = contract.unit.property
        return context
