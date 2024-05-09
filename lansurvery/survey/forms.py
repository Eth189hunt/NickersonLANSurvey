from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, HTML
from django import forms

from . import models

class NationalParkSatisfactionBehaviorForm(forms.ModelForm):
    class Meta:
        model = models.NationalParkSatisfactionBehavior
        fields = "__all__"
        # fields = ["q1"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.form_tag = False

        self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     "q1",
        # )