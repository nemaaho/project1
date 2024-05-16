from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'webapp'
urlpatterns = [
    path('', LoginView.as_view(template_name='webapp/login.html')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logoutpage'),
    #path('', views.IndexView.as_view(), name='index'),
    path('home/', views.indexView, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/results/', views.resultsView, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('last/', views.lastView, name='lastpage'),
    
]