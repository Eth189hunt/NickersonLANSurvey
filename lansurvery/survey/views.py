from django.shortcuts import render
from django.views.generic import CreateView

from . import models, forms

class NationalParkSatisfactionBehaviorView(CreateView):
    template_name = "survey/national_park.html"
    model = models.NationalParkSatisfactionBehavior
    form_class = forms.NationalParkSatisfactionBehaviorForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
