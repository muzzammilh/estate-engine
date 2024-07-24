from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView, UpdateView

from properties.forms import TableUnitFilterForm
from properties.models import Document, Unit
from users.models import User

from .forms import TenancyContractForm
from .models import TenancyContract
from .views import get_filtered_queryset


# view for making contract
class TenancyContractCreateView(View):
    template_name = 'contracts/contract_create.html'
    success_url = reverse_lazy('approved_tenants')

    def get_context_data(self, **kwargs):
        context = kwargs
        context['form'] = context.get('form', TenancyContractForm())
        return context

    def get(self, request, tenant_id):
        tenant = get_object_or_404(User, id=tenant_id)
        unit_id = request.GET.get('unit_id')

        if unit_id:
            unit = get_object_or_404(Unit, id=unit_id)
            document = Document.objects.filter(tenant=tenant, unit=unit, status='approved').first()

            if document:
                tenancy_contract = TenancyContract.objects.filter(
                    tenant=tenant,
                    owner=request.user,
                    unit=unit
                ).first()

                if tenancy_contract:
                    form = TenancyContractForm(instance=tenancy_contract)
                else:
                    form = TenancyContractForm(initial={
                        'tenant': tenant,
                        'owner': request.user,
                        'unit': unit
                    })
                return self.render_response(request, form=form)

        return self.render_response(request)

    def post(self, request, tenant_id):
        tenant = get_object_or_404(User, id=tenant_id)
        form = TenancyContractForm(request.POST)

        if form.is_valid():
            return self.form_valid(form, tenant, request.user)
        return self.render_response(request, form=form)

    def form_valid(self, form, tenant, owner):
        with transaction.atomic():
            existing_contract = TenancyContract.objects.filter(
                tenant=tenant,
                unit=form.cleaned_data['unit']
            ).first()

            if existing_contract:
                existing_contract.delete()
                messages.warning(self.request, 'Updated the contract.')

            contract = form.save(commit=False)
            contract.tenant = tenant
            contract.owner = owner
            contract.save()

        return redirect(self.success_url)

    def render_response(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data(**kwargs))


# for active contracts
class ActiveContractsView(ListView):
    template_name = 'contracts/active_contracts.html'
    context_object_name = 'contracts'
    paginate_by = 20

    def get_queryset(self):
        owner = self.request.user
        queryset = TenancyContract.objects.filter(owner=owner, active=True)
        return get_filtered_queryset(queryset, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TableUnitFilterForm(user=self.request.user, data=self.request.GET)
        return context


# for all contracts
class AllContractsView(ListView):
    template_name = 'contracts/all_contracts.html'
    context_object_name = 'contracts'
    paginate_by = 20

    def get_queryset(self):
        owner = self.request.user
        queryset = TenancyContract.objects.filter(owner=owner)
        return get_filtered_queryset(queryset, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TableUnitFilterForm(user=self.request.user, data=self.request.GET)
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
