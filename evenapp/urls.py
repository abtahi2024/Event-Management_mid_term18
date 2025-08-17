from evenapp.views import *
from django.urls import *

urlpatterns = [
    path('show-event/',show_event ,name='show-event'),
    path('deshboard/',deshboard,name='deshboard'),
    path('create-event/',CreateEvent.as_view(),name='create-event'),
    path('update-event/<int:pk>/',Update_event.as_view(),name='update_event'),
    path('delete_event/<int:pk>/',Delete_event.as_view(),name='delete_event'),
    path('remove-participant/<int:user_id>/',remove_participant ,name='remove-participant'),
    path('event-details/<int:pk>/',Event_details.as_view(),name='event-details'),
    path('add-category/',add_category,name='add-category'),
    path('rsvp-event/<int:event_id>/',RSVP_Event,name='rsvp-event'),
    path('participantDashboard/',ParticipantDashboardView.as_view(),name='participantDashboard')
]
