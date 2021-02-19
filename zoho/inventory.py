from typing import Optional, Union, ClassVar
from dataclasses import dataclass
from .base_request import ZohoRequest, RequestParams


@dataclass
class InvResponse:
    data: dict
    info: dict


@dataclass
class InvParams(RequestParams):
    pass


@dataclass
class CrmRequest(ZohoRequest):
    params: InvParams = InvParams()
    ENDPOINT: ClassVar[str] = "https://inventory.zoho.com/api/v1/"
    VALID_MODULES: ClassVar[list] = []

    def parse_response(self, resp: dict):
        return InvResponse(data=resp["data"], info=resp["info"])
