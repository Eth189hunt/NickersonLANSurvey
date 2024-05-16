import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.forms import (
    CheckboxSelectMultiple,
    ChoiceField,
    MultipleChoiceField,
    RadioSelect,
    TypedChoiceField,
)

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
        AGE_18_24 = "1", "18-24"
        AGE_25_34 = "2", "25-34"
        AGE_35_44 = "3", "35-44"
        AGE_45_54 = "4", "45-54"
        AGE_55_64 = "5", "55-64"
        AGE_65_PLUS = "6", "65 or older"

    q1 = RadioSelect(
        max_length=1,
        choices=Ages.choices,
        blank=True,
        null=True,
        verbose_name="Please indicate your age.",
        default="",
    )

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        NON_BINARY = "N", "Non-binary / third gender"
        PREFER_NOT_TO_SAY = "P", "Prefer not to say"

    q2 = RadioSelect(
        max_length=1,
        choices=Gender.choices,
        blank=True,
        null=True,
        verbose_name="What is your gender?",
    )

    class YesNo(models.TextChoices):
        YES = "Y", "Yes"
        NO = "N", "No"

    q3 = RadioSelect(
        max_length=1,
        choices=YesNo.choices,
        blank=True,
        null=True,
        verbose_name="Are you Hispanic or Latino?",
    )

    class Race(models.TextChoices):
        AMERICAN = "AA", "American Indian or Alaska Native"
        ASIAN = "A", "Asian"
        BLACK = "B", "Black or African American"
        NATIVE = "N", "Native Hawaiian or Other Pacific Islander"
        WHITE = "W", "White"
        TWO_OR_MORE = "T", "Two or more races"

    q4 = CheckBoxSelect(
        choices=Race.choices,
        verbose_name="Which of these Categories best indicates your race?",
        blank=True,
        null=True,
        help_text="Please select one or more.",
    )

    class Education(models.TextChoices):
        LESS_THAN_HS = "1", "Less than high school"
        SOME_HS = "2", "Some high school"
        HIGHSCHOOL = "3", "High school graduate or GED"
        TRADE = "4", "Vocational/trade school certificate"
        SOME_COLLEGE = "5", "Some college"
        AS = "6", "Associate degree (AA, AS, etc.)"
        BS = "7", "Bachelor's degree (BA, AB, BS, etc.)"
        MS = "8", "Master's degree (MA, MS, MEd, MSW, MBA, etc.)"
        DDS = "9", "Professional degree (MG, DDS, DVM, LLB, JD, etc.)"
        PHD = "10", "Doctorate degree (PhD, EdD, etc.)"

    q5 = RadioSelect(
        max_length=2,
        choices=Education.choices,
        blank=True,
        null=True,
        verbose_name="What is the highest level of education you have completed?",
    )

    class Income(models.TextChoices):
        LESS_THAN_25k = "1", "Less than $25,000"
        BETWEEN_25_35k = "2", "$25,000 to $34,999"
        BETWEEN_35_50k = "3", "$35,000 to $49,999"
        BETWEEN_50_75k = "4", "$50,000 to $74,999"
        BETWEEN_75_100k = "5", "$75,000 to $99,999"
        BETWEEN_100_150k = "6", "$100,000 to $149,999"
        BETWEEN_150_200k = "7", "$150,000 to $199,999"
        OVER_200k = "8", "$200,000 or more"

    q6 = RadioSelect(
        max_length=2,
        choices=Income.choices,
        blank=True,
        null=True,
        verbose_name="Which category best represents your annual household income?",
    )

    q7 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="How many people reside in your household including you?",
    )

    q8 = RadioSelect(
        max_length=1,
        choices=YesNo.choices,
        blank=True,
        null=True,
        verbose_name="Are you a permanent resident or citizen of the United States?",
    )
    # If no q8
    q9 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="What is your country of origin?",
    )
    # if yes q9
    q10_1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="What is your state of residence?",
    )
    q10_2 = models.IntegerField(
        blank=True, null=True, verbose_name="What is your zip code?"
    )

    # What is the primary purpose of your trip?
    # Please select your top three reasons that best describe the overall purpose of your trip:
    # ** Make these radio select vertical
    class One_two_three(models.TextChoices):
        ONE = "1", "#1"
        TWO = "2", "#2"
        THREE = "3", "#3"

    q11_1 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="To visit National Parks, National Monuments, or National Historic Sites",
    )
    q11_2 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="To escape from an urban setting",
    )
    q11_3 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="To spend time with friends/family",
    )
    q11_4 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="To view wildlife or natural scenery",
    )
    # Break(make some space between fields)
    q11_5 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="To be physically active",
    )
    q11_6 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="To experience relaxtion/renewal",
    )
    q11_7 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="To visit this particular national park",
    )
    q11_8 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="To learn about the culture or history of this area",
    )
    # Break(make some space between fields)
    q11_9 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="Pleasure trip or vacation",
    )
    q11_10 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="Business/professional reasons",
    )
    q11_11 = RadioSelect(
        max_length=1,
        choices=One_two_three.choices,
        blank=True,
        null=True,
        verbose_name="School-related trip",
    )

    class Parks_Places(models.TextChoices):
        ARCHES_NATIONAL_PARK = "A", "Arches National Park"
        BRYCE_CANYON_NATIONAL_PARK = "B", "Bryce Canyon National Park"
        CANYONLANDS_NATIONAL_PARK = "C", "Canyonlands National Park"
        CAPITOL_REEF_NATIONAL_PARK = "D", "Capitol Reef National Park"
        ZION_NATIONAL_PARK = "Z", "Zion National Park"
        GRAND_CANYON_NATIONAL_PARK = "G", "Grand Canyon National Park"
        ROCKY_MOUNTAIN_NATIONAL_PARK = "R", "Rocky Mountain National Park"
        MESA_VERDE_NATIONAL_PARK = "M", "Mesa Verde National Park"
        RAINBOW_BRIDGE_NATIONAL_MONUMENT = "RB", "Rainbow Bridge National Monument"
        NATURAL_BRIDGES_NATIONAL_MONUMENT = "NB", "Natural Bridges National Monument"
        GLEN_CANYON_NATIONAL_RECREATION_AREA_LAKE_POWELL = (
            "GC",
            "Glen Canyon National Recreation Area/ Lake Powell",
        )
        BEAR_EARS_NATIONAL_MONUMENT = "BE", "Bear Ears National Monument"
        HOVENWEEP_NATIONAL_MONUMENT = "H", "Hovenweep National Monument"
        GRANDSTAIRCASE_ESCALANTE_NATIONAL_MONUMENT = (
            "GS",
            "Grand Staircase/Escalante National Monument",
        )
        CEDAR_BREAKS_NATIONAL_MONUMENT = "CB", "Cedar Breaks National Monument"
        MONUMENT_VALLEY = "MV", "Monument Valley"
        FOUR_CORNERS_MONUMENT = "FC", "Four Corners Monument"
        LAS_VEGAS = "LV", "Las Vegas"
        SALT_LAKE_CITY = "SL", "Salt Lake City"
        PHEONIX = "P", "Pheonix"
        DENVER = "D", "Denver"
        PIPE_SPRING_NATIONAL_MONUMENT = "PS", "Pipe Spring National Monument"

    q12 = CheckBoxSelectOther(
        choices=Parks_Places.choices,
        blank=True,
        null=True,
        verbose_name="Please indicate the following places you have visited or will visit on this trip.",
    )
    q12_23_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Other (please list):",
    )

    q13 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="How many nights will you or did you spend away from home on this trip?",
    )

    q14 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="How many nights of this trip will be or were spent in Utah?",
    )

    q15 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="How many people were, are, or will be in your travel group, including you?",
    )

    class TravelWith(models.TextChoices):
        KIDS_UNDER_18 = "K", "Kid(s) under age 18"
        FAMILY = "F", "Family"
        FRIENDS = "F", "Friends"
        ADULTS_20_64 = "A", "Adults (ages 20-64)"
        ADULTS_65_PLUS = "S", "Adults (65+ years old)"
        TOUR_OR_OTHER = "T", "Tour or other group"
        PETS = "P", "Pet(s)"

    q16 = CheckBoxSelect(
        choices=TravelWith.choices,
        blank=True,
        null=True,
        verbose_name="With whom did you travel during this trip?",
    )

    # How important was each of the following reasons for your visit?
    class Importance(models.TextChoices):
        NOT = "1", "Not at all important"
        SLIGHTLY = "2", "Slightly important"
        MODERATELY = "3", "Moderately important"
        VERY = "4", "Very important"
        EXTREMELY = "5", "Extremely important"

    q17_1 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Appreciate the scenic beauty",
    )
    q17_2 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Experience solitude and calmness",
    )
    q17_3 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Spend time with family/friends",
    )
    q17_4 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Travel in an environmentally conscious way",
    )
    q17_5 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Experience nature",
    )
    # break
    q17_6 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Experience local culture and history",
    )
    q17_7 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Experience a sense of challenge",
    )
    q17_8 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Gain knowledge on environmental consciousness and wildlife",
    )
    q17_9 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Experience rest and relaxtion",
    )
    q17_10 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Engage in healthy activities",
    )
    # break
    q17_11 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Experience adventure",
    )
    q17_12 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Experience a luxury vacation",
    )
    q17_13 = RadioSelect(
        max_length=1,
        choices=Importance.choices,
        blank=True,
        null=True,
        verbose_name="Experience a cost-conscious vacation",
    )

    # How well were you able to achieve your motivations? (If it is not applicable, please select not applicable)
    class Achieve(models.TextChoices):
        NOT_APPLICABLE = "1", "Not applicable"
        NOT_AT_ALL = "2", "Not at all achieved"
        SLIGHTLY = "3", "Slightly achieved"
        MODERATELY = "4", "Moderately achieved"
        FULLY = "5", "Fully achieved"

    q18_1 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Appreciate the scenic beauty",
    )
    q18_2 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Experience solitude and calmness",
    )
    q18_3 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Spend time with family/friends",
    )
    q18_4 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Travel in an environmentally conscious way",
    )
    q18_5 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Experience nature",
    )
    # break

    q18_6 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Experience local culture and history",
    )
    q18_7 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Experience a sense of challenge",
    )
    q18_8 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Gain knowledge on environmental consciousness and wildlife",
    )
    q18_9 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Experience rest and relaxtion",
    )
    q18_10 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Engage in healthy activities",
    )
    # break

    q18_11 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Experience adventure",
    )
    q18_12 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Experience a luxury vacation",
    )
    q18_13 = RadioSelect(
        max_length=1,
        choices=Achieve.choices,
        blank=True,
        null=True,
        verbose_name="Experience a cost-conscious vacation",
    )

    class Transportation(models.TextChoices):
        PERSONAL_VEHICLE = "PV", "Personal vehicle"
        RENTAL_CAR = "RC", "Rental car"
        RV = "RV", "RV"
        BUS_SHUTTLE = "BS", "Bus/Shuttle"
        AIRPLANE = "AP", "Airplane"

    q19 = CheckBoxSelectOther(
        choices=Transportation.choices,
        blank=True,
        null=True,
        verbose_name="What forms of transportation did you take between home and the national park(s)?",
        help_text="Please mark all that apply.",
    )

    q19_6_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Other (please list):",
    )

    # If airplance selected
    class Airports(models.TextChoices):
        SALT_LAKE_CITY = "SLC", "Salt Lake City International Airport"
        ST_GEORGE = "SGU", "St. George Regional Airport (St. George)"
        LAS_VEGAS = "LAS", "Harry Reid International Airport (Las Vegas)"
        DENVER = "DEN", "Denver International Airport"
        PHOENIX = "PHX", "Phoenix Sky Harbor International Airport"
        CANYONLANDS = "CNY", "Canyonlands Regional Airport (Moab)"
        OGDEN = "OGD", "Ogden-Hinckley Airport (Ogden)"
        PROVO = "PVU", "Provo Airport (Provo)"
        CEDAR_CITY = "CDC", "Cedar City Regional Airport (Cedar City)"
        OTHER = "O", "Other"

    q20 = RadioSelect(
        max_length=3,
        choices=Airports.choices,
        blank=True,
        null=True,
        verbose_name="If your transportation to a Utah National Park included an airport, please select the last airport visited prior to visiting the National Park(s).",
    )

    q20_10_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Other (please list):",
    )

    # Where did you stay during your National Park(s) visit and how many nights for each?
    q21_1 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Hotel/Lodge",
    )
    q21_2 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Cabin",
    )
    q21_3 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Bed & Breakfast",
    )
    q21_4 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Short-term rental",
    )
    q21_5 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Camping",
    )
    q21_6 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Family/friends",
    )
    q21_7 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Personal seasonal residence",
    )
    q21_8 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Othrer (please specify):",
    )

    # Please indicate the level of importance of the following items fro your visit to this National Park, and the quality of your experience based on your visit
    class Importance2(models.TextChoices):
        VERY_UNIMPORTANT = "1", "Very unimportant"
        SOMEWHAT_UNIMPORTANT = "2", "Somewhat unimportant"
        IMPORTANT = "3", "Important"
        VERY_IMPORTANT = "4", "Very important"

    class Quality(models.TextChoices):
        VERY_POOR = "1", "Very poor"
        POOR = "2", "Poor"
        AVERAGE = "3", "Average"
        VERY_GOOD = "4", "Very good"
        DONT_KNOW_NOT_APPLIABLE = "5", "Don't know/Not applicable"

    q22_1_1 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="National Park entrance experience",
    )
    q22_2_1 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="National Park entrance experience",
    )

    q22_1_2 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Staff providing information or orientation",
    )
    q22_2_2 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Staff providing information or orientation",
    )

    q22_1_3 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Visitor center exhibits",
    )
    q22_2_3 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Visitor center exhibits",
    )

    q22_1_4 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="National Park orientation movie(s)",
    )
    q22_2_4 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="National Park orientation movie(s)",
    )

    q22_1_5 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Visitor center parking",
    )
    q22_2_5 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Visitor center parking",
    )

    q22_1_6 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Visitor center activities",
    )
    q22_2_6 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Visitor center activities",
    )

    q22_1_7 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Roadside and trailside exhibits",
    )
    q22_2_7 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Roadside and trailside exhibits",
    )

    q22_1_8 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Shuttle bus inside National Park",
    )
    q22_2_8 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Shuttle bus inside National Park",
    )

    q22_1_9 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Shuttle bus outside National Park",
    )
    q22_2_9 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Shuttle bus outside National Park",
    )

    q22_1_10 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Hours of shuttle bus operation",
    )
    q22_2_10 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Hours of shuttle bus operation",
    )

    q22_1_11 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Parking within National Park",
    )
    q22_2_11 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Parking within National Park",
    )

    q22_1_12 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Timed entry/reservation process",
    )
    q22_2_12 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Timed entry/reservation process",
    )

    q22_1_13 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Private vehicle traffic flow",
    )
    q22_2_13 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Private vehicle traffic flow",
    )

    q22_1_14 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Overall level of crowding throughout entire National Park visit",
    )
    q22_2_14 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Overall level of crowding throughout entire National Park visit",
    )

    q22_1_15 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Facilitating crowd flow within National Park",
    )
    q22_2_15 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Facilitating crowd flow within National Park",
    )

    q22_1_16 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Opportunity to visit desired National Park destination(s)",
    )
    q22_2_16 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Opportunity to visit desired National Park destination(s)",
    )

    q22_1_17 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Condition of trails",
    )
    q22_2_17 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Condition of trails",
    )

    q22_1_18 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Quantity of trails",
    )
    q22_2_18 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Quantity of trails",
    )

    q22_1_19 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Ranger-led programs",
    )
    q22_2_19 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Ranger-led programs",
    )

    q22_1_20 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Condition of restrooms",
    )
    q22_2_20 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Condition of restrooms",
    )

    q22_1_21 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Quantity of restrooms",
    )
    q22_2_21 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Quantity of restrooms",
    )

    q22_1_22 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Quantity of garbage bins",
    )
    q22_2_22 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Quantity of garbage bins",
    )

    q22_1_23 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Condition of campsites",
    )
    q22_2_23 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Condition of campsites",
    )

    q22_1_24 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Availability of campsites",
    )
    q22_2_24 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Availability of campsites",
    )

    q22_1_25 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Condition of park resources",
    )
    q22_2_25 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Condition of park resources",
    )

    q22_1_26 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="National Park outdoor recreation activities",
    )
    q22_2_26 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="National Park outdoor recreation activities",
    )

    q22_1_27 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Guided tour or other program(s)",
    )
    q22_2_27 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Guided tour or other program(s)",
    )

    q22_1_28 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Accessibility of food (<em>cafes, restaurants, convenience stores</em>)",
    )
    q22_2_28 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Accessibility of food (<em>cafes, restaurants, convenience stores</em>)",
    )

    q22_1_29 = RadioSelect(
        max_length=1,
        choices=Importance2.choices,
        blank=True,
        null=True,
        verbose_name="Excursions and activities within National Park",
    )
    q22_2_29 = RadioSelect(
        max_length=1,
        choices=Quality.choices,
        blank=True,
        null=True,
        verbose_name="Excursions and activities within National Park",
    )

    class Crowded(models.TextChoices):
        NOT_AT_ALL = "1", "Not at all"
        SLIGHTLY = "2", "Slightly"
        MODERATELY = "3", "Moderately"
        VERY = "4", "Very"
        EXTREMELY = "5", "Extremely"

    q23 = RadioSelect(
        max_length=1,
        choices=Crowded.choices,
        blank=True,
        null=True,
        verbose_name="How crowded did you feel while visiting the National Park?",
    )

    # How frequently did you do the following during your National Park visit? (If not applicable, please select not applicable)
    class Frequently(models.TextChoices):
        NEVER = "1", "Never"
        RARELY = "2", "Rarely"
        SOMETIMES = "3", "Sometimes"
        OFTEN = "4", "Often"
        ALWAYS = "5", "Always"
        NOT_APPLICABLE = "6", "Not applicable"

    q24_1 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Prepared for all types of weather, hazards, or emergencies before getting on a trail",
    )
    q24_2 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Scheduled trip to avoid times of high use",
    )
    q24_3 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Stayed on designated or established trailes",
    )
    q24_4 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Walked around wet or muddy sections of a trail",
    )
    q24_5 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Carried out all waste, including food crumbs, peels, or cores",
    )
    # break

    q24_6 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Removed objects from the areas, including a small item like a rock, plant, stick, or feather",
    )
    q24_7 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Approached, fed, or followed wildlife",
    )
    q24_8 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Took breaks away from the trail and other visitors",
    )
    q24_9 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Complied with area regulations",
    )
    q24_10 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Paid attention to wildlife habitat and did not interact with wildlife",
    )
    # break

    q24_11 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Tried not to disrupt the natural fauna and flora",
    )
    q24_12 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Attended environmental improvement activities in the visited destination",
    )
    q24_13 = RadioSelect(
        max_length=1,
        choices=Frequently.choices,
        blank=True,
        null=True,
        verbose_name="Encouraged others to protect the destination's natural environment",
    )

    q25 = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="How many National Parks have you visited?",
    )

    q26 = RadioSelect(
        max_length=1,
        choices=YesNo.choices,
        blank=True,
        null=True,
        verbose_name="Have you visited the state of Utah prior to this trip?",
    )

    class Often(models.TextChoices):
        NOT_AT_ALL = "1", "Not at all"
        ONCE_OR_TWICE = "2", "Once or twice per year"
        SEVERAL_TIMES = "3", "Several times per year"
        NOT_SURE = "4", "Not sure"

    q27 = RadioSelect(
        max_length=1,
        choices=Often.choices,
        blank=True,
        null=True,
        verbose_name="How often do you generally visit National Parks or National Monuments?",
    )

    # Please rank the following National Park aspects from 1 to 10, with 1 being the most valuable aspect to you and 10 being the least valuable aspect to you.
    class Rank(models.TextChoices):
        R1 = "1", "1"
        R2 = "2", "2"
        R3 = "3", "3"
        R4 = "4", "4"
        R5 = "5", "5"
        R6 = "6", "6"
        R7 = "7", "7"
        R8 = "8", "8"
        R9 = "9", "9"
        R10 = "10", "10"

    q28_1 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="The provide enjoyable scenery, sights, sounds, smells, etc.",
    )
    q28_2 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="The provide habitat for a variety of fish, wildlife, plant life, etc.",
    )
    q28_3 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="The are places to pass down the wisdom, knowledge, traditions, and way of life of my ancestors.",
    )
    q28_4 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="The allow future generations to know and experience the area as it is now.",
    )
    q28_5 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="They have places and things of natural and human history that matter to me.",
    )
    q28_6 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="They provide an areas where we can learn about the environment through scientific observation or experimentation.",
    )
    q28_7 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="They provide economic opportunities for communities through tourism, outfitting, guiding, and other services.",
    )
    q28_8 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="The provide a place for my favorite outdoor recreation activity/activities",
    )
    q28_9 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="They have sacred, religious, or spiritual meaning to me or because I feel reverence and respect for the nature there.",
    )
    q28_10 = RadioSelect(
        max_length=2,
        choices=Rank.choices,
        blank=True,
        null=True,
        verbose_name="They make me feel better physically and/or mentally.",
    )
