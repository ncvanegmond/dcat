"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# Imports
from django.conf.urls import url, include
from rest_framework import routers
from project.apicc import views


#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)

app_name = 'apicc'
urlpatterns = [
#    url(r'^', include(router.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^updateDB/$', views.save_cryptoasset, name='updateDB'),
    url(r'^momentum_plot/(?P<pname>\d+)/$', views.momentum_plot, name='momentum_plot'),
    url(r'^draw_mpl/$', views.draw_mpl, name='draw_mpl'),
    url(r'^momentum_plot_model/(?P<pname>\d+)/$', views.momentum_plot, name='momentum_plot_model'),
    url(r'^draw_mpl_model/$', views.draw_mpl_model, name='draw_mpl_model'),
]