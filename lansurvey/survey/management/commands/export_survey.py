import csv
import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import models as django_models
from survey import models

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Command to export survey data to a CSV file."
    model = models.NationalParkSatisfactionBehavior

    def handle(self, *args, **options):
        objs = self.model.objects.all()

        headers = [
            "startDate",
            "endDate",
            "status",
            "ipAddress",
            "progress",
            "duration",
            "finished",
            "recordedDate",
            "_recordId",
            "recipientLastName",
            "recipientFirstName",
            "recipientEmail",
            "externalDataReference",
            "locationLatitude",
            "locationLongitude",
            "distributionChannel",
            "userLanguage",
            "QID1",
            "QID2",
            "QID3",
            "QID4",
            "QID5",
            "QID6",
            "QID7_TEXT",
            "QID8",
            "QID9_TEXT",
            "QID10_1",
            "QID10_2",
            "QID11_1",
            "QID11_2",
            "QID11_3",
            "QID11_4",
            "QID11_5",
            "QID11_6",
            "QID11_7",
            "QID11_8",
            "QID11_9",
            "QID11_10",
            "QID11_11",
            "QID12",
            "QID12_23_TEXT",
            "QID13_TEXT",
            "QID14_TEXT",
            "QID15_TEXT",
            "QID17",
            "QID16_1",
            "QID16_2",
            "QID16_3",
            "QID16_4",
            "QID16_5",
            "QID16_6",
            "QID16_7",
            "QID16_8",
            "QID16_9",
            "QID16_10",
            "QID16_11",
            "QID16_12",
            "QID16_13",
            "QID18_1",
            "QID18_2",
            "QID18_3",
            "QID18_4",
            "QID18_5",
            "QID18_6",
            "QID18_7",
            "QID18_8",
            "QID18_9",
            "QID18_10",
            "QID18_11",
            "QID18_12",
            "QID18_13",
            "QID19",
            "QID19_6_TEXT",
            "QID20",
            "QID20_10_TEXT",
            "QID21_1",
            "QID21_2",
            "QID21_3",
            "QID21_4",
            "QID21_5",
            "QID21_6",
            "QID21_7",
            "QID21_8",
            "QID22#1_1",
            "QID22#1_2",
            "QID22#1_3",
            "QID22#1_4",
            "QID22#1_5",
            "QID22#1_6",
            "QID22#1_7",
            "QID22#1_8",
            "QID22#1_9",
            "QID22#1_10",
            "QID22#1_11",
            "QID22#1_12",
            "QID22#1_13",
            "QID22#1_14",
            "QID22#1_15",
            "QID22#1_16",
            "QID22#1_17",
            "QID22#1_18",
            "QID22#1_19",
            "QID22#1_20",
            "QID22#1_21",
            "QID22#1_22",
            "QID22#1_23",
            "QID22#1_24",
            "QID22#1_25",
            "QID22#1_26",
            "QID22#1_27",
            "QID22#1_28",
            "QID22#1_29",
            "QID22#2_1",
            "QID22#2_2",
            "QID22#2_3",
            "QID22#2_4",
            "QID22#2_5",
            "QID22#2_6",
            "QID22#2_7",
            "QID22#2_8",
            "QID22#2_9",
            "QID22#2_10",
            "QID22#2_11",
            "QID22#2_12",
            "QID22#2_13",
            "QID22#2_14",
            "QID22#2_15",
            "QID22#2_16",
            "QID22#2_17",
            "QID22#2_18",
            "QID22#2_19",
            "QID22#2_20",
            "QID22#2_21",
            "QID22#2_22",
            "QID22#2_23",
            "QID22#2_24",
            "QID22#2_25",
            "QID22#2_26",
            "QID22#2_27",
            "QID22#2_28",
            "QID22#2_29",
            "QID23",
            "QID24_1",
            "QID24_2",
            "QID24_3",
            "QID24_4",
            "QID24_5",
            "QID24_6",
            "QID24_7",
            "QID24_8",
            "QID24_9",
            "QID24_10",
            "QID24_11",
            "QID24_12",
            "QID24_13",
            "QID25_TEXT",
            "QID26",
            "QID27",
            "QID28_1",
            "QID28_2",
            "QID28_3",
            "QID28_4",
            "QID28_5",
            "QID28_6",
            "QID28_7",
            "QID28_8",
            "QID28_9",
            "QID28_10",
        ]

        data_cols = [
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
            "q12",
            "q12_23_text",
            "q13",
            "q14",
            "q15",
            "q16",
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
            "q19",
            "q19_6_text",
            "q20",
            "q20_10_text",
            "q21_1",
            "q21_2",
            "q21_3",
            "q21_4",
            "q21_5",
            "q21_6",
            "q21_7",
            "q21_8",
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
            "q23",
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
            "q25",
            "q26",
            "q27",
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
        ]

        data = []
        for obj in objs:
            temp_data = [
                "",  # StartDate
                "",  # EndDate
                "",  # Status
                "",  # IPAddress
                "",  # Progress
                "",  # Duration(in seconds)
                "",  # Finished
                "",  # RecordedDate
                "",  # ResponseId
                "",  # RecipientLastName
                "",  # RecipientFirstName
                "",  # recipientEmail
                "",  # externalDataReference
                "",  # locationLatitude
                "",  # locationLongitude
                "",  # distributionChannel
                "",  # userLanguage
            ]

            for col in data_cols:
                match obj._meta.get_field(col):
                    case models.RadioSelect():
                        # logger.warn("RadioSelect")
                        col_name = f"get_{col}_display"
                        method = getattr(obj, col_name, "")
                        temp_data.append(method())
                        pass
                    case models.CheckBoxSelect():
                        # logger.warn("CheckBoxSelect")
                        col_name = f"get_{col}_display_custom"
                        method = getattr(obj, col_name, "")
                        temp_data.append(method())
                        pass
                    case models.CheckBoxSelectOther():
                        # logger.warn("CheckBoxSelectOther")
                        col_name = f"get_{col}_display_custom"
                        method = getattr(obj, col_name, "")
                        temp_data.append(method())
                        pass
                    case django_models.TextField():
                        # logger.warn("TextArea")
                        col_name = col
                        temp_data.append(getattr(obj, col_name, ""))
                        pass
                    case django_models.CharField():
                        # logger.warn("CharField")
                        col_name = col
                        temp_data.append(getattr(obj, col_name, ""))
                        pass
                    case django_models.IntegerField():
                        # logger.warn("IntegerField")
                        col_name = col
                        temp_data.append(getattr(obj, col_name, ""))
                        pass
                    case _:
                        # logger.warn("Unknown")
                        col_name = col
                        temp_data.append(getattr(obj, col_name, ""))
            data.append(temp_data)

        # logger.warn(data)
        with open("parkexample.csv", mode="r", newline="") as infile:
            reader = csv.reader(infile)
            first_three_rows = [next(reader) for _ in range(3)]

        with open("import.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            # writer.writerow(headers)
            writer.writerows(first_three_rows)
            writer.writerows(data)
