from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from properties.forms import TableUnitFilterForm
from users.models import User

from .forms import MessageForm
from .models import Message, TenancyContract
from .views import (get_chat_messages, get_filtered_queryset, get_user_by_id,
                    get_user_context_data, get_user_messages)


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


# chatting from tenant side
class TenantChatView(View):
    template_name = 'contracts/chat.html'

    def get(self, request, owner_id):
        owner = get_user_by_id(owner_id)
        messages = get_chat_messages(request.user, owner)

        form = MessageForm()
        return render(request, self.template_name, {
            'tenant': request.user,
            'chat_messages': messages,
            'form': form,
            'owner': owner,
        })

    def post(self, request, owner_id):
        owner = get_user_by_id(owner_id)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = owner
            message.save()
            return redirect('tenant_chat', owner_id=owner_id)
        return self.get(request, owner_id)


# messages for tennat side
class TenantMessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'contracts/tenant_messages.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '').strip()
        return get_user_messages(self.request.user, search_query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_context_data(self.request.user, is_owner=False))
        return context


# for tenant detail
class TenantDetailView(DetailView):
    model = User
    template_name = 'contracts/tenant_detail.html'
    context_object_name = 'tenant'
