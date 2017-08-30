# -*- coding: utf-8 -*-

# Imports
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Cryptoasset, CryptoassetVersionOne

# Class declarations
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
        

#TODO rewrite ot HyperlinkedModelSerializer

class CryptoassetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cryptoasset
        fields = '__all__' 
#        fields = ('Name', 'Id', 'Url', 'ImageUrl', 'CoinName', 
#                  'TotalCoinSypply', 'PreminedValue',
#                  'FullName', 'Algorithm', 'ProofType', 'SortOrder')

class CryptoassetV1Serializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializer for catching CryptoCompare v1 API data on tickers
    
    src: https://api.coinmarketcap.com/v1/ticker/
    '''
    class Meta:
        model = CryptoassetVersionOne
        fields = '__all__' 