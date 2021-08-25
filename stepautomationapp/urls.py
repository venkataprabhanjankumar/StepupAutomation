from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('<template>/', views.handle_redirect, name='redirect'),
    path('<token>/<template>', views.dashboard, name='dashboard'),
]
