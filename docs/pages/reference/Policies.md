---
title: Policies
parent: SDK Reference
---

# Policies
{:.no_toc}

* TOC
{:toc}

## Models

### BusinessPolicyStewardsField
Individual list item returned in the `stewards` field of the item `BusinessPolicy`. 

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| id          | int                   | The API ID of the steward assigned to the policy.                                                      |
| otype   | str                   | Type of steward. Response is either `user` or `groupprofile` |
| otype_display_name | str                   | The display name of the otype. Response is either `User` or `Group Profile`                  |
| name  | str              | The name of the steward. Response is either the name of the individual user or `Steward` for groups.   |
| title     | str | The title of the steward.                                 |
| url        | str                  | The Alation url of the steward                                               |
| deleted  | bool              | Deleted status of the steward   |
| snippet     | str |                                  |
| photo_url        | str                  | The Alation url to the photo of the steward                                               |
| email        | str                  | The email of the steward                                               |


### BusinessPolicyBase
Sub-model used in the parent Models of `BusinessPolicy` and `BusinessPolicyPutItem`.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| id          | int                   | The API ID assigned to the policy.                                                      |
| title   | str                   | The title of the policy. |
| description | str                   | The discription of the policy                  |

### BusinessPolicy
Individual list item returned in the response of the function `get_business_policies` that represents a policy in Alation.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| otype          | str                   | the Policy object type name, value being `business_policy`.                                                      |
| ts_created   | datetime                   | The ISO 8601 formatted date of when the policy was created. |
| stewards | list                   | A list of `BusinessPolicyStewardsField` objects with information on the stewards that are associated to the Policy.

### BusinessPolicyPostItem
Python object used to create a `BusinessPolicy` in Alation and passed in the parameter `business_policies` as a list in the function `create_business_policies`.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| title        |  TRUE    | str                   | The title of the Policy.                                     |
| description  |  FALSE   | str                   | The description of the Policy.                               |
| template_id  |  FALSE   | int                   | The ID of the custom template to be assigned to this Policy. | 
| policy_group_ids  |  FALSE   | list              | A list containing the Policy Group IDs that this Policy should be a member of. | 
| fields  |  FALSE   | list              | A list of `CustomFieldValueItem` objects containing custom field information relative to the custom template ID specified by `template_id`. This will get updated as metadata content for this Policy. | 


### BusinessPolicyGroupIds
An item returned as part of the field `policy_group_ids` in the item `BusinessPolicyPutItem` containing the Policy Group operation that this Policy should be a member of and array of respective policy group IDs.

Attributes:

| Name        | Type                  | Description                                                                              |
|-------------|-----------------------|------------------------------------------------------------------------------------------|
| add         | list                   | A list of integer IDs of policy groups to be added to the existing set of associated policy groups policy.                                                      |
| remove   | list                   | A list of integer IDs of policy groups to be removed from the existing set of associated policy groups |
| replace | list                   | A list of integer IDs of policy groups to be freshly associated. As a result, any existing set of associated policy groups will be overwritten
                  |                                                                 |

### BusinessPolicyPutItem
Python object used to update a `BusinessPolicy` in Alation and passed in the parameter `business_policies` as a list in the function `update_business_policies`.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| template_id  |  FALSE   | int                   | The ID of the custom template to be assigned to this Policy. | 
| policy_group_ids        |  FALSE    | BusinessPolicyGroupIds                   | Item containing the Policy Group operation that this Policy should be a member of and array of respective policy group IDs.                                     |
| fields  |  FALSE   | list              | A list of `CustomFieldValueItem` objects containing custom field information relative to the custom template ID specified by `template_id`. This will get updated as metadata content for this Policy. | 


### BusinessPolicyParams
Optional item used to filter the response of the returned data from the function `get_business_policies`.

Attributes:

| Name  | Type  | Description                                                                                                                |
|-------|-------|----------------------------------------------------------------------------------------------------------------------------|
| id   | int   | The integer ID of the policy to return   |
| search | str   | Filter by Policy title  |
| deleted | bool   | Will return only deleted entities when set to true.  |

## Methods

### get_business_policies

```
get_business_policies(query_params:BusinessPolicyParams = None) -> list[BusinessPolicy]:
```

Query multiple Alation Business Policies and return their details

Args:
* query_params (BusinessPolicyParams): REST API Business Policy Query Parameters.
Returns:
* list: Alation Business Policies with each item being represented as a `BusinessPolicy` object

### create_business_policies

```
create_business_policies(business_policies: list[BusinessPolicyPostItem]) -> list[JobDetails]
```

Create Business Policies in Bulk

Args:
* business_policies: list of `BusinessPolicyPostItem` objects

Returns:
* List of JobDetails: Status report of the executed background jobs.

### update_business_policies

```
update_business_policies(business_policies: list[BusinessPolicyPutItem]) -> list[JobDetails]
```

Bulk Update Business Policies in Bulk

Args:
* business_policies: list of `BusinessPolicyPutItem` objects

Returns:
* List of JobDetails: Status report of the executed background jobs.

### delete_business_policies

```
delete_business_policies(business_policies: list[BusinessPolicy]) -> list[JobDetails]
```

Delete an Alation policy.

Args:
* business_policies: list of `BusinessPolicy` objects to be deleted.
  
Returns:
* Job details

## Examples

### Create a policy

See `/examples/example_policy.py`.