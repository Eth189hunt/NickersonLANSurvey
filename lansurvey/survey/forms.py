from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Fieldset, Layout
from django import forms

from . import models


class NationalParkSatisfactionBehaviorForm(forms.ModelForm):
    class Meta:
        model = models.NationalParkSatisfactionBehavior
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "q1",
            "q2",
            "q3",
            "q4",
            "q5",
            "q6",
            "q7",
            "q8",
            "q9",
            "q10_1",
            "q10_2",
            HTML(
                """
            <h3>What is the primary purpose of your trip?</h3>
            <p>Please select your top three reasons that best describe the overall purpose of your trip:</p>
            """
            ),
            Fieldset(
                "",
                "q11_1",
                "q11_2",
                "q11_3",
                "q11_4",
                "q11_5",
                "q11_6",
                "q11_7",
                "q11_8",
                "q11_9",
                "q11_10",
                "q11_11",
                css_class="ps-5",
            ),
            "q12",
            "q12_23_text",
            "q13",
            "q14",
            "q15",
            "q16",
            HTML(
                """
            <h3>How important was each of the following reasons for your visit?</h3>
            """
            ),
            Fieldset(
                "",
                "q17_1",
                "q17_2",
                "q17_3",
                "q17_4",
                "q17_5",
                "q17_6",
                "q17_7",
                "q17_8",
                "q17_9",
                "q17_10",
                "q17_11",
                "q17_12",
                "q17_13",
                css_class="ps-5",
            ),
            HTML(
                """
            <h3>How well were you able to achieve your motivations? (If it is not applicable, 
            please select not applicable)</h3>
            """
            ),
            Fieldset(
                "",
                "q18_1",
                "q18_2",
                "q18_3",
                "q18_4",
                "q18_5",
                "q18_6",
                "q18_7",
                "q18_8",
                "q18_9",
                "q18_10",
                "q18_11",
                "q18_12",
                "q18_13",
                css_class="ps-5",
            ),
            "q19",
            "q19_6_text",
            "q20",
            "q20_10_text",
            HTML(
                """
            <h3>Where did you stay during your National Park(s) visit and how many nights for each?</h3>
            """
            ),
            Fieldset(
                "",
                "q21_1",
                "q21_2",
                "q21_3",
                "q21_4",
                "q21_5",
                "q21_6",
                "q21_7",
                "q21_8",
                css_class="ps-5",
            ),
            HTML(
                """
            <h3>Please indicate the level of importance of the following items fro your visit to 
            this National Park, and the quality of your experience based on your visit</h3>
            """
            ),
            Fieldset(
                "",
                "q22_1_1",
                "q22_1_2",
                "q22_1_3",
                "q22_1_4",
                "q22_1_5",
                "q22_1_6",
                "q22_1_7",
                "q22_1_8",
                "q22_1_9",
                "q22_1_10",
                "q22_1_11",
                "q22_1_12",
                "q22_1_13",
                "q22_1_14",
                "q22_1_15",
                "q22_1_16",
                "q22_1_17",
                "q22_1_18",
                "q22_1_19",
                "q22_1_20",
                "q22_1_21",
                "q22_1_22",
                "q22_1_23",
                "q22_1_24",
                "q22_1_25",
                "q22_1_26",
                "q22_1_27",
                "q22_1_28",
                "q22_1_29",
                "q22_2_1",
                "q22_2_2",
                "q22_2_3",
                "q22_2_4",
                "q22_2_5",
                "q22_2_6",
                "q22_2_7",
                "q22_2_8",
                "q22_2_9",
                "q22_2_10",
                "q22_2_11",
                "q22_2_12",
                "q22_2_13",
                "q22_2_14",
                "q22_2_15",
                "q22_2_16",
                "q22_2_17",
                "q22_2_18",
                "q22_2_19",
                "q22_2_20",
                "q22_2_21",
                "q22_2_22",
                "q22_2_23",
                "q22_2_24",
                "q22_2_25",
                "q22_2_26",
                "q22_2_27",
                "q22_2_28",
                "q22_2_29",
                css_class="ps-5",
            ),
            "q23",
            HTML(
                """
            <h3>How frequently did you do the following during your National Park visit? 
            (If not applicable, please select not applicable)</h3>
            """
            ),
            Fieldset(
                "",
                "q24_1",
                "q24_2",
                "q24_3",
                "q24_4",
                "q24_5",
                "q24_6",
                "q24_7",
                "q24_8",
                "q24_9",
                "q24_10",
                "q24_11",
                "q24_12",
                "q24_13",
                css_class="ps-5",
            ),
            "q25",
            "q26",
            "q27",
            HTML(
                """
            <h3>Please rank the following National Park aspects from 1 to 10, with 1 being the 
            most valuable aspect to you and 10 being the least valuable aspect to you.</h3>
            """
            ),
            Fieldset(
                "",
                "q28_1",
                "q28_2",
                "q28_3",
                "q28_4",
                "q28_5",
                "q28_6",
                "q28_7",
                "q28_8",
                "q28_9",
                "q28_10",
                css_class="ps-5",
            ),
        )
