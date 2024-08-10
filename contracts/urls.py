from django.urls import path

from .contract_views import (ActiveContractsView, AllContractsView,
                             ContractDeleteView, ContractUpdateView,
                             TenancyContractCreateView)
from .tenant_views import (ContractDetailView, TenantActiveContractsView,
                           TenantChatView, TenantContractsView,
                           TenantDetailView, TenantMessagesView)
from .views import (OwnerChatView, OwnerDetailView, OwnerMessagesView,
                    SendMessageView)

urlpatterns = [
    path('create-contract/<int:tenant_id>/', TenancyContractCreateView.as_view(), name='create_contract'),
    path('active/', ActiveContractsView.as_view(), name='active_contracts'),
    path('all/', AllContractsView.as_view(), name='all_contracts'),
    path('<int:pk>/update/', ContractUpdateView.as_view(), name='update_contract'),
    path('<int:pk>/delete/', ContractDeleteView.as_view(), name='delete_contract'),
    path('your-contracts/', TenantContractsView.as_view(), name='your_contracts'),
    path('detail/<int:pk>/', ContractDetailView.as_view(), name='contract_detail'),
    path('tenant/<int:tenant_id>/active-contracts/', TenantActiveContractsView.as_view(), name='tenant_active_contracts'),
    path('owner_chat/<int:tenant_id>/', OwnerChatView.as_view(), name='owner_chat'),
    path('tenant_chat/<int:owner_id>/', TenantChatView.as_view(), name='tenant_chat'),
    path('send_message/<int:receiver_id>/', SendMessageView.as_view(), name='send_message'),
    path('owner_messages/', OwnerMessagesView.as_view(), name='owner_messages'),
    path('tenant_messages/', TenantMessagesView.as_view(), name='tenant_messages'),
    path('tenant_detail/<int:pk>/', TenantDetailView.as_view(), name='tenant_detail'),
    path('owner_detail/<int:pk>/', OwnerDetailView.as_view(), name='owner_detail'),
]
