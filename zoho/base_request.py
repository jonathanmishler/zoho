from typing import ClassVar
from dataclasses import dataclass, asdict

from .api import Zoho


@dataclass
class RequestParams:
    """Dataclass to hold parameters for the request. This can be the base class
    for the params for specific requests.  The method will create a dict of all the
    non-null param values.
    """

    def to_dict(self):
        return {
            key: value for (key, value) in asdict(self).items() if value is not None
        }


@dataclass
class ZohoRequest:
    """ Base Class ***DO NOT USE*** """

    api_client: Zoho
    module: str
    params: RequestParams = RequestParams()
    max_records: int = 1000
    ENDPOINT: ClassVar[str] = None  # used for the application endpoint url
    VALID_MODULES: ClassVar[
        list
    ] = []  # list to include the valid module name endpoints

    def execute(self) -> list:
        data = list()
        if self.module in self.VALID_MODULES:
            raw = self.api_client.get(f"{self.ENDPOINT}{self.module}", self.params.to_dict())
            response = self.parse_response(raw)
            total_count = response.info["count"] + (
                (response.info["page"] - 1) * response.info["per_page"]
            )
            data.extend(response.data)
            print(
                f"Added {response.info['count']} records for a total of {total_count} records"
            )
            if (total_count < self.max_records) and response.info["more_records"]:
                self.params.page = response.info["page"] + 1
                data.extend(self.execute())
        else:
            print(f"Module name {self.module} is not valid")

        return data

    def parse_response(self, resp: dict):
        pass