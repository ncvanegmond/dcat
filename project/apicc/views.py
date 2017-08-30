# Imports 
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import generic

import requests
from rest_framework import viewsets
#import pandas as pd 
#import numpy as np
import matplotlib
# fix dependency issue in Heroku: doesn't support Tk
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg


from project.apicc.forms import SubmitCryptoasset, PortfolioForm
from project.apicc.serializers import (UserSerializer, 
                                       CryptoassetSerializer,
                                       CryptoassetV1Serializer,
                                       )

from .models import Cryptoasset, CryptoassetVersionOne, Portfolio

from .fetch_coinlist import(mpl_plot_fig_basic,
                            df_data_to_float,
                            get_portfolio,
                           )

# Create your views here.
#==============================================================================
# #class IndexView(LoginRequiredMixin, generic.ListView):
# class IndexView(generic.ListView):
#     login_url = '../../accounts/login/'
#     redirect_field_name = 'redirect_to'
#     template_name = 'dcai/index.html'
#     context_object_name = 'cryptoasset_list'
# 
#     def get_queryset(self):
#         """return list of cryptoassets in the database"""
#         return Cryptoasset.objects.filter().order_by('pk')
#==============================================================================

def index(request):
    template_name = 'index.html'

    return render(request, template_name, {})

#==============================================================================
# def save_cryptoasset(request):
#     def delete_all_item():
#         print("clear all entries in the DB")
#         Cryptoasset.objects.all().delete()
#         
#     if request.method == "POST":
#         delete_all_item()
#         print("POST")
#         form = SubmitCryptoasset(request.POST)
#         if form.is_valid():
#             url = form.cleaned_data['url']
#             r = requests.get(url)
#             json = r.json()
#             data = json['Data']
#             
#             for num, key in enumerate(data):
#                 serializer = CryptoassetSerializer(data=data[key])
#                 if serializer.is_valid():
#                     print("serializer is valid")
#                     embed = serializer.save()
#                     print(serializer.errors)
#                 else: 
#                     print("serializer in invalid")
#                     print(serializer.errors)
#                     serializer.is_valid()
#                 if num==len(data):    
#                     return render(request, 'embeds.html', {'embed': embed})
#                 
#     else:
#         print("render form")
#         form = SubmitCryptoasset()
# 
#     return render(request, 'index.html', {'form': form})
#==============================================================================

# Global variable declarations
TOP_BY_MARKETCAP = 500

# Function based view declarations
#==============================================================================
# def draw_mpl(request):
# #def draw_mpl(request, portfolio=0):
# #    size = request.GET.get('size')
# #    return render(request, 'dcai/draw_mpl.html', {'size':size})
#     #TODO make pythonesque
#     #TODO figure out why GET request doesn't take strings?
#     if request.GET.get('portfolio')==None:
#         print("no get request")
#         portfolio = 0
#     else:
#         print("get GET")
#         portfolio = request.GET.get('portfolio')
#     
#     return render(request, 'apicc/draw_mpl.html', {'portfolio':portfolio})
#==============================================================================

def draw_mpl(request):
    if request.GET.get('pname')==None:
        print("no get request")
        pname = 0
    else:
        print("get GET")
        pname = request.GET.get('pname')
    
    return render(request, 'apicc/draw_mpl.html', {'pname':pname})


def draw_mpl_model(request):
    #TODO write dynamic title -_-'
    #TODO make pythonesque
    print("draw_mpl_model")
    form = PortfolioForm()
    
    if request.GET.get('pname')==None:
        print("no get request")
        pname = 0
        print("print: {}".format(pname))
    else:
        pname = request.GET.get('pname')
        print("get POST: {}".format(pname))
        
    print("let's render", pname)
    return render(request, 'apicc/draw_mpl_model.html', {'pname': pname, 'form':form})
    

def momentum_plot(request, pname):
#def momentum_plot(rquest, size=1,):
#    portfolio = name
    print("\n\nmomentum_plot\n\n")
#    print(type(portfolio), portfolio)
    
    if pname=='0':
        print("No input: return empty plot")
        f = plt.figure()
        ax = f.add_subplot(111)
#        ax.plot([1,2,3,4], color='b')
        ax.axis('off')
    else:
#        data = CryptoassetVersionOne.objects.values_list('symbol', flat=True).filter(portfolio__pname__startswith='Anonymous').distinct()
        data = CryptoassetVersionOne.objects.values_list('symbol', flat=True).filter(portfolio__id=pname).distinct()
        print("got ticker data")
        data_list = list(data)
        print("list of retrieved data: \n{}".format(data_list))
#        
        portfolio_description = Portfolio.objects.values_list('pdescription', flat=True).filter(id=pname).distinct()
        portfolio_description = list(portfolio_description)[0]
        print('portfolio_description: {}\type: {}'.format(portfolio_description, type(portfolio_description)))
        
        f = mpl_plot_fig_basic(data_list, portfolio_description)

#        f = plt.figure()
#        ax = f.add_subplot(111)
#        ax.plot([1,2,3,4], color='r')
#        ax.axis('off')

    def output_mlp_quantprofile(fig, portfolio):
        '''
        Export figure to file
        '''
        print('export figure to file')
        #TODO: to prevent clutter: save outputfiles to ./image/folder
#        filename = tempfile.NamedTemporaryFile(
##            dir='static/temp',
#            dir='dcai/static/dcai/',
#            suffix='.png', delete=False)
        
        #TODO rewrite static folder reference
        filename = "apicc/static/dcai/momentum_{}.png".format(portfolio)
        plotPng = filename.split('/')[-1]

        dpi = 250
        fig.savefig(filename, dpi=dpi, facecolor='w', edgecolor='w',
#        fig.savefig(filename, dpi=250, facecolor='0.7', edgecolor='r',
            orientation='landscape', papertype=None, format=None,
            transparent=False, bbox_inches='tight', pad_inches=0,
            frameon=None)

#        filename.close()
#        plotPng = filename.name.split('/')[-1]
        print(plotPng)
        #TODO destroy tempfile after use
        return plotPng    
        
#    plotPng = output_mlp_quantprofile(f, portfolio)
    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    matplotlib.pyplot.close(f)
    #TODO find out how to catch temp file name
    
    print("give response")
    return response 
#    return response, plotPng 
#    else:
#        print("not right argument")

def save_cryptoasset(request):
    def delete_all_item():
        print("clear all entries in the DB")
        CryptoassetVersionOne.objects.all().delete()
#    delete_all_item()
        
    if request.method == "POST":
        print("POST")
#        delete_all_item()
        form = SubmitCryptoasset(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            url = 'https://api.coinmarketcap.com/v1/ticker/'
            r = requests.get(url)
            data = r.json()
            top_x = TOP_BY_MARKETCAP
            data = data[:top_x]
            print("Looping through all items.")
            
            #TODO check if exists, if so update, if not create
            #    check on last updated field
            for num, key in enumerate(data):
#            for num, key in enumerate(data[:1]):
                print(key['rank'], key['symbol'])
#                serializer = CryptoassetV1Serializer(data=data[key])
                serializer = CryptoassetV1Serializer(data=key)
                if serializer.is_valid():
#                    print("{}. serializer is valid".format(num))
                    embed = serializer.save()
                else: 
                    print("{}. serializer in invalid. Printing errors:".format(num))
                    print(serializer.errors)
#                    serializer.is_valid()
                if num==len(data):    
                    return render(request, 'embeds.html', {'embed': embed})
                
    else:
        print("render form")
        form = SubmitCryptoasset()

    return render(request, 'apicc/update.html', {'form': form})

# Class based view declarations
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer