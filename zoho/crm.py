from typing import Optional, Union, ClassVar
from dataclasses import dataclass
from .base_request import ZohoRequest, RequestParams


@dataclass
class CrmResponse:
    data: dict
    info: dict


@dataclass
class CrmParams(RequestParams):
    fields: Optional[str] = None
    """ To retrieve specific field values.
    Possible values: Comma separated field API names. Example: Last_Name,Email """
    ids: Optional[str] = None
    """ To retrieve specific records based on their unique ID.
    Possible values: Valid unique IDs of records. Example: 4150868000001944196 """
    sort_order: Optional[str] = None
    """ To sort the list of records in either ascending or descending order.
    Possible values:asc - ascending order; desc - descending order """
    sort_by: Optional[str] = None
    """ Specify the API name of the field based on which the records must be sorted.
    Possible values: Field API names. Example: Email """
    converted: Union[str, bool] = False
    """ To retrieve the list of converted records. Default value is false.
    Possible values:true - get only converted records; false - get only non-converted records; both - get all records """
    approved: Union[str, bool] = True
    """ To retrieve the list of approved records. Default value is true.
    Possible values:true - get only approved records; false - get only records which are not approved; both - get all records """
    page: int = 1
    """ To get the list of records from the respective pages. Default value for page is 1.
    Possible values: Positive Integer values only. """
    per_page: int = 200
    """ To get the list of records available per page. Default value for page is 200.
    Possible values: Positive Integer values only. """
    cvid: Optional[str] = None
    """ To get the list of records in a custom view.
    Possible values: {custom_view_id} which you can get using custom view metadata API. """
    territory_id: Optional[str] = None
    """ To get the list of records in a territory.
    Possible values: {territory_id} which you can get using Territory API. """
    include_child: bool = False
    """ To include records from the child territories. Default is false.
    Possible values:true - include child territory records; false -does not include child territory records """


@dataclass
class CrmRequest(ZohoRequest):
    params: CrmParams = CrmParams()
    ENDPOINT: ClassVar[str] ="https://www.zohoapis.com/crm/v2/"
    VALID_MODULES: ClassVar[list] = [
        "Leads",
        "Accounts",
        "Contacts",
        "Deals",
        "Campaigns",
        "Tasks",
        "Cases",
        "Events",
        "Calls",
        "Solutions",
        "Products",
        "Vendors",
        "Price Books",
        "Quotes",
        "Sales Orders",
        "Purchase Orders",
        "Invoices",
        "Custom",
        "Activities",
    ]

    def parse_response(self, resp: dict):
        return CrmResponse(data=resp["data"], info=resp["info"])
