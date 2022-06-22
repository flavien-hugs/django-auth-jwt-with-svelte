# accounts.urls.py

from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views

token_obtain_view = TokenObtainPairView.as_view()
token_refresh_view = TokenRefreshView.as_view()


app_name = 'accounts'
urlpatterns = [
    path(route='register/', view=views.user_register_view, name='register_user'),
    path(route='login/', view=views.user_login_view, name='login_user'),
    path(route='logout/', view=views.logout_view, name="logout_user"),
    path(route='user/', view=views.user_retrieve_view, name='user'),
    path(route='token/', view=token_obtain_view, name='token_obtain_pair'),
    path(route='token/refresh/', view=token_refresh_view, name='token_refresh'),
]
