from django.urls import path
from users.views import sign_up,sign_in,sign_out,activate_user,admin_dashboard,assign_role,create_group,group_list,delete_group
from users.views import ProfileView,ChangePasswordView,CustomPasswordResetView,CustomPasswordConfirmResetView,EditProfileView
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView
urlpatterns = [
    path('sig-up/',sign_up,name='sign-up'),
    path('sign-in',sign_in,name='sign-in'),
    path('sign-out/',sign_out,name='sign-out'),
    path('activate/<int:user_id>/<str:token>/',activate_user,name='activate-user'),
    path('admin-dashboard/',admin_dashboard,name='admin-dashboard'),
    path('assign-role/<int:user_id>/',assign_role,name='assign-role'),
    path('create-group/',create_group,name='create-group'),
    path('group-list/',group_list,name='group-list'),
    path('delete-group/<int:group_id>/',delete_group,name='delete-group'),

    path('profile/',ProfileView.as_view(),name='profile'),
    path('password_Change/',ChangePasswordView.as_view(),name='password-change'),
    path('password-done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password-change-done'),
    path('password-reset/',CustomPasswordResetView.as_view(),name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordConfirmResetView.as_view(),name='password_reset_confirm'),
    path('edit-profile/',EditProfileView.as_view(),name='edit-profile')

]
