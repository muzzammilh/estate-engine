from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from users.models import User

from .forms import MessageForm
from .models import Message, TenancyContract


def get_filtered_queryset(queryset, request):
    property_id = request.GET.get('property')
    unit_id = request.GET.get('unit')

    if property_id:
        queryset = queryset.filter(unit__property_id=property_id)
    if unit_id:
        queryset = queryset.filter(unit_id=unit_id)

    return queryset


# just for sending messages and ajax
class SendMessageView(View):
    def post(self, request, tenant_id):
        if request.user.role == User.OWNER:
            receiver = get_object_or_404(User, id=tenant_id)
        else:
            receiver = get_object_or_404(User, id=tenant_id)

        form = MessageForm(request.POST)

        if form.is_valid():
            try:
                message = form.save(commit=False)
                message.sender = request.user
                message.receiver = receiver
                message.save()

                response_data = {
                    'sender': 'me' if message.sender == request.user else 'other',
                    'content': message.content,
                    'timestamp': message.timestamp.strftime('%H:%M')
                }
                return JsonResponse(response_data)
            except Exception as e:
                print(f'Error saving message: {e}')
                return JsonResponse({'error': 'Failed to save message'}, status=500)
        else:
            return JsonResponse({'error': 'Form is not valid', 'errors': form.errors}, status=400)


# chatting from owner side
class OwnerChatView(View):
    template_name = 'contracts/chat.html'

    def get(self, request, tenant_id):
        tenant = get_object_or_404(User, id=tenant_id)
        messages = Message.objects.filter(
            sender__in=[request.user, tenant],
            receiver__in=[request.user, tenant]
        ).order_by('timestamp')
        form = MessageForm()
        return render(request, self.template_name, {
            'tenant': tenant,
            'chat_messages': messages,
            'form': form,
        })

    def post(self, request, tenant_id):
        tenant = get_object_or_404(User, id=tenant_id)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = tenant
            message.save()
            return redirect('owner_chat', tenant_id=tenant_id)


# messages for owner side
class OwnerMessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'contracts/owner_messages.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        user = self.request.user
        search_query = self.request.GET.get('search', '').strip()

        messages = Message.objects.filter(
            Q(sender__email__icontains=search_query) |
            Q(receiver__email__icontains=search_query),
            Q(sender=user) | Q(receiver=user)
        ).distinct().select_related('sender', 'receiver')

        unique_conversations = {}
        for message in messages:
            key = message.sender.id if message.sender.role == User.TENANT else message.receiver.id
            if key not in unique_conversations:
                unique_conversations[key] = message

        return unique_conversations.values()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contracts'] = TenancyContract.objects.filter(
            owner=self.request.user
        ).select_related('tenant', 'unit', 'unit__property')
        return context
