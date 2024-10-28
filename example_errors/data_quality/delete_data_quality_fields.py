"""
Example of the delete request for DQ fields failing

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- Set the variables in the "Set Global Variables" section below.

"""

import allie_sdk as allie
import logging
import sys
import configparser


# ================================
# Define Logging Config
# ================================

logging.basicConfig(
  level=logging.INFO
  , stream = sys.stdout
  , format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================================
# Set Global Variables
# ================================
DQ_FIELD_KEY = "no-existing-rule-name"



# ================================
# Source Global Config
# ================================

config = configparser.ConfigParser()
config.read("./../config.ini")

ALATION_USER_ID = config.get(section = "api", option = "ALATION_USER_ID")
ALATION_BASE_URL = config.get(section = "api", option = "ALATION_BASE_URL")
ALATION_API_REFRESH_TOKEN = config.get(section = "api", option = "ALATION_API_REFRESH_TOKEN")

# ================================
# Create session with your Alation instance
# ================================

alation = allie.Alation(
    host = ALATION_BASE_URL
    , user_id = ALATION_USER_ID
    , refresh_token = ALATION_API_REFRESH_TOKEN
)



# ================================
# Delete a data health rule and child values
# ================================

result_2 = alation.data_quality.delete_data_quality_fields(
        [
            allie.DataQualityField(
                key=DQ_FIELD_KEY
            )
        ]
    )

print(result_2)

"""
Expected result: successful

The job API returns a success, however, we can see that under
result > fields > not_found:

count = 1

=> Developers will have to check for this value whether the execution was really successful or not.

[
    JobDetailsDataQuality(
        status='successful'
        , msg='Job finished in 0.007528 seconds at 2024-10-28 11:23:46.395550+00:00'
        , result=JobDetailsDataQualityResult(
            fields=JobDetailsDataQualityResultAction(
                created=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                , deleted=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                , not_found=JobDetailsDataQualityResultActionStats(
                    count=1
                    , sample=[{'field_key': 'no-existing-rule-name'}]
                )
            )
            , values=JobDetailsDataQualityResultAction(
                created=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                , updated=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                , deleted=JobDetailsDataQualityResultActionStats(count=0, sample=[])
                , not_found=JobDetailsDataQualityResultActionStats(count=0, sample=[])
            )
            , created_object_attribution=JobDetailsDataQualityResultCreatedObjectAttribution(
                success_count=0
                , failure_count=0
                , success_sample=[]
                , failure_sample=[]
            )
            , flag_counts={}
            , total_duration=0.009011203997943085
        )
    )
]
"""
