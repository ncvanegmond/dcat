# -*- coding: utf-8 -*-
from django.shortcuts import render

#class IndexView(LoginRequiredMixin, generic.ListView):
def index(request):
    template_name = 'index.html'
    print(request)

#    return render(request, template_name)
    return render(request, template_name, {})