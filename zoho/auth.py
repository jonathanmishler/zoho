import urllib
import http.server
import webbrowser
import httpx


class ZohoOAuth2(httpx.Auth):
    """ HTTPX custom authorization class to preform the OAuth 2.0
    implementation on the Zoho API.  See all OAuth API docs at:
    https://www.zoho.com/accounts/protocol/oauth.html
    """

    SCHEME = "https"
    BASE = "accounts.zoho.com"

    def __init__(self, client_id, client_secret, scope, redirect):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.redirect = redirect
        self.grant_token = None
        self.access_token = None

        # Initalize OAuth 2.0 Process
        self.grant_request()
        self.access_request()

    def auth_flow(self, request):
        """ For each HTTPX request, this will add the access token
        to the header according to the Zoho API documentation.
        """
        request.headers["Authorization"] = f"Zoho-oauthtoken {self.access_token}"
        response = yield request
        if response.status_code == 401:
            # Retry the OAuth Process
            self.grant_request()
            self.access_request()
            request.headers["Authorization"] = f"Zoho-oauthtoken {self.access_token}"
            yield request

    def grant_request(self):
        """ Opens a Web Browser to log in and grant access.  This first step
        creates a grant token to use in requesting the access token.        
        """
        path = "/oauth/v2/auth"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": self.scope,
            "redirect_uri": self.redirect,
        }
        query = urllib.parse.urlencode(params, True)
        grant_access_url = urllib.parse.urlunsplit(
            (self.SCHEME, self.BASE, path, query, "")
        )
        webbrowser.open_new(grant_access_url)
        httpServer = http.server.HTTPServer(("localhost", 8080), HTTPAuthHandler)
        httpServer.handle_request()
        if hasattr(httpServer, "grant_token"):
            self.grant_token = httpServer.grant_token[0]

    def access_request(self):
        """ Using the grant token, this second step creates a access token
        without a refresh token.  This access token with expire in 1 hour.
        If you require a connection lasting longer than 1 hour, then you can 
        modify the grant_access() step to change the access type in the Zoho 
        API.
        """
        if self.grant_token is not None:
            path = "/oauth/v2/token"
            params = {
                "code": self.grant_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect,
                "grant_type": "authorization_code",
            }
            response = httpx.post(f"{self.SCHEME}://{self.BASE}{path}", params=params)
            response_attr = response.json()
            self.access_token = response_attr.get("access_token", None)


class HTTPAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        query = urllib.parse.urlparse(self.path).query
        query = urllib.parse.parse_qs(query)
        if "code" in query.keys():
            self.wfile.write(
                bytes("<html><h1>You may now close this window.</h1></html>", "utf-8")
            )
            self.server.grant_token = query["code"]
        else:
            self.wfile.write(
                bytes(
                    "<html><h1>Something went wrong.  Please Try Again</h1></html>",
                    "utf-8",
                )
            )
