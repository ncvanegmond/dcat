from .base import *

SECRET_KEY = env('DJANGO_SECRET_KEY', default='^+duvk^m9q1$bs9__&j18idqcpe@(dgxd&%=iuh9di631m%fq$')

DEBUG = env.bool('DJANGO_DEBUG', default=True)