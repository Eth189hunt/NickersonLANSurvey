from django.db import models
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple, MultipleChoiceField, RadioSelect, ChoiceField, TypedChoiceField
import logging

logger = logging.getLogger(__name__)

class RadioSelectField(TypedChoiceField):
    widget = RadioSelect

class CheckBoxSelectField(MultipleChoiceField):
    widget = CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        # Fix some of the kwargs
        self.required = kwargs.pop("required", True)
        del kwargs["coerce"]

        # Remove initial choices
        kwargs["choices"].pop(0)
        if "empty_value" in kwargs:
            del kwargs["empty_value"]

        super().__init__(*args, **kwargs)


class CheckBoxSelectOtherField(CheckBoxSelectField):
    widget = CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        # Add the other field
        kwargs["choices"] += [("OTHER", "Other")]
        super().__init__(*args, **kwargs)


class MultipleChoiceField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = ""
        self.max_length = self.get_max_length_choices()

    def to_python(self, value):
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(
                self.error_messages["invalid_list"], code="invalid_list"
            )
        return [str(val) for val in value]

    def validate(self, value, model_instance):
        """Validate that the input is a list or tuple."""
        self.required = True
        if self.required and not value:
            raise ValidationError(self.error_messages["required"], code="required")
        # Validate that each value in the value list is in self.choices.
        for val in value:
            if not self.valid_value(val):
                raise ValidationError(
                    self.error_messages["invalid_choice"],
                    code="invalid_choice",
                    params={"value": val},
                )

    def valid_value(self, value):
        """Check to see if the provided value is a valid choice."""
        text_value = str(value)
        for k, v in self.choices:
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if value == k2 or text_value == str(k2):
                        return True
            else:
                if value == k or text_value == str(k):
                    return True
        return False

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return value.split(",")

    def get_prep_value(self, value):
        if isinstance(value, list):
            return ",".join(value)
        return value
    
    def get_max_length_choices(self):
        total = 0
        for choice in self.choices:
            total += len(choice[0])
        
        # Multiply by 2 to account for commas
        total = total * 2
        return total


class CheckBoxSelectOther(MultipleChoiceField):
    def formfield(self, **kwargs):
        choices_form_class = CheckBoxSelectOtherField
        return super().formfield(choices_form_class=choices_form_class, **kwargs)


class CheckBoxSelect(MultipleChoiceField):
    def formfield(self, **kwargs):
        choices_form_class = CheckBoxSelectField
        return super().formfield(choices_form_class=choices_form_class, **kwargs)

class RadioSelect(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = ""

    def formfield(self, **kwargs):
        choices_form_class = RadioSelectField
        return super().formfield(choices_form_class=choices_form_class, **kwargs)

class NationalParkSatisfactionBehavior(models.Model):
    class Ages(models.TextChoices):
        AGE_18_24 = '1', '18-24'
        AGE_25_34 = '2', '25-34'
        AGE_35_44 = '3', '35-44'
        AGE_45_54 = '4', '45-54'
        AGE_55_64 = '5', '55-64'
        AGE_65_PLUS = '6', '65 or older'
    q1 = RadioSelect(max_length=1, choices=Ages.choices, verbose_name="Please indicate your age.", default="")

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        NON_BINARY = "N", "Non-binary / third gender"
        PREFER_NOT_TO_SAY = "P", "Prefer not to say"
    q2 = RadioSelect(max_length=1, choices=Gender.choices, verbose_name="What is your gender?")

    class YesNo(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'
    q3 = RadioSelect(max_length=1, choices=YesNo.choices, verbose_name="Are you Hispanic or Latino?")

    class Race(models.TextChoices):
        AMERICAN = 'AA', 'American Indian or Alaska Native'
        ASIAN = 'A', 'Asian'
        BLACK = 'B', 'Black or African American'
        NATIVE = 'N', 'Native Hawaiian or Other Pacific Islander'
        WHITE = 'W', 'White'
        TWO_OR_MORE = 'T', 'Two or more races'
    q4 = CheckBoxSelect(choices=Race.choices, verbose_name="Which of these Categories best indicates your race?", help_text="Please select one or more.")

    class Education(models.TextChoices):
        LESS_THAN_HS = '1', 'Less than high school'
        SOME_HS = '2', 'Some high school'
        HIGHSCHOOL = '3', 'High school graduate or GED'
        TRADE = '4', 'Vocational/trade school certificate'
        SOME_COLLEGE = '5', 'Some college'
        AS = '6', 'Associate degree (AA, AS, etc.)'
        BS = '7', "Bachelor's degree (BA, AB, BS, etc.)"
        MS = '8', "Master's degree (MA, MS, MEd, MSW, MBA, etc.)"
        DDS = '9', "Professional degree (MG, DDS, DVM, LLB, JD, etc.)"
        PHD = '10', "Doctorate degree (PhD, EdD, etc.)"
    q5 = RadioSelect(max_length=2, choices=Education.choices, verbose_name="What is the highest level of education you have completed?")