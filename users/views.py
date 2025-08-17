from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from users.forms import RegisterForm,LoginForm,AssignRoleForm,createfrom,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditProfileForm
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView,LogoutView
from django.views.generic import TemplateView,UpdateView,View,FormView,CreateView,ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
# Create your views here.
User=get_user_model()



def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def sign_up(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            messages.success(request, 'A confirmation mail sent. please chack')
            return redirect('sign-in')
        else:
            print("form is not")
    else:
        form=RegisterForm()
    return render(request,'registration/register.html',{'form':form})


def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html',{'form':form})

@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")
          

def activate_user(request, user_id, token):
    try:
        print(f"Received user_id={user_id},token={token}")
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    
@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, "admin/dashboard.html", {"users": users})

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name__iexact='Organizer').exists())

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)
            messages.success(
                request, f"User{user.username} has been assigned to the {role.name}"
            )
            return redirect("admin-dashboard")

    return render(request, "admin/assign_role.html", {"form": form})

@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    if request.method == "POST":
        form = createfrom(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group{group.name} has been successfully")
            return redirect("create-group")
    else:
        form=createfrom()
    return render(request, "admin/create_group.html", {"form": form})


@user_passes_test(is_admin,login_url='no-permission')
def delete_group(request, group_id):
    del_group = get_object_or_404(Group, id=group_id)
    del_group.delete()
    return redirect('group_list')

@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups=Group.objects.all()
    return render(request,'admin/group_list.html',{'groups':groups})

class ProfileView(TemplateView):
    template_name='accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=self.request.user
        context['username']=user.username
        context['email']=user.email
        context['member_since']=user.date_joined
        context['last_login']=user.last_login
        context['profile_image']=user.profile_image
        context['phone']=user.phone
        
        return context
    
class ChangePasswordView(PasswordChangeView):
    template_name='accounts/password_change.html'
    form_class=CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name='registration/reset_password.html'
    success_url=reverse_lazy('sign-in')
    html_email_template_name='registration/reset_email.html'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['protocol']='https' if self.request.is_secure() else 'http'
        print(context)
        return context
    
    def form_valid(self, form):
       messages.success(
           self.request,'A Reset Email sent. Please check your email'
       )
       return super().form_valid(form)
    
class CustomPasswordConfirmResetView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirmForm
    template_name='registration/reset_password.html'
    success_url=reverse_lazy('sign-in')
    
    def form_valid(self, form):
       messages.success(
           self.request,'Password Reset Successfully '
       )
       return super().form_valid(form)
    

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')