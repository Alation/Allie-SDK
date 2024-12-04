"""
Example of listing groups.

Prerequisites:

- You adjusted the "config.ini" file with your settings.

"""

import allie_sdk as allie
import logging
import sys
import configparser

# ================================
# Set Global Variables
# ================================


# ================================
# Define Logging Config
# ================================

logging.basicConfig(
  level=logging.INFO
  , stream = sys.stdout
  , format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================================
# Source Global Config
# ================================

config = configparser.ConfigParser()
config.read("config.ini")

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
# FETCH USER
# ================================

get_users_response = alation.user.get_users(
    allie.UserParams(
        id = 1
    )
)

if get_users_response:
    display_name = get_users_response[0].display_name
    print(f"The display name of user with id 1 is: {display_name}")

# or alternatively you can use this method as well
get_users_response = alation.user.get_a_user(
    user_id = 1
)

if get_users_response:
    display_name = get_users_response.display_name
    print(f"The display name of user with id 1 is: {display_name}")

# ================================
# GET DETAILS OF AUTHENTICATED USER
# ================================

get_authenticated_user_response = alation.user.get_authenticated_user()

if get_authenticated_user_response:
    email = get_authenticated_user_response.email
    print(f"The email of the authenticated user is: {email}")

# ================================
# GET DUPLICATE ALATION USERS AS CSV
# ================================

get_duplicated_users_response = alation.user.get_generate_dup_users_accts_csv()

if isinstance(get_duplicated_users_response, allie.JobDetails):
    if get_duplicated_users_response.status == "successful":
        print(get_duplicated_users_response.msg)
    else:
        print(get_duplicated_users_response.result)
else:
    # write get_csv_result CSV into a file
    with open('/tmp/dup_users.csv', 'w') as csv_file:
        csv_file.write(get_duplicated_users_response)

"""
Sample output (str): 

SN,Username,email,Action,Group\r\n1,api_user,api_user@mail.com,RETAIN/SUSPEND,1\r\n2,Api_user,api_user@mail.com,RETAIN/SUSPEND,1\r\n

"""

# ================================
# POST CSV TO REMOVE DUPLICATE ALATION USERS
# ================================

remove_duplicated_users_response = alation.user.post_remove_dup_users_accts(
    csv_file = "/tmp/dup_users.csv"
)

"""
Sample input in a file:
SN,Username,email,Action,Group\r\n
1,APIUser1,apiuser@alation.com,RETAIN,1\r\n
2,APIUSER1,apiuser1@alation.com,SUSPEND,1\r\n
"""

if remove_duplicated_users_response:
    if remove_duplicated_users_response.status == "successful":
        print(remove_duplicated_users_response.msg)
    else:
        print(remove_duplicated_users_response.result)