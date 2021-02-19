import httpx

from .auth import ZohoOAuth2


class Zoho:
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
            params={"organization_id": org_id},
        )

    def close(self):
        self.request.close()

    def get(self, url: str, params: dict = None):
        data = None
        response = self.request.get(url, params=params)
        if response.status_code == httpx.codes.OK:
            data = response.json()

        return data
