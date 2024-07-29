from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from properties.forms import TableUnitFilterForm
from users.models import User

from .models import TenancyContract
from .views import get_filtered_queryset


# to show active contracts of the tenant
class TenantActiveContractsView(ListView):
    model = TenancyContract
    template_name = 'contracts/tenant_active_contracts.html'
    context_object_name = 'contracts'
    paginate_by = 20

    def get_queryset(self):
        tenant = get_object_or_404(User, pk=self.kwargs['tenant_id'])
        queryset = TenancyContract.objects.filter(tenant=tenant, active=True)
        return get_filtered_queryset(queryset, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tenant'] = get_object_or_404(User, pk=self.kwargs['tenant_id'])
        context['filter_form'] = TableUnitFilterForm(self.request.GET)
        return context


# to show contracts for user
class TenantContractsView(ListView):
    template_name = 'contracts/tenant_contracts_list.html'
    context_object_name = 'contracts'
    paginate_by = 20

    def get_queryset(self):
        queryset = TenancyContract.objects.filter(tenant=self.request.user)
        return get_filtered_queryset(queryset, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TableUnitFilterForm(self.request.GET)
        return context


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
