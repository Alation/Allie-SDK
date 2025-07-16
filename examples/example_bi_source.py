"""
Example of creating, listing, updating and deleting one bi source.

Prerequisites:

- You adjusted the "config.ini" file with your settings.
- ... OPEN ...

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
# LOOKUP ANY REQUIRED DATA
# ================================


# ================================
# CREATE BI SERVER
# ================================

# created_bi_servers = alation.bi_source.create_bi_servers(
#     [
#         allie.BIServerItem(
#             uri = "http://localhost:5000/bi_servers"
#             , title = "BI Server Test"
#             , description = "BI Server Test"
#             , name_configuration = allie.BIServerNameConfiguration(
#                 bi_report = "BI Report"
#                 , bi_datasource = "BI Data Source"
#                 , bi_folder = "BI Folder"
#                 , bi_connection = "BI Connection"
#             )
#         )
#     ]
# )
#
# if created_bi_servers is None:
#     logging.error("Tried to create BI Server but received no response ...")
#     sys.exit(1)
# elif isinstance(created_bi_servers, allie.JobDetailsBIServerPost):
#     if created_bi_servers.status == "successful":
#         created_bi_server_id = created_bi_servers.result.ServerIDs[0]
#         logging.info(f"Number of BI Servers created: {created_bi_servers.result.Count}")
#         logging.info(f"The following BI Servers were created (IDs): {created_bi_server_id}")
#     else:
#         logging.error(f"Tried to create BI Servers but received {created_bi_servers.status}: {created_bi_servers.result}")
# else:
#     logging.error(f"Unexpected result ... I don't know what to do ...")
#     sys.exit(1)
#
# # ================================
# # GET BI SERVERS
# # ================================
#
# existing_bi_servers = alation.bi_source.get_bi_servers()
#
#
# if existing_bi_servers is None or len(existing_bi_servers) == 0:
#     logging.warning("No BI Server was found.")
# elif isinstance(existing_bi_servers, list):
#     logging.info(f"Found {len(existing_bi_servers)} BI Servers:")
#     for d in existing_bi_servers:
#         logging.info(f"{d.title}")
# else:
#     print(f"Unexpected result ... I don't know what to do ...")
#     sys.exit(1)
#
# # ================================
# # GET ONE BI SERVER
# # ================================
#
# existing_bi_servers = alation.bi_source.get_bi_servers(
#     query_params = allie.BIServerParams(
#         oids=[ created_bi_server_id ]
#     )
# )
#
# if existing_bi_servers is None or len(existing_bi_servers) == 0:
#     logging.warning("No BI Server was found.")
# elif isinstance(existing_bi_servers, list):
#     logging.info(f"Found {len(existing_bi_servers)} BI Servers:")
#     for d in existing_bi_servers:
#         logging.info(f"{d.title}")
# else:
#     print(f"Unexpected result ... I don't know what to do ...")
#     sys.exit(1)
#
# # ================================
# # UPDATE BI SERVER
# # ================================
#
# updated_bi_server = alation.bi_source.update_bi_server(
#     bi_server_id = created_bi_server_id
#     , bi_server = allie.BIServerItem(
#             uri = "http://localhost:5000/bi_servers"
#             , title = "BI Server Test"
#             , description = "BI Server Test UPDATED"
#             , name_configuration = allie.BIServerNameConfiguration(
#                 bi_report = "BI Report"
#                 , bi_datasource = "BI Data Source"
#                 , bi_folder = "BI Folder"
#                 , bi_connection = "BI Connection"
#             )
#         )
# )
#
# if updated_bi_server is None:
#     logging.error("Tried to update BI Server but received no response ...")
#     sys.exit(1)
# elif isinstance(updated_bi_server, allie.JobDetails):
#     if updated_bi_server.status == "successful":
#         logging.info(f"BI Server updated.")
#     else:
#         logging.error(f"Tried to update BI Server but received {updated_bi_server.status}: {updated_bi_server.result}")
# else:
#     logging.error(f"Unexpected result ... I don't know what to do ...")
#     sys.exit(1)

# ================================
# DELETE BI SERVER
# ================================

# no method available

# ================================
# CREATE BI FOLDERS
# ================================

bi_server_id = 21 # REMOVE LATER !!!

created_bi_folder = alation.bi_source.create_bi_folders(
    bi_server_id = bi_server_id
    , bi_folders = [
        allie.BIFolderItem(
            name = "Product Data Domains" # required
            , external_id = "product_data_domains" # required
            , source_url = "/a/b/c" # required
            , bi_object_type = "Project"
            , description_at_source = "And here goes the description ..."
            , owner = "Peter Summer"
            , created_at = "2025-04-10T00:00:00.000000-08:00"
            , last_updated = "2025-04-10T00:00:00.000000-08:00"
            , num_reports = 2
            , num_report_accesses = 343
            , parent_folder = ""
        )
    ]
)

"""
async_results: [{'msg': 'Job finished in 0.092239 seconds at 2025-04-17 10:00:55.383912+00:00', 'result': ['1 BIFolder object(s) received, 1 new object(s) created', 'BI_V2_API_SYNCING took 0.09s'], 'status': 'successful'}]
created_bi_folder = [JobDetails(status='successful', msg='Job finished in 0.051855 seconds at 2025-04-17 13:26:40.148839+00:00', result=['1 BIFolder object(s) received, 1 existing object(s) updated', 'BI_V2_API_SYNCING took 0.05s'])]
"""

if created_bi_folder is None:
    logging.error("Tried to create BI Folder but received no response ...")
    sys.exit(1)
elif isinstance(created_bi_folder, list):
    for c in created_bi_folder:
        if c.status == "successful":
            created_bi_server_result = c.result[0]
            logging.info(f"Number of BI Servers created: {created_bi_server_result}")
        else:
            logging.error(f"Tried to create BI Folders but received {created_bi_folder.status}: {created_bi_folder.result}")
else:
    logging.error(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)

# ================================
# GET BI FOLDERS
# ================================


existing_bi_folders = alation.bi_source.get_bi_folders(
    bi_server_id = bi_server_id
)

"""
response = [{'id': 16, 'external_id': 'parent_workspace_folder', 'name': 'Workspaces', 'created_at': None, 'last_updated': None, 'source_url': None, 'bi_object_type': 'PowerBI Workspaces', 'owner': None, 'description_at_source': None, 'num_reports': 0, 'num_report_accesses': 0, 'popularity': 0.0, 'parent_folder': None, 'subfolders': ['2a41d8b2-038d-49f2-8afc-24520bab929f'], 'connections': [], 'reports': [], 'datasources': []}, {'id': 17, 'external_id': '2a41d8b2-038d-49f2-8afc-24520bab929f', 'name': 'Acme Bank Workspace', 'created_at': None, 'last_updated': None, 'source_url': 'groups/2a41d8b2-038d-49f2-8afc-24520bab929f', 'bi_object_type': 'New Workspace', 'owner': None, 'description_at_source': None, 'num_reports': 2, 'num_report_accesses': 0, 'popularity': None, 'parent_folder': 'parent_workspace_folder', 'subfolders': [], 'connections': [], 'reports': ['663b9e9a-d6dc-4554-a0d3-9379a6586897', '90274a21-e533-4506-b23a-2f5e6b75e15c'], 'datasources': ['919cf9a1-cd06-422a-b239-b82948e0dde1']}]
existing_bi_folders = [BIFolder(id=16, name='Workspaces', external_id='parent_workspace_folder', source_url=None, bi_object_type='PowerBI Workspaces', description_at_source=None, owner=None, created_at=None, last_updated=None, num_reports=0, num_report_accesses=0, parent_folder=None, popularity=0.0, subfolders=['2a41d8b2-038d-49f2-8afc-24520bab929f'], connections=[], reports=[]), BIFolder(id=17, name='Acme Bank Workspace', external_id='2a41d8b2-038d-49f2-8afc-24520bab929f', source_url='groups/2a41d8b2-038d-49f2-8afc-24520bab929f', bi_object_type='New Workspace', description_at_source=None, owner=None, created_at=None, last_updated=None, num_reports=2, num_report_accesses=0, parent_folder='parent_workspace_folder', popularity=None, subfolders=[], connections=[], reports=['663b9e9a-d6dc-4554-a0d3-9379a6586897', '90274a21-e533-4506-b23a-2f5e6b75e15c'])]
"""

existing_bi_folder_ids = []

if existing_bi_folders is None or len(existing_bi_folders) == 0:
    logging.warning("No BI Folders were found.")
elif isinstance(existing_bi_folders, list):
    logging.info(f"Found {len(existing_bi_folders)} BI Folders:")
    for d in existing_bi_folders:
        logging.info(f"{d.name}")
        existing_bi_folder_ids.append(d.id)
else:
    print(f"Unexpected result ... I don't know what to do ...")
    sys.exit(1)


# ================================
# DELETE BI FOLDERS
# ================================


deleted_bi_folders = alation.bi_source.delete_bi_folders(
    bi_server_id = bi_server_id
    # , query_params = allie.BISourceBaseParams(
    #     oids = existing_bi_folder_ids
    # )
)

deleted_bi_folders