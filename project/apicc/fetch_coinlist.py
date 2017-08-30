#!/user/bin/env python3 -tt
# -*- coding: utf-8 -*-
"""
Module documentation.

Fetch the coins currently available via CryptoCompare API
    https://www.cryptocompare.com/api/data/coinlist/
    
Notes:
    MPL does not handle plotting (x,y) = (x,0) values on a x,y axes system?
"""

# Imports
import json
import requests
import time
import math
import tempfile
from datetime import datetime
import urllib.request
from pathlib import Path

# fix for Heroku https://stackoverflow.com/questions/41319082/import-matplotlib-failing-with-no-module-named-tkinter-on-heroku

import pandas as pd
import numpy as np
# not installed in dcai_bot VirtualEnv
#from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.image as image
#from PIL import Image

#from adjustText import adjust_text
#https://github.com/Phlya/adjustText/blob/master/examples/Examples.ipynb

#from .auxiliary import (AppURLopener,
#                       df_data_to_float,
#                       generate_sample_period_str,
#                       )

# Global variables
SMALL_SIZE = 6
MEDIUM_SIZE = 9
BIGGER_SIZE = 12   
BIGGEST_SIZE = 14   

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGEST_SIZE)  # fontsize of the figure title
    
CURRENT_DATE = datetime.fromtimestamp(time.time()).strftime('%d %b %Y')
DEBUG = False

# Class declarations
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

# Function declarations
def df_data_to_float(DataFrame):
    '''
    Try to convert each columns to numeric
    '''
    print("Convert dataframe to float")
    for series in DataFrame:
#            print(series, DataFrame[series].name)
        try:
            DataFrame[series] = pd.to_numeric(DataFrame[series])
        except ValueError:
#            print(series, "not able to convert")
            pass
    return DataFrame

def generate_sample_period_str(df):
    start_date = df.index[0].strftime('%d-%b-%Y')
    end_date = df.index[-1].strftime('%d-%b-%Y')
#    sample_period = "Timeframe: {} to {}".format(start_date, end_date)
    sample_period = "{} to {}".format(start_date, end_date)
    return sample_period

def check_coinlist(ticker='BTC'):
    '''
    Check if coin is listed on CryptoCompare
    
    Input:
        * 1x ticker
    Output:
        * Boolean
    '''
#    print("Check if coin is on CryptoCompare CoinList")
#    url = "https://www.cryptocompare.com/api/data/coinlist/"
#    
#    print(url)
#    response = requests.get(url)
#
#    dic = json.loads(response.content)
#
#    CryptoCompare_coinList = []
#    for index, key in enumerate(dic['Data']):
#        print(index, key)
#        CryptoCompare_coinList.append(key)
#
#    print("${} is listed on CryptoCompare: ".format(ticker)+str(ticker in CryptoCompare_coinList))
#    CryptoCompare_coinList = fetch_coinlist()
#    return ticker in CryptoCompare_coinList
    return ticker in fetch_coinlist()

def fetch_coinList():
    '''
    Fetch complete list of coins listed on CryptoCompare
    '''
    print("Let's get CryptoCompare CoinList")
    url = "https://www.cryptocompare.com/api/data/coinlist/"

    print(url)
    response = requests.get(url)

    dic = json.loads(response.content)
    data = dic['Data']

    return data

def get_IdList():
    data = fetch_coinList()
#    for key in data:
    
    for key in data:
        print(key, data[key]['Id'])

def fetch_coinlist():
    '''
    Convert data retrieved from CryptoCompare to list
    #TODO rename & check dependencies
    '''
    data = fetch_coinList()
    CryptoCompare_coinList_sorted = sorted(list(data.keys()))

    return CryptoCompare_coinList_sorted

#==============================================================================
# def get_coinlogo(fsym):
#     '''
#     Get logo.png from CryptoCompare site
#     
#     Input:
#         * 1x ticker
#     Output: 
#         * Image | Boolean
#     '''
#     if DEBUG==True:
#         fsym = 'BTC'
#     my_file = Path('image/logo_{}.png'.format(fsym))
#     if my_file.is_file():
#         print("File exists")
# #        im = image.imread(my_file)
#         #TODO
#         im = Image.open(my_file)
#     else:
#         try:
#             print("Let's get {} Logo from CryptoCompare".format(fsym))
#             url = "https://www.cryptocompare.com/api/data/coinlist/"
#         
#             print(url)
#             response = requests.get(url)
#         
#             dic = json.loads(response.content)
#             url_logo = dic['BaseImageUrl']+dic['Data'][fsym]['ImageUrl']
#             
#             print("{}".format(url_logo))
#         
#             opener = AppURLopener()
#             response = opener.open(url_logo)
#             im = image.imread(response)
#         except ConnectionError: 
#             print("No active internet connection?")
#             pass
#     
#     try: 
#         return im
#     except NameError:
#         return False
#==============================================================================

def get_portfolio():
    '''
    Get basic data for all coins listed on CryptoCompare
    
    Output:
        * DataFrame ordered by market_cap_usd
    '''
    url = "https://api.coinmarketcap.com/v1/ticker/"
    response = requests.get(url)

#    soup = BeautifulSoup(response.content, "html.parser")
#    dic = json.loads(soup.prettify())

    dic = json.loads(response.content)

    data_list = list(dic[0].keys())

    # create an empty DataFrame
    df = pd.DataFrame(columns=data_list)

    #TODO refactor
#    for i in range(len(dic)):
    for i in range(len(dic)):
        tmp = []
        for e in enumerate(data_list):
#                print("i: {} e[1]: {}".format(i, e[1]))
            tmp.append(dic[i][e[1]])
        df.loc[len(df)] = np.array(tmp)

    df = df_data_to_float(df)

    return df

def get_portfolio_by_marketcap(top=100):
    '''
    Get basic data for all coins listed on CryptoCompare
    
    Input:
        * Int 
    Output:
        * DataFrame ordered by market_cap_usd
    '''
    df = get_portfolio()
    df.sort_values(by=['market_cap_usd'])
    
#     apply conversion to numeric as 'df' contains lots of 'None' string as values
    df.market_cap_usd = pd.to_numeric(df.market_cap_usd)

    # convert all series to numeric
#        try:
#             df.percent_change_24h = pd.to_numeric(df.percent_change_24h)

    # Save those ranked top_x in market_cap_usd
    top_x = int(top)
    df_output = df[(df.index < top_x)]

#    print(P[['symbol', 'percent_change_24h', 'percent_change_7d']], end="\n\n")

#    portfolio = list(df_output.symbol)
#    print(portfolio)

    return df_output

def generate_portfolio_mns(names=False):
    '''
    Output: 
        * unique list of tickers of MasterNode coins
    
    TODO:
        * fetch list from https://twitter.com/jimtalksdata
    '''
    portfolio_description = "MasterNode coins"
    
    #TODO check if list is all listed
    portfolio_tickers = ['8BIT', 'AMS', 'ARC', 'BLOCK', 'BOS', 'BRO',  
                        'BSD', 'BTA', 'CHC', 'CRAVE', 'CRW', 'DASH', 'DMD', 
                        'ENT', 'EON', 'EXCL', 'FLAX', 'ICASH', 'INSN', 'ION', 
                        'LINDA', 'MUE', 'NEOS', 'NTRN', 'PIVX', 'RNS', 'SIB', 
                        'SYNX', 'TX', 'XBY', 'XEM', 'XVC',]
    
#    portfolio_tickers = ['DASH', 'XEM', 'PIVX', 'CHC', 'SIB', 'BLOCK', 'CRW', 'MUE',
#                        'ION', 'NEOS', 'XBY', 'DMD', 'XVC', 'BSD', 'EXCL', 'SYNX',
#                        'BTA', 'INSN', 'TX', 'NTRN', 'ICASH', 'CRAVE', 'RNS',
#                        'ARC', '8BIT', 'ENT', 'FLAX', 'AMS', 'BRO', ]

    return portfolio_tickers, portfolio_description

def generate_portfolio_eth(names=False):
    '''
    Output: 
        * unique list of tickers of MasterNode coins
    
    TODO:
        * fetch list from https://etherscan.io/tokens
    '''
    portfolio_description = "Ethereum & Ether tokens"
    portfolio_tickers = ['ETH', '1ST', 'ANT', 'BAT', 'BCAP', 'BET', 'BQX', 'BTX',
                        'CFI', 'CVC', 'DGD', 'DRP', 'EDG', 'EXP',
                        'FND', 'GNT', 'GUP', 'HKG', 'HMQ', 'ICN', 'INC',
                        'IXT', 'LUN', 'MCO', 'METAL', 'MLN', 'MYST', 'NMR',
                        'OAX', 'OMG', 'OROC', 'PAY', 'PBT', 'PPT', 'PTOY',
                        'REP', 'RLC', 'SHIFT', 'SJCX', 'SNGLS', 'SNT', 'SPT',
                        'SRC', 'STAR', 'SWT', 'TAAS', 'TFL', 'TKN', 'TRST',
                        'UBQ', 'VIP', 'WGR', 'WTT', 'ZRC']

    return portfolio_tickers, portfolio_description

def generate_portfolio_top10(names=False):
    '''
    Returns list of tickers of top 10 coins w/ long history
    '''
    portfolio_description = "10 Large Caps"
    portfolio_tickers = ['BTC', 'ETH', 'LTC', 'ETC', 'XRP', 'DASH', 'XEM', 'XMR', 
               'STRAT', 'ZEC', ]
    
    return portfolio_tickers, portfolio_description

def generate_portfolio_exchanges(names=False):
    '''
    Returns list of tickers of Decentralised Exchanges
    '''
    portfolio_description = "Decentralised Exchanges"
    portfolio_tickers = ['BLOCK', 'MSP', 'BNB', 'WAVES', ]
    
    return portfolio_tickers, portfolio_description
    
def generate_portfolio_anon(names=False):    
    '''
    Returns list of tickers for Anon coins
    '''
    portfolio_description = 'Anonymous cryptocurrencies'
    portfolio_tickers = ['ZEC', 'XVG', 'XZC', 'DASH', 'PIVX', 'XMR', 'ZCL', 
                         'XSPEC', 'ZEN', 'CLOAK', 'XST', 'NAV', ]
#    add_later = ['SDC',]

    return portfolio_tickers, portfolio_description
    
def generate_portfolio_platform(names=False):    
    '''
    Returns list of tickers for Platform assets
    
    IPFS, 
    '''
    portfolio_description = 'Crypto platforms'
    portfolio_tickers = ['ETH', 'NEO', 'LSK', 'WAVES', 'UBIQ', 'STRAT',  ]

    return portfolio_tickers, portfolio_description
    
def generate_portfolio_storage(names=False):    
    '''
    Returns list of tickers for Storage coins
    
    IPFS, 
    '''
    portfolio_description = 'Distributed Storage crypto'
    portfolio_tickers = ['SC', 'STORJ', 'SJCX', ]

    return portfolio_tickers, portfolio_description
    
def generate_portfolio_computing(names=False):    
    '''
    Returns list of tickers for Storage coins
    '''
    portfolio_description = 'Distributed Computing crypto'
    portfolio_tickers = ['ETH', 'RLC', 'GNT',]

    return portfolio_tickers, portfolio_description
    
def generate_portfolio_ico(names=False):    
    '''
    Returns list of tickers for Anon coins
    '''
    portfolio_description = 'Huge ICOs'
    portfolio_tickers = ['BAT', 'BAN', 'PAY', 'CVC', 'EOS', 'SNT', 'QTUM', 
                         'OMG', 'NEO', ]

    return portfolio_tickers, portfolio_description

def generate_portfolio_gambling(names=False):    
    '''
    Returns list of tickers for Crypto Gambling plays
    '''
    portfolio_description = 'Gambling Crypto'
    portfolio_tickers = ['PPY', 'EDG', 'WGR', 'DICE', '1ST', 'FUN', 'BET', 
                         'GAM',]

    return portfolio_tickers, portfolio_description
    
def calculate_VW_EW(df, weight='both'):
    '''
    Calculate Equal Weighted (EW) & Value Weighted portfolio returns 
    Append results to input DataFrame
    
    Input
        * CryptoCompare coinlist API DataFrame
        * weight= 'both' 'EW' or 'VW"
    Output:
        * Input DataFrame with VW/EW rows appended
        
    Assumptions:
        * Supply is constant over time (negligible over 7D timeframe)
    '''
    
    df['market_cap_7d_ago']=df['market_cap_usd']/(1+df['percent_change_7d']/100)
    df['market_cap_24h_ago']=df['market_cap_usd']/(1+df['percent_change_24h']/100)
    df['market_cap_1h_ago']=df['market_cap_usd']/(1+df['percent_change_1h']/100)
    market_cap_now = np.sum(df['market_cap_usd'])
    market_cap_7d_ago = np.sum(df['market_cap_7d_ago'])
    market_cap_24h_ago = np.sum(df['market_cap_24h_ago'])
    market_cap_1h_ago = np.sum(df['market_cap_1h_ago'])
    percent_change_7d_VW = (market_cap_now/market_cap_7d_ago - 1)*100
    percent_change_24h_VW = (market_cap_now/market_cap_24h_ago - 1)*100
    percent_change_1h_VW = (market_cap_now/market_cap_1h_ago - 1)*100
                           
#    df_output = df.copy()

    if weight=='both' or weight=='VW':
        df_VW = pd.DataFrame(columns=df.columns)
        df_VW.loc[0]=[0 for n in range(len(df.columns))]
        df_VW['symbol']="All VW"
        df_VW['percent_change_7d']=percent_change_7d_VW
        df_VW['percent_change_24h']=percent_change_24h_VW
        df_VW['percent_change_1h']=percent_change_1h_VW
        df_VW['market_cap_usd']=market_cap_now

    if weight=='both' or weight=='EW':
        df_EW = pd.DataFrame(columns=df.columns)
        df_EW.loc[0]=[0 for n in range(len(df.columns))]
        df_EW['symbol']="All EW"
        df_EW['percent_change_7d']=df['percent_change_7d'].mean()
        df_EW['percent_change_24h']=df['percent_change_24h'].mean()
        df_EW['percent_change_1h']=df['percent_change_1h'].mean()
        #TODO adjust market cap for equal weighted
        df_EW['market_cap_usd']=df['market_cap_usd'][:20].median()
        df_EW['market_cap_usd']=market_cap_now

    if weight=='both' or weight=='VW':
        df = df.append(df_VW, ignore_index=True)
    if weight=='both' or weight=='EW':
        df = df.append(df_EW, ignore_index=True)

    return df

def mpl_create_fig(figure_title):
    fig = plt.figure()
    mpl_fig_format(fig)
    reference_str = "{}, @NCvanEgmond - Data: @CryptoCompare".format(CURRENT_DATE)
    fig.text(0.5, 1.04, figure_title, va='bottom', ha='center', size=BIGGEST_SIZE)
    fig.text(0.5, 0.0, reference_str, va='top', ha='center', size=SMALL_SIZE)
    
    return fig
    
def mpl_fig_format(fig):
    fig.set_size_inches(8,4)
    #TODO figure out why tight layout breaks the add-logo function
    # https://stackoverflow.com/questions/22734068/matplotlib-tight-layout-causing-runtimeerror
    fig.set_tight_layout(tight=True)
    fig.autofmt_xdate()
#    fig.figimage(im)   

def mpl_axis_format(ax, xseries, yseries, square=False):
        #TODO write legend thing
        '''
        https://stackoverflow.com/questions/23577505/how-to-avoid-overlapping-of-labels-autopct-in-a-matplotlib-pie-chart
        '''
        #TODO not DRY fix
        try:
            ax.set_ylabel(yseries.name)
            ax.set_xlabel(xseries.name)
        except AttributeError:
            print("Some error setting set_xlabels")
    #    ax1.yaxis.set_label_coords(1,1)

        #TODO find out why next line doesn't work
    #    ax1.xaxis.set_label_coords(1,0)
    
        # Generic Axis formatting
        def mpl_format_set_xyaxis(ax):
            ax.axhline(y=0, color='k', linewidth='0.5', )
            ax.axvline(x=0, color='k', linewidth='0.5', )
        
        mpl_format_set_xyaxis(ax)
        
        def mpl_format_set_plotarea(ax, light=True):
            ax.set_facecolor('0.97')
            ax.grid(color='0.9', linestyle='-', linewidth=1, zorder=-1, )
        
        mpl_format_set_plotarea(ax)
                                 
        def square_axis(ax):
            round_to = 25
            lower_bound = min(yseries.min(), xseries.min())
            lower_bound = math.floor(lower_bound/round_to)*round_to
#            lower_bound = -20
            upper_bound = max(yseries.max(), xseries.max())
            upper_bound = math.ceil(upper_bound/round_to)*round_to
#            upper_bound = 80
            ax.axis(xmin=lower_bound, xmax=upper_bound, 
                    ymin=lower_bound, ymax=upper_bound)                    
         
        if square:
            print("do square")
            square_axis(ax)
        else:
            pass
            ax.axis(xmin=-100, xmax=100,ymin=-100,ymax=100,)
            
        ax.axis(xmin=-50, xmax=150, ymin=-50, ymax=150,)
        square_axis(ax)

        ax.tick_params(axis='both', length=1,)
        
        # format tick labels
        def mpl_format_xticks_perc(ax):
            vals = ax.get_xticks()
            ax.set_xticklabels(['{:.0%}'.format(x/100) for x in vals])
        def mpl_format_yticks_perc(ax):
            vals = ax.get_yticks()
            ax.set_yticklabels(['{:.0%}'.format(x/100) for x in vals])
        
        mpl_format_yticks_perc(ax)
        mpl_format_xticks_perc(ax)
        
def mpl_plot_bubble_chart(ax, plot_title, xseries, yseries, bseries, labels, 
                          colors=None, hist=None, 
                          plot_fig=False, log=False):
    '''
    Generate Plot with bubbles & histograms!
    '''

    print("yseries name: {}".format(yseries.name))
    print("xseries name: {}".format(xseries.name))

    ax_title = "{} (bubble size: market cap)".format(plot_title)
    ax.set_title(ax_title, y=1.035)
    
    def series_normalisation(bubble_series, type='zscore'):
        '''
        Normalise data series
        '''
        if type=='zscore':
            # z-score normalisation
            #TODO areas cannot be negative, so absolute values negative z-scores used for bsize
            areas = (bubble_series-bubble_series.mean())/bubble_series.std()
            areas = (areas + abs(areas.min()))
        if type=='minmax':
            # min-max scaling
            areas = (bubble_series-bubble_series.min())/(bubble_series.max()-bubble_series.min())
        
        # areas cannot be negative
        areas = abs(areas)
        return areas

    #TODO feed bubbles into color scale for bubble color
    areas = series_normalisation(bseries, type='zscore')
    
    if type(colors)=='Series':
        print("No conditional formating of the bubbles parsed")
        colors = pd.DataFrame(0, index=np.arange(len(xseries)), columns='placeholder')
    else:
        colors = colors
        
    areas = areas * 500
    ax.scatter(xseries, yseries,
               c=colors, 
               s=areas,
               cmap=plt.cm.Set1, 
#               cmap=plt.cm.YlOrRd, 
               alpha=0.3,
#               alpha="0.3",
                )
    
    def mpl_ax_xlogscale(ax, xseries):
        '''
        Calculate min/max for logscale axis based on data series
        '''
        #TODO make module level function for use elsewhere
        print("mpl_ax_xlogscale")
        ax.set_xscale('log')

        def mpl_axis_log_max(p_ts):
            z = float(p_ts.max())
            if math.floor(z)==0:
                x = math.floor(1/z)
                y = len(str(x)) - 1
                ymax = 10**(-y)
            else:
                y = len(str(math.floor(z)))
                ymax = 10**y
                
            return ymax
        
        def mpl_axis_log_min(p_ts):    
            z = float(p_ts.min())
            if math.floor(z)==0:
                x = math.floor(1/z)
                y = len(str(x)) 
                ymin = 10**(-y)
            else:
                y = len(str(math.floor(z))) -1
                ymin = 10**y
                
            return ymin
    
        return mpl_axis_log_min(xseries), mpl_axis_log_max(xseries)
    

    def mpl_hist(ax, xseries, yseries, orientation='horizontal'):
        '''
        Plot histogram to ax using xseries, yseries
        '''
        print("mpl_hist", orientation)
        binwidth=10
        
        #TODO fix NaNs in data -> "range parameter must be finite"
        
        ax_max = 50
        #TODO make xlim dependent on max bin size
        if orientation=='horizontal':
#            print("orientation: {}".format(orientation))
            ax2 = ax.twiny()
            print(ax_max)
#            ax2.set_ylim([0,ax_max])
            ax2.axis(xmin=0, xmax=ax_max)
#            ax2.set_xlim([0,ax_max])
            ax2.set_xlabel("frequency")
            
            ax2.xaxis.set_label_coords(1,1.05)
#            xseries = yseries
            
        if orientation=='vertical':
#            print("orientation: {}".format(orientation))
            ax2 = ax.twinx()
#            ax2.set_xlim([-100,100])
#            ax2.set_xlim([-50,100])
            #TODO make ylim dependent on max bin size
#            ax2.set_ylim([0,ax_max])
            print(ax_max)
#            ax2.set_xlim([0,ax_max])
            ax2.axis(ymin=0, ymax=ax_max)
            ax2.set_ylabel("frequency")
#            xseries = yseries

        # plot histogram  
#        fig = plt.figure()
#        ax2 = fig.add_subplot(111)
#        yseries = yseries.dropna()
        ax2.hist(yseries, 
                color='0.1', orientation=orientation, 
                alpha=0.08,
                bins=np.arange(min(yseries), max(yseries) + binwidth, binwidth),
#                bins=np.arange(min(yseries), max(yseries) + binwidth, binwidth),
#                bins=20,
                edgecolor='0.25', linewidth=0.2,
#                edgecolor='r', linewidth=1,
                )
        ax2.grid(b='off')
        ax2.tick_params(axis='both', length=1,)
        
#        plt.show()

    #TODO revector code
    if hist=='x' or hist =='both':
        mpl_hist(ax, xseries, yseries, orientation='horizontal')
    if hist=='y' or hist =='both':
        mpl_hist(ax, yseries, xseries, orientation='vertical')
    
    def mpl_label_datapoints(ax, xseries, yseries, labels, highlighted=None):    
        '''
        Labels datapoints in current axis using xseries & yseries coordinates
        
        Input:
            * List with fsym 
        NOTE: plot annotate after adjusting axes to prevent misalignment
        #TODO revector code
        #TODO set fontsize at figure level
        '''
        print("label datapoints")
        
        for i, xy in enumerate(zip(xseries, yseries)):
#            print(i, xy, type(xy))
            #TODO convert to function
#            annotation = "{} \n ({:.2f}%)".format(labels[i], df['percent_change_1h'][i])
#            annotation = "{}".format(labels[i])
            if highlighted:
#                print(i, labels[i])
                if labels[i] in highlighted:
                    annotation = "{}".format(labels[i])
                    fontweight='bold'
                    print("Higlighting {}".format(labels[i]))
                else:
                    fontweight='normal'
                    annotation = "{}".format(labels[i])
                    annotation=""
                ax.annotate(annotation,
                             xy=xy,
                             textcoords='data',
                             fontsize=7,
                             va='center',
                             ha='center',
                             fontweight=fontweight,
                             )
            else:
                fontweight='normal'
                annotation = ""
#                annotation = "{}".format(labels[i])
                annotation = "{}".format(labels.iloc[i])
                ax.annotate(annotation,
                             xy=xy,
                             textcoords='data',
                             fontsize=7,
                             va='center',
                             ha='center',
                             )

    mpl_axis_format(ax, xseries, yseries)
    # call function after general formating to override percent xaxis
    if log:
        xmin, xmax = mpl_ax_xlogscale(ax, xseries)
        ax.axis(xmin=xmin, xmax=xmax)
    # call function after function that might change axis limits
#    highlighted, nom = generate_portfolio_ico()
    highlighted = []
    mpl_label_datapoints(ax, xseries, yseries, labels, highlighted=highlighted)
    
    if plot_fig:
        plt.show()
    
def mpl_plot_boxplots(ax, data, plot_fig=False, timeframe="7D"):
    '''
    Plot boxplots for bis
    
    #TODO remove endogeneity from analysis: Use last weeks MarketCap vs current
    '''        
    top_x = 750

    #TODO evaluate following lines of code
    # Bin the data frame by "a" with 10 bins...
#    data_trim = data[['market_cap_usd', 'percent_change_7d']][:250].dropna()
#    data = data[data.symbol != 'ARC']
    if timeframe == '7D':
        data_trim = data[['market_cap_usd', 'percent_change_7d']].dropna()
        data_trim['market_cap_usd_lw'] = data['market_cap_usd'].divide(1+data['percent_change_7d']/100)
        data_trim = data_trim.sort_values(['market_cap_usd_lw'], ascending=False,)
        data_trim = data[['percent_change_7d']].dropna()
    else:
        data_trim = data[['market_cap_usd', 'percent_change_24h']].dropna()
        data_trim['market_cap_usd_yd'] = data['market_cap_usd'].divide(1+data['percent_change_24h']/100)
        data_trim = data_trim.sort_values(['market_cap_usd_yd'], ascending=False,)
        data_trim = data[['percent_change_7d']].dropna()
    
    df = data_trim.reset_index(drop=True)[:top_x]
    #NOTE: drop last bin, otherwise last obs ends up alone
    #NOTE: make one more bin limit than groups
    bins = np.linspace(df.index.min(), df.index.max(), 16)[:-1]
    groups = df.groupby(np.digitize(df.index, bins))
#    groups.boxplot(subplots=False, rot=90, showfliers=False)
    
    '''
    Plot grouped boxplots
    '''
    # configure
    bin_size = 50

    # config figure
    if plot_fig:
        fig, ax = plt.subplots()
        fig.suptitle("Returns top {} crypto (grouped per 50 by MarketCap) \n {}, @NCvanEgmond, data: @CryptoCompare \n \n".format(top_x, CURRENT_DATE), fontsize=BIGGER_SIZE)
    
    def generate_ylabels_list():
        ylabels = []
        number_of_bins = 15
        for i in range(1,number_of_bins+1):
            #TODO rewrite to make clean variable labels
#            print("{}-{}".format(math.floor(((i-1)*bin_size+1)), math.ceil((i)*bin_size)))
            label_str = ("{}-{}".format(((i-1)*bin_size+1), (i)*bin_size))
            ylabels.append(label_str)
        return ylabels
            
    ylabels = generate_ylabels_list()
        
    #https://github.com/pandas-dev/pandas/issues/5263
    pd_box = groups.boxplot(subplots=False, rot=90, showfliers=False)
#    pd_box = groups.boxplot(subplots=False, rot=90)
    vals = pd_box.get_yticks()
    if timeframe == '7D':
        ylabel="percent_change_7d"
    else:
        ylabel="percent_change_24h"
        
    pd_box.set(xticklabels=ylabels,
            yticklabels=(['{:.0%}'.format(x/100) for x in vals]),
            ylabel=ylabel,
            #TODO rewrite group labels to include market cap in MM USD
            xlabel=("Top n by market capitalisation at start of period"),
            facecolor=('w'),
            )
    pd_box.grid(color='0.9', linestyle='-', linewidth=0.5, zorder=-1,)
    pd_box.axhline(y=0, color='k', linewidth=0.5)
#    pd_box.axis(ymin=-50, ymax=50)
    groups_means = groups.mean()
    mean_bubbles = pd_box.scatter(groups_means.index, groups_means, color='orange', label='Mean group return')
    green_line = mlines.Line2D([],[],color='green', label='Median group return')
    pd_box.legend(handles=[green_line, mean_bubbles], 
#                      fontsize=fs, 
                  loc=3,)
    ax.set_title("Returns top {} crypto (grouped per 50 by MarketCap)".format(top_x),
                 size=MEDIUM_SIZE,)
    
    if plot_fig:
        plt.show()

def mpl_plot_breakeven(ax):
    '''
    Plot line indicating 0% returns for x<0
    '''
    x = np.arange(-50, 0.1, 1)
    y = eval('(abs(x)/(100+x))*100')
    ax.plot(x, y, color='0.8', linewidth='3')

def mpl_plot_fig_basic(fsym, portfolio_description):
#    startTime = datetime.now()
    '''
    Steps to plotting
        1. define portfolio 
        2. get data for portfolio
        3. generate figure
        4. plot to ax
    '''        
    try:
#        data, portfolio_description, fsym
        data
    except NameError:
#        fsym, portfolio_description = generate_portfolio_anon()
        df, top_x = get_dataset(fsym)
#        data = get_portfolio()
#        data = data.dropna()
        
#    top_x = 100
#    df = data[15:top_x]
#    df = data[:top_x]
#    df = data[50:100]
    #TODO highlighted list needs to be set globally / passed to 
#    highlighted = list(df['symbol'][50:100])
    highlighted = list(df['symbol'])
#    df = calculate_VW_EW(df, weight='both')
#    highlighted = ['All EW', 'All VW',]
    
#    figure_title = "The time has come for Anon to shine.."
    #TODO mpl_create_fig() triggers error
    fig = plt.figure()
#    fig = mpl_create_fig(figure_title)
    fig.set_size_inches(8,4)
#    portfolio_description = "top 1-{} by MarketCap".format(top_x) 
#    portfolio_description = "top {} by MarketCap".format(top_x) 
    
#    ax = fig.add_subplot(211)
    ax = fig.add_subplot(111)
#    mpl_plot_pumped(df, portfolio_description, ax, plot_fig=False)
    mpl_plot_momentum(df, portfolio_description, ax, plot_fig=False)
#    mpl_plot_marketcap(df, portfolio_description, ax, plot_fig=False)

    '''
    [] Output fig file
    [] load fig file on the page
    '''
    
    def output_mlp_quantprofile(fig):
        '''
        Export figure to file
        '''
        print('export figure to file')
        #TODO: to prevent clutter: save outputfiles to ./image/folder
#        filename = "image/qp_{}".format(fsym)
#        filename = "/dcai/templates/dcai/momentum_anon"
        filename = "dcai/static/dcai/momentum_anon"
        filename = tempfile.NamedTemporaryFile(
#            dir='static/temp',
            dir='dcai/static/dcai/',
            suffix='.png',delete=False)

        dpi = 250
        fig.savefig(filename, dpi=dpi, facecolor='w', edgecolor='w',
#        fig.savefig(filename, dpi=250, facecolor='0.7', edgecolor='r',
            orientation='landscape', papertype=None, format=None,
            transparent=False, bbox_inches='tight', pad_inches=0,
            frameon=None)

        filename.close()
        plotPng = filename.name.split('/')[-1]
        print(plotPng)
        return plotPng

#    filename = output_mlp_quantprofile(fig)
    
#    return filename

    return fig

#    print("End of mpl_plot_basic: {}".format(datetime.now() - startTime))
    
#    figure_title = "Mid caps are having an awesome week so far"
#    fig = mpl_create_fig(figure_title)
#    fig.set_size_inches(8,8)
#    ax = fig.add_subplot(111)
#    mpl_plot_boxplots(ax, data, plot_fig=False)
    
#    figure_title = "Mid caps are having an awesome day so far"
#    fig = mpl_create_fig(figure_title)
#    fig.set_size_inches(8,8)
#    ax = fig.add_subplot(111)
#    mpl_plot_boxplots(ax, data, plot_fig=False, timeframe="24h",)

def mpl_plot_marketcap(df, portfolio_description, ax, plot_fig=False):
    '''
    Plot bubble plot 
    '''
    print("mpl_test_plot: Let's make a bubble chart")
    
    if plot_fig:
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 12)

    plot_title = "Returns of of {}".format(portfolio_description)
    
    xseries = df['market_cap_usd']
    yseries = df['percent_change_24h']
    bsize = df['market_cap_usd']
    labels = df['symbol']
    colors = df['rank']
    mpl_plot_bubble_chart(ax, 
                          plot_title, 
                          xseries, 
                          yseries, 
                          bsize, 
                          labels,
                          colors,
                          hist='x', # 'both', 'x', 'y'
                          log=True,
                          )

    if plot_fig:
        plt.show()  

def mpl_plot_momentum(df, portfolio_description, ax, plot_fig=False):
    '''
    Plot bubble plot 
    '''
    print("mpl_test_plot: Let's make a bubble chart")
    
    if plot_fig:
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 8)

    plot_title = "Momentum of {}".format(portfolio_description)
    
    xseries = df['percent_change_7d']
    yseries = df['percent_change_24h']
    bsize = df['market_cap_usd']
    labels = df['symbol']
#    labels = labels.reset_index(inplace=True)
    colors = df['rank']
    mpl_plot_bubble_chart(ax, 
                          plot_title, 
                          xseries, 
                          yseries, 
                          bsize, 
                          labels,
                          colors,
#                          hist='both', # 'both', 'x', 'y'
                          )

    if plot_fig:
        plt.show()  

def mpl_plot_pumped(df, portfolio_description, ax, plot_fig=False):
    '''
    Plot bubble plot 
    '''
    print("mpl_test_plot: Let's make a bubble chart")
    
    if plot_fig:
        fig, ax = plt.subplots()
        fig.set_size_inches(12, 12)

    plot_title = "Momentum of {}".format(portfolio_description)
    
    df['24h_vol_over_marcap'] = df['24h_volume_usd']/df['market_cap_usd'] * 100
    xseries = df['percent_change_7d']
    yseries = df['percent_change_24h']
    yseries = df['24h_vol_over_marcap']
    bsize = df['market_cap_usd']
    labels = df['symbol']
    colors = df['rank']
    mpl_plot_bubble_chart(ax, 
                          plot_title, 
                          xseries, 
                          yseries, 
                          bsize, 
                          labels,
                          colors,
                          hist='y', # 'both', 'x', 'y'
                          )

    if plot_fig:
        plt.show()  

def get_dataset(tickers, top_x=50):
    '''
    Get subset of CryptoCompare data based on list input
    
    Input: 
        * List of tickers
    '''
    print("get_dataset")
    #get data for all coins
    #TODO check if this can be more efficient, i.e. not get data for ALL coins
    df = get_portfolio()
    df = df.dropna().reset_index()
#    df = df_data_to_float(df)

#==============================================================================
#     # get data for tickers from dataset
#     startTime = datetime.now()
#     
#     dfb = df.copy()
#     dfb['portfolio'] = 0
#     e=0
#     for i, symbol in enumerate(dfb['symbol']):
#         if symbol in tickers and dfb['market_cap_usd'].loc[i]>0:
# #            print(i, symbol)
#             e=e+1
# #            print("{}. {} is a ETH blockchain asset".format(e, symbol))
#             dfb['portfolio'].loc[i]=1
#               
#     # check if nummber of items =< tickers in portfolio
#     tickers_in_portfolio = np.sum(dfb['portfolio'] == 1)
#     
#     if (tickers_in_portfolio>len(tickers)):
#         print("Numbers don't add up")
#     else:
#         print("Checked numbers: Portfolio checks out")
#         df_portfolio = dfb.where(dfb['portfolio']==1)
#         df_portfolio = df_portfolio.dropna(axis=0, how='all')
# 
#         new_index = np.arange(0,len(df_portfolio), 1)
#         df_portfolio.index = new_index
# 
#         #declutter: Get top 30 by MarketCap
#         top_x = top_x
#         df_portfolio.sort_values(by=['market_cap_usd'])
#         df_portfolio = df_portfolio[(df_portfolio.index < top_x)]
# 
#     df_portfolio = df_portfolio[df_portfolio.columns[:-1]]
#     df = df_portfolio
#     
#     print("Loop method: {}".format(datetime.now() - startTime))
#     return df, top_x  
#==============================================================================
    
    startTime = datetime.now()
    
    dfa = df.copy()
    dfa.index = df['symbol']
    dfalt = dfa.T[tickers].T
    dfalt = df_data_to_float(dfalt)
    dfalt = dfalt.sort_values(by=['market_cap_usd'], ascending=False,)
    dfalt.index = dfalt['rank']-1
    dfalt.index = np.arange(0,len(dfalt), 1)
                       
    if (len(dfalt)>len(tickers)):  
        print("request data for {} coins, got data for {}. Something went wrong?".format(len(tickers), len(dfalt)))
    else:
        print("Portfolio data checks out")
                       
    print("Transpose method: {}".format(datetime.now() - startTime))
    
    return dfalt, top_x  
      
# Main body
if __name__ == '__main__':
#    fsym = "GPU"
#    check_coinlist(fsym)

    # shorter version
#    CryptoCompare_coinList_sorted = fetch_coinlist()
#    ticker in CryptoCompare_coinList_sorted

    '''
    Chart ideas: comparative gains over time since january
    Invest minimum wage to lambo
    
    '''
    mpl_plot_fig_basic()
        
#    p_daily, r_daily = get_dataseries(portfolio_symbol)
#    portfolio_symbol, portfolio_name = generate_portfolio_ETH()
#    list_symbols = df['symbol'].tolist()
#    df_fetch = fetch_prices(list_symbols)

#    def get_dataset_ETH(df):
#        '''
#        
#        '''
#        df = get_portfolio()
#        #TODO write more general version of function
#        portfolio_symbol = generate_portfolio_eth()
#
#        # filter ETH tokens from dataset
#        df['ETH_blockchain'] = 0
#        e=0
#        for i, symbol in enumerate(df['symbol']):
#            if symbol in portfolio_symbol and df['market_cap_usd'].loc[i]>0:
#                e=e+1
#    #            print("{}. {} is a ETH blockchain asset".format(e, symbol))
#                df['ETH_blockchain'].loc[i]=1
#        number_of_ETHs = np.sum(df['ETH_blockchain'] == 1)
#        if (number_of_ETHs>len(portfolio_symbol)):
#            print("numbers don't add up")
#        else:
#            print("Checked numbers: Portfolio checks out")
#            df_ETH = df.where(df['ETH_blockchain']==1)
#            df_ETH = df_ETH.dropna(axis=0, how='all')
#
#            new_index = np.arange(0,len(df_ETH), 1)
#            df_ETH.index = new_index
#
#            #declutter: Get top 30 by MarketCap
#            top_x = 50
#            df_ETH.sort_values(by=['market_cap_usd'])
#            df_ETH = df_ETH[(df_ETH.index < top_x)]
#
#            df = df_ETH
#
#        return df, top_x
    

#
#    tickers, portfolio_description = generate_portfolio_anon()
#    data, top_x = get_dataset(tickers)
#    df = get_portfolio()
#    df, top_x = get_dataset_ETH(df)
#    plot_title = ("Momentum of top {} Ethereum tokens by MarketCap".format(top_x))



#    df = calculate_VW_EW(df)

    #TODO: convert to function
    #NOTE: double matching on name & ticker required
    # insanecoin listed under 2 ticker,
    # two coins listed with $ARC ticker
#    def get_dataset_MN(df):
#        portfolio_symbol, portfolio_name = generate_portfolio_mns(names=True)
#        df['MN'] = 0
#        e=0
#        for i, name in enumerate(df['name']):
#    #        print(name)
#            if name in portfolio_name:
#                symbol = df['symbol'].loc[i]
##                print(symbol)
#                if symbol in portfolio_symbol:
#                    df['MN'].loc[i]=1
#                    e = e+1
##                    print("{} Match: {} == {} is a MN coin".format(e, df['name'].loc[i], name))
#
#        number_of_MNs = np.sum(df['MN'] == 1)
#        if (number_of_MNs>len(portfolio_symbol)):
#            print("numbers don't add up")
#        else:
#            df_MN = df.where(df['MN']>0)
#            df_MN = df_MN.dropna(axis=0, how='all')
#            new_index = np.arange(0,len(df_MN), 1)
#            df_MN.index = new_index
#            df = df_MN
#
#        return df
#
#    def mpl_plot_fig_MNs():
#        '''
#        Plot momentum plot for MasterNode coins
#        '''
#        #TODO clean up!
#        data = get_portfolio()
#        df = get_dataset_MN(data)
#        figure_title = "How are the MasterNode coins doing?"
#        fig = mpl_create_fig(figure_title)
#        portfolio_description = "MasterNode coins".format() 
#        ax = fig.add_subplot(111)
#        mpl_test_plot(df, portfolio_description, ax, plot_fig=False)
#
##    mpl_plot_fig_basic()       
    