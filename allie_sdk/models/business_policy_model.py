
"""Alation REST API Business Policy Data Models."""

from dataclasses import dataclass, field
from ..core.data_structures import BaseClass, BaseParams
from ..models.custom_field_model import CustomFieldValueItem
from ..core.custom_exceptions import validate_rest_payload, InvalidPostBody

"""

Matrix: Methods VS Required Attributes

| Attribute        | GET  | PUT      | POST     | DELETE |
| ---------------- | ---- | -------- | -------- | ------ |
| id               | X    | X        |          | X      |
| title            | X    | X        | X        |        |
| description      | X    | X        | X        |        |
| otype            | X    |          |          |        |
| ts_created       | X    |          |          |        |
| url              | X    |          |          |        |
| stewards         | X    |          |          |        |
| template_id      |      | X        | X        |        |
| policy_group_ids |      | X (dict) | X (list) |        |
| fields           |      | X        | X        |        |

"""


@dataclass
class BusinessPolicyStewardsField(BaseClass):
    otype:str = field(default=None)
    otype_display_name:str = field(default=None)
    id:int = field(default=None)
    name:str = field(default=None)
    title:str = field(default=None)
    url:str = field(default=None)
    deleted:bool = field(default=None)
    snippet:str = field(default=None)
    photo_url:str = field(default=None)
    email:str = field(default=None)


@dataclass(kw_only = True)
class BusinessPolicyBase(BaseClass):
    id: int
    title: str = field(default=None)
    description: str = field(default=None)

# For GET payload
@dataclass(kw_only = True)
class BusinessPolicy(BusinessPolicyBase):
    otype: str = field(default=None)
    ts_created: str = field(default=None)
    url: str = field(default=None)
    stewards: list[BusinessPolicyStewardsField] = field(default=None)
    # currently GET method does not return:
    # - template_id 
    # - policy group ids
    # - custom fields
    def __post_init__(self):
        if isinstance(self.ts_created, str):
            self.ts_created = self.convert_timestamp(self.ts_created)
        # Make sure the nested stewards dict gets converted to the proper StewardField data class
        if isinstance(self.stewards, list):
            self.stewards = [BusinessPolicyStewardsField.from_api_response(value) for value in self.stewards]


class BusinessPolicyItemBase():
    def _create_fields_payload(self) -> list:
        item: CustomFieldValueItem
        validate_rest_payload(self.fields, (CustomFieldValueItem,))

        return [
            {
                'field_id': item.field_id
                , 'value': item.get_field_values()
            }
            for item in self.fields
        ]

# For POST payload
@dataclass(kw_only = True)
class BusinessPolicyPostItem(BaseClass, BusinessPolicyItemBase):
    title: str # mandatory
    description: str = field(default=None)
    template_id: int = field(default=None)  
    policy_group_ids: list[int] = field(default=None)
    fields: list[CustomFieldValueItem] = field(default=None)

    # PREPARE PAYLOAD
    # make sure payload includes only fields with values
    def generate_api_post_payload(self):
        if self.title is None:
            raise InvalidPostBody("'title' is a required field for the POST payload body")
        payload = {'title': self.title}
        if self.description:
            payload['description'] = self.description
        if self.template_id:
            payload['template_id'] = self.template_id
        if self.policy_group_ids:
            payload['policy_group_ids'] = sorted(self.policy_group_ids)
        if self.fields:
            payload['fields'] = self._create_fields_payload()

        return payload

@dataclass
class BusinessPolicyGroupIds(BaseClass):
    add:list[int] = field(default=None)
    remove:list[int] = field(default=None)
    replace:list[int] = field(default=None)

# For PUT payload
@dataclass(kw_only = True)
class BusinessPolicyPutItem(BusinessPolicyBase, BusinessPolicyItemBase):
    template_id: int = field(default=None)  
    policy_group_ids: BusinessPolicyGroupIds = field(default=None)
    # policy group ids: for updates, the dict includes 'add' and 'remove' fields
    fields: list[CustomFieldValueItem] = field(default=None)
    
    """
    CREATE OUTPUT

    When we create the payload for the API call we can't just pass the data classes as
    payload but have to convert them to standard dicts.
    Since we have nested data classes as well, we have to provide functions to convert
    them to dicts as well.
    Another important point to remember is that we can only pass fields in the payload
    that have actual values, otherwise the request will fail.
    """
    
    def _create_policy_group_ids_payload(self) -> dict:
        
        pg_ids = self.policy_group_ids

        out = {}

        if pg_ids.add:
            out['add'] = pg_ids.add
        if pg_ids.remove:
            out['remove'] = pg_ids.remove
        if pg_ids.replace:
            out['replace'] = pg_ids.replace

        return out

    # PREPARE PAYLOAD
    # make sure payload includes only fields with values
    def generate_api_put_payload(self):
        if self.id is None:
            raise InvalidPostBody("'id' is a required field for the POST payload body")
        payload = {'id': self.id}
        if self.title:
            payload['title'] = self.title
        if self.description:
            payload['description'] = self.description
        if self.template_id:
            payload['template_id'] = self.template_id
        if self.policy_group_ids:
            payload['policy_group_ids'] = self._create_policy_group_ids_payload()
        if self.fields:
            payload['fields'] = self._create_fields_payload()

        return payload

# class for REST API Get filter values
@dataclass
class BusinessPolicyParams(BaseParams):
    id:int = field(default_factory = set)
    search:str = field(default = None)
    deleted:bool = field(default = False)