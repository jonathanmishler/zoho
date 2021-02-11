import httpx

from .auth import ZohoOAuth2


class Zoho:
    """ BASE CLASS DO NOT USE """

    def __init__(
        self,
        org_id: str,
        client_id: str,
        client_secret: str,
        redirect: str,
        scope: list,
    ):
        self.auth = ZohoOAuth2(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            redirect=redirect,
        )
        self.request = httpx.Client(
            auth=self.auth,
            base_url=self.ENDPOINT,
            params={"organization_id": org_id},
        )

    def close(self):
        self.request.close()

    def all(self, module: str):
        return self.get(f"{module}")[module]

    def record(self, module: str, record_id: str):
        return self.get(f"{module}/{record_id}")[module[:-1]]

    def records(self, module: str, record_ids: list):
        record_list = list()
        if record_ids:
            record_list = [self.record(module, record_id) for record_id in record_ids]

        return record_list

    def get(self, endpoint: str):
        data = None
        response = self.request.get(f"{endpoint}")
        if response.status_code == httpx.codes.OK:
            data = response.json()

        return data

class Inv(Zoho):
    ENDPOINT = "https://inventory.zoho.com/api/v1/"

class Crm(Zoho):
    ENDPOINT = "https://www.zohoapis.com/crm/v2/"