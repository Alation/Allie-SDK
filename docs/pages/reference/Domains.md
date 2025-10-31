---
title: Domains
parent: SDK Reference
---


# Domains
{:.no_toc}

* TOC
{:toc}

## Models

### Domain

Python object returned by the `get_domains` method:

Attributes:

| Name  | Type    | Description                |
|-------|---------|----------------------------|
| id    | integer | Domain object id           |
| title | string  | Title of the Domain object |
| description | string | Description of the Domain object |
| parent_id | integer | The id of the domain's parent, if it has one. |


### DomainParams

Optional item used to filter the response of the returned data from the function `get_domains`.

Attributes:

| Name      | Type    | Description                |
|-----------|---------|----------------------------|
| parent_id | integer | The id of the parent of the domain           |

### DomainMembership

Python object used to create a Domain Membership and passed in the parameter `domain_membership` in the function `assign_objects_to_domain`.

Attributes:

| Name          | Type      | Description  |
|---------------|-----------|--------------|
| id            | int       | Domain id, to which objects will be added. |
| exclude       | bool      | Should it unassign objects from the domain? (By default, it's false. i.e. it will assign the objects to the domain.) |
| recursive     | bool      | When enabled, will automatically include children of the specified objects as members of the domain. When recursive is set to true, children of the specified objects will automatically be included as members of the domain. Available for the following object types: data (data sources), schema, table, article, bi_server, bi_folder, bi_report, bi_datasource, and glossary_v3 (glossaries). When adding or excluding recursively, try to avoid applying redundant or overlapping domain assignments, as it may cause additional load and delays in applying domain membership assignments. For example, if a schema and its children are already assigned to a domain, recursively assigning that same domain to the schema's parent data source creates redundant assignments for the schema. Recursive membership assignment is best used when targeting isolated and unconnected sets of objects, for example multiple independent schemas or multiple articles that are not part of the same child tree.    |
| oid | list[int] | List of object IDs to be assigned to the domain. |
| otype | str | otype of the Catalog Objects |

### DomainMembershipRuleRequest

Python object used to filter domain membership rules returned by `view_domain_membership_rules`.

Attributes:

| Name       | Type | Description |
|------------|------|-------------|
| domain_ids | list[int] | Domain identifiers whose rules should be returned. |
| exclude    | bool | Return rules that exclude (`True`) or include (`False`) objects in a domain. |
| recursive  | bool | Optional. Filter rules that are recursive (`True`) or non-recursive (`False`). |

### DomainMembershipRule

Python object returned by the `view_domain_membership_rules` method.

Attributes:

| Name | Type | Description |
|------|------|-------------|
| domain_id | integer | Identifier of the domain where the rule is applied. |
| exclude | bool | Indicates whether objects are excluded (`True`) or included (`False`). |
| recursive | bool | Indicates if the rule applies recursively to descendants. |
| otype | string | Catalog object type that the rule targets. |
| oid | integer | Identifier of the catalog object affected by the rule. |

## Methods

### get_domains

```
get_domains(self, query_params: DomainParams = None) -> list[Domain]
```

Get all domains and their details.

Args:
* query_params (`DomainParams`): REST API Get Filter Values.

Returns:
* list: list of Alation Domains

### assign_objects_to_domain

```
assign_objects_to_domain(self, domain_membership: DomainMembership) -> list[JobDetails]
```

Enables you to assign Alation objects (e.g. documents) to a given domain.

Args:
- `domain_membership`: Alation `DomainMembership` object

Returns:
- List of Job Details

### view_domain_membership_rules

```
view_domain_membership_rules(
    self,
    rules_request: DomainMembershipRuleRequest
) -> list[DomainMembershipRule]
```

Browse the membership rules that are applied to the requested domains.

Args:
- `rules_request`: Filters describing which rules should be returned.

Returns:
- List of `DomainMembershipRule` instances representing the matching rules.

## Examples

See `/examples/example_domain.py`.