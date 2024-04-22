from django.urls import path

from BACKEND.views import AuthUser, ConfirmAccountUser,DetailAccount, WhoUsedInvite

app_name = 'BACKEND'
urlpatterns = [
    path('user/authorization', AuthUser.as_view(), name='authorization'),
    path('user/confirm', ConfirmAccountUser.as_view(), name='confirm'),
    path('user/detail_account', DetailAccount.as_view(), name='detail_account'),
    path('user/detail_account/invited', WhoUsedInvite.as_view(), name='invited')
]