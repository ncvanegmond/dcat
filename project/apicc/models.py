from django.db import models
#from concurrency.fields import IntegerVersionField

# Create your models here.
class Cryptoasset(models.Model):
    Id = models.IntegerField(blank=False, primary_key=True,)
    Url = models.CharField(max_length=100, blank=True)
    ImageUrl = models.CharField(max_length=100, blank=True)
    Name = models.CharField(max_length=100, blank=False, unique=True,)
    CoinName = models.CharField(max_length=100, blank=True)
    FullName = models.CharField(max_length=100, blank=True)
    Algorithm = models.CharField(max_length=100, blank=True)
    ProofType = models.CharField(max_length=100, blank=True)
    FullyPremined = models.CharField(max_length=100, blank=True)
    TotalCoinSypply = models.CharField(max_length=100, blank=True)
    PreminedValue = models.CharField(max_length=100, blank=True)
    TotalCoinsFreeFloat = models.CharField(max_length=100, blank=True)
    SortOrder = models.IntegerField(blank=True)
    
    def __str__(self):
        return self.Name
    
#    def get_absolute_url(self):
#        return reverse('dcai:index', kwargs={})
    
    class Meta:
        ordering = ('Name',)
        
class CryptoassetVersionOne(models.Model):
    '''
    Model for catching CryptoCompare v1 API data on tickers
    
    src: https://api.coinmarketcap.com/v1/ticker/
    '''
#    id = models.IntegerField(max_length=100, blank=False, primary_key=True)
#    id = models.CharField(max_length=100, blank=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    symbol = models.CharField(max_length=100, blank=True)
    rank = models.IntegerField(blank=True)
#    rank = models.IntegerField(max_length=100, blank=False)
#    price_usd = models.CharField(max_length=100, blank=True)
#    price_btc = models.CharField(max_length=100, blank=True)
#    24h_volume_usd = models.CharField(max_length=100, blank=True)
#    market_cap_usd = models.CharField(max_length=100, blank=True)
#    available_supply = models.CharField(max_length=100, blank=True)
#    total_supply = models.CharField(max_length=100, blank=True)
#    percent_change_1h = models.CharField(max_length=100, blank=True)
#    percent_change_24h = models.CharField(max_length=100, blank=True)
#    percent_change_7d = models.CharField(max_length=100, blank=True)
#    last_updated = models.CharField(max_length=100, blank=True)
        
    def __str__(self):              # __unicode__ on Python 2
        return self.symbol

#    def get_absolute_url(self):
#        return reverse('dcai:index', kwargs={})
    
    class Meta:
        ordering = ('symbol',)
        
class Portfolio(models.Model):
#    version = IntegerVersionField( )
    pname = models.CharField(max_length=255, blank=False)
    pdescription = models.CharField(max_length=255, blank=False)
    cryptoassets = models.ManyToManyField(CryptoassetVersionOne)    
    
    def __str__(self):              # __unicode__ on Python 2
        return self.pname

#    def get_absolute_url(self):
#        return reverse('dcai:index', kwargs={})
    
    class Meta:
        ordering = ('pname',)