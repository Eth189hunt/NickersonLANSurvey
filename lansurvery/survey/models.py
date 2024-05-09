from django.db import models

class NationalParkSatisfactionBehavior(models.Model):
    # Radio select form
    class Ages(models.TextChoices):
        AGE_18_24 = '1', '18-24'
        AGE_25_34 = '2', '25-34'
        AGE_35_44 = '3', '35-44'
        AGE_45_54 = '4', '45-54'
        AGE_55_64 = '5', '55-64'
        AGE_65_PLUS = '6', '65 or older'
    q1 = models.CharField(max_length=1, choices=Ages.choices, verbose_name="Please indicate your age.")

    # Radio select form
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        NON_BINARY = "N", "Non-binary / third gender"
        PREFER_NOT_TO_SAY = "P", "Prefer not to say"
    q2 = models.CharField(max_length=1, choices=Gender.choices, verbose_name="What is your gender?")

    # Radio select form
    class YesNo(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'
    q3 = models.CharField(max_length=1, choices=YesNo.choices, verbose_name="Are you Hispanic or Latino?")

    # Multiple choice form
    class Race(models.TextChoices):
        AMERICAN = 'AA', 'American Indian or Alaska Native'
        ASIAN = 'A', 'Asian'
        BLACK = 'B', 'Black or African American'
        NATIVE = 'N', 'Native Hawaiian or Other Pacific Islander'
        WHITE = 'W', 'White'
        TWO_OR_MORE = 'T', 'Two or more races'
    q4 = models.CharField(max_length=2, choices=Race.choices, verbose_name="Which of these Categories best indicates your race?", help_text="Please select one or more.")

    # Radio select form
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
    q5 = models.CharField(max_length=2, choices=Education.choices, verbose_name="What is the highest level of education you have completed?")