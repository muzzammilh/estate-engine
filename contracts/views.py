
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from users.models import User

from .forms import MessageForm
from .models import Message


def get_filtered_queryset(queryset, request):
    property_id = request.GET.get('property')
    unit_id = request.GET.get('unit')

    if property_id:
        queryset = queryset.filter(unit__property_id=property_id)
    if unit_id:
        queryset = queryset.filter(unit_id=unit_id)

    return queryset


class SendMessageView(View):
    def post(self, request, tenant_id):
        tenant = get_object_or_404(User, id=tenant_id)
        form = MessageForm(request.POST)

        if form.is_valid():
            try:
                message = form.save(commit=False)
                message.sender = request.user
                message.receiver = tenant
                message.save()

                # Prepare JSON response
                response_data = {
                    'sender': 'me' if message.sender == request.user else 'other',
                    'content': message.content,
                    'timestamp': message.timestamp.strftime('%H:%M')
                }
                return JsonResponse(response_data)
            except Exception as e:
                # Log the exception and return a JSON response with the error message
                print(f'Error saving message: {e}')
                return JsonResponse({'error': 'Failed to save message'}, status=500)
        else:
            # Return validation errors
            return JsonResponse({'error': 'Form is not valid', 'errors': form.errors}, status=400)


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


class TenantChatView(View):
    template_name = 'contracts/chat.html'

    def get(self, request, owner_id):
        owner = get_object_or_404(User, id=owner_id)
        messages = Message.objects.filter(
            sender__in=[request.user, owner],
            receiver__in=[request.user, owner]
        ).order_by('timestamp')
        form = MessageForm()
        return render(request, self.template_name, {
            'tenant': request.user,
            'chat_messages': messages,
            'form': form,
            'owner': owner,
        })

    def post(self, request, owner_id):
        owner = get_object_or_404(User, id=owner_id)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = owner
            message.save()
        return redirect('tenant_chat', owner_id=owner_id)
