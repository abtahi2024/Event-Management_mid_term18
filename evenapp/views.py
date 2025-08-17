from datetime import date
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.mail import send_mail
from django.views import View
from django.views.generic import UpdateView, DeleteView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Count

from .models import Event, Category
from .forms import EventForm, CategoryForm
# Create your views here.

User=get_user_model()

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()
def is_organizer(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name__iexact='Organizer').exists())

def admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)

def is_participant(user):
    return user.groups.filter(name='participate').exists()

def show_event(request):
    events = Event.objects.all()
    return render(request, 'show_event.html',{'events':events})


@login_required
def deshboard(request):
    today=date.today()
    events=Event.objects.select_related('category').prefetch_related('participant')

    context={
        'events':events,
        'total_events':events.count(),
        'total_categories':Category.objects.count(),
        'upcoming_events':events.filter(date__gt=today).count(),
        'past_events':events.filter(date__lt=today).count(),
        'todays_events':events.filter(date=today).count(),
    }
    return render(request,'event.html',context)


class CreateEvent(View):
    template_name = 'Event_Form.html'

    def get(self, request, *args, **kwargs):
        form = EventForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('deshboard')
        return render(request, self.template_name, {'form': form})

@method_decorator(user_passes_test(is_organizer, login_url='no-permission'), name='dispatch')
class Update_event(UpdateView):
    model=Event
    form_class=EventForm
    template_name='Event_Form.html'
    success_url=reverse_lazy('deshboard')
    pk_url_kwarg='pk'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['event']=self.get_object()
        return context
    def form_valid(self, form):
        messages.success(self.request,'Event update')
        return super().form_valid(form)
    
@method_decorator(user_passes_test(is_organizer, login_url='no-permission'), name='dispatch')
class Delete_event(DeleteView):
    model=Event
    template_name='Event_Form.html'
    success_url=reverse_lazy('deshboard')
    def delete(self, request, *args, **kwargs):
        messages.success(request,'event Deleted')
        return super().delete(request, *args, **kwargs)
    
@user_passes_test(is_admin, login_url='no-permission')
def remove_participant(request, event_id, user_id):
    event = get_object_or_404(Event, id=event_id)
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        event.participant.remove(user)
        messages.success(request, f"{user.username} has been removed from the event.")
        return redirect('event_detail', id=event.id)
    return render(request, 'RMB_participate.html', {'event': event, 'user': user})

class Event_details(DetailView):
    model=Event
    template_name='Event_detail.html'
    pk_url_kwarg='pk'

@user_passes_test(is_organizer,login_url='no-permission')
def add_category(request):
    form=CategoryForm(request.POST or None)
    if request.method =='POST' and form.is_valid():
        form.save()
        messages.success(request,'added category')
        return redirect('deshboard')
    return render(request,'category_form.html',{'form':form})

@login_required
def RSVP_Event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user

    if event.participant.filter(pk=user.id).exists():
        messages.error(request, "You have already RSVP'd to this event.")
    else:
        event.participant.add(user)
        messages.success(request, "RSVP successful! A confirmation email has been sent.")

        send_mail(
            subject="RSVP Confirmation Email",
            message=f"Aslamolikum {user.username},\n\nYou have successfully RSVP'd to the event {event.name}.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True
        )

    return redirect('event-details', pk=event.id)


class ParticipantDashboardView(TemplateView):
    template_name='participant_dashboard.html'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['rsvp_events']=self.request.user.rsvp_events.all()
        return context