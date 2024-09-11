from django.urls import path

# views
from entry_management.views import EntryListCreateView, EntryUpdateDeleteView

app_name = 'entry_management'

urlpatterns = [
    path('', EntryListCreateView.as_view(), name='EntryListCreateView'),
    path('<int:entry_id>', EntryUpdateDeleteView.as_view(), name='EntryUpdateDeleteView'),
]
