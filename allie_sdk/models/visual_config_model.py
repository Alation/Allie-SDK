
"""Alation REST API Visual Config Data Models."""
import logging
from dataclasses import dataclass, field
from ..core.data_structures import BaseClass, BaseParams
from ..core.custom_exceptions import validate_rest_payload, InvalidPostBody

@dataclass(kw_only=True)
class VisualConfigComponent(BaseClass):
    # Rendered object type for the visual config component.
    rendered_otype: str = field(default=None)
    # The unique ID of the field to include in this component. If it's a custom field, this property is required.
    rendered_oid: int = field(default=None)
    # If the component_type is PAGE_DEFINED, this field is required and must be set to the page defined type.
    # Otherwise, its value is null.
    page_defined_type: str = field(default=None)
    # Type of the component:
    # BUILT_IN refers to a field that's defined and provided by Alation but whose value is editable.
    # PAGE_DEFINED refers to a read-only field that's associated with a particular object type and whose value is derived from the object itself.
    # USER_DEFINED refers to a custom field that's defined by catalog admins.
    component_type: str = field(default=None)
    # Panel where the component is rendered.
    # MAIN refers to the wide left panel, and
    # SIDEBAR refers to the narrow right panel on a catalog page.
    panel: str = field(default=None)

    def generate_api_payload(self) -> dict:

        payload = dict()

        # API endpoint validator throws error if rendered_otype is not present
        # so we add it in any case:
        payload['rendered_otype'] = self.rendered_otype

        if self.rendered_oid:
            payload['rendered_oid'] = self.rendered_oid

        if self.component_type.upper() not in ['BUILT_IN', 'PAGE_DEFINED', 'USER_DEFINED']:
            raise InvalidPostBody(f"The component type '{self.component_type}' is not supported")
        else:
            payload['component_type'] = self.component_type.upper()

        if self.page_defined_type is None:
            if self.component_type == 'PAGE_DEFINED':
                raise InvalidPostBody(f"The page defined type must be set if component type is PAGE_DEFINED")
            # API endpoint validator throws error if page_defined_type is not present
            # so we add it in any case:
            payload['page_defined_type'] = self.page_defined_type
        else:
            payload['page_defined_type'] = self.page_defined_type

        if self.panel.upper() not in ['MAIN', 'SIDEBAR']:
            raise InvalidPostBody(f"The panel type '{self.panel}' is not supported")
        else:
            payload['panel'] = self.panel

        return payload


@dataclass(kw_only=True)
class VisualGroupedComponent(BaseClass):
    # Label for the group component. aka Group Name
    label:str = field(default = None)
    # Indicates if a group component should be open by default.
    open_by_default:bool = field(default = False)
    # Panel where the component is rendered.
    # MAIN refers to the wide left panel, and
    # SIDEBAR refers to the narrow right panel on a catalog page.
    panel:str = field(default = None)
    # Specifies if the component is a group. It must always be set to true, as it is intended only for grouped components.
    is_group:bool = field(default = True)
    components:list[VisualConfigComponent] = field(default = None)

    def __post_init__(self):
        # Make sure the nested custom fields gets converted to the proper data class
        if isinstance(self.components, list):
            components_out = []
            if len(self.components) > 0:
                for value in self.components:
                    if isinstance(value, dict):
                        if all(var in value.keys() for var in ("rendered_otype", "rendered_oid", "panel")):
                            components_out.append(VisualConfigComponent.from_api_response(value))
                    else:
                        # handle anything else
                        components_out.append(value)
                self.components = components_out

    def generate_api_payload(self) -> dict:
        payload = dict()

        if self.label is None:
            raise InvalidPostBody(f"The label must be set")
        else:
            payload['label'] = self.label

        if self.open_by_default:
            payload['open_by_default'] = self.open_by_default

        if self.panel.upper() not in ['MAIN', 'SIDEBAR']:
            raise InvalidPostBody(f"The panel type '{self.panel}' is not supported")
        else:
            payload['panel'] = self.panel

        if self.is_group:
            payload['is_group'] = self.is_group

        if self.components is None:
            raise InvalidPostBody(f"components must be set")
        else:
            components_out = []
            for value in self.components:
                components_out.append(VisualConfigComponent.generate_api_payload(value))
            payload['components'] = components_out

        return payload


@dataclass(kw_only = True)
class VisualConfigBase(BaseClass):
    # Title of the template for this visual config.
    title:str = field(default = None)
    # Object type that the visual config is associated with.
    layout_otype:str = field(default = None)
    component_list_in_config:list[VisualConfigComponent | VisualGroupedComponent] = field(default = None)

    def __post_init__(self):
        # Make sure the nested custom fields gets converted to the proper data class
        if isinstance(self.component_list_in_config, list):
            components_out = []
            if len(self.component_list_in_config) > 0:
                for value in self.component_list_in_config:
                    if isinstance(value, dict):
                        if all(var in value.keys() for var in ("rendered_otype", "rendered_oid", "panel")):
                            components_out.append(VisualConfigComponent.from_api_response(value))
                        elif all(var in value.keys() for var in ("label", "panel", "components")):
                            components_out.append(VisualGroupedComponent.from_api_response(value))
                    else:
                        # handle anything else
                        components_out.append(value)
                self.component_list_in_config = components_out


@dataclass(kw_only = True)
class VisualConfigItem(VisualConfigBase):

    # Currently collection_type_id is only available for POST and PUT requests.
    collection_type_id:int = field(default = None)
    def generate_api_payload(self) -> dict:

        payload = dict()

        # collection_type_id is optional
        if self.collection_type_id:
            payload['collection_type_id'] = self.collection_type_id

        if self.title is None:
            raise InvalidPostBody(f"The title must be set")
        else:
            payload['title'] = self.title

        if self.layout_otype is None:
            raise InvalidPostBody(f"The layout_otype must be set")
        else:
            payload['layout_otype'] = self.layout_otype

        if self.component_list_in_config is None:
            raise InvalidPostBody(f"The component_list_in_config must be set")
        else:
            component_list_in_config_out = []
            for value in self.component_list_in_config:
                if isinstance(value, VisualConfigComponent):
                    component_list_in_config_out.append(VisualConfigComponent.generate_api_payload(value))
                elif isinstance(value, VisualGroupedComponent):
                    component_list_in_config_out.append(VisualGroupedComponent.generate_api_payload(value))
                else:
                    logging.error(f"The component_list_in_config '{value}' is not supported")

                payload['component_list_in_config'] = component_list_in_config_out

        return payload

@dataclass(kw_only=True)
class VisualConfig(VisualConfigBase):
    # Unique ID of the visual config.
    id: int = field(default=None)