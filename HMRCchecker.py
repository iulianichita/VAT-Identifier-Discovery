# returns the right results for the test data from https://github.com/hmrc/vat-registered-companies-api/blob/main/public/api/conf/2.0/test-data/vrn.csv

import os, requests
from dotenv import load_dotenv

load_dotenv()

BASE = "https://test-api.service.hmrc.gov.uk"  # sandbox
tok = requests.post(f"{BASE}/oauth/token", data={
    "client_id": os.environ["HMRC_CLIENT_ID"],
    "client_secret": os.environ["HMRC_CLIENT_SECRET"],
    "grant_type": "client_credentials",
    "scope": "read:vat",
}).json()["access_token"]

def check(vrn):
    r = requests.get(
        f"{BASE}/organisations/vat/check-vat-number/lookup/{vrn}",
        headers={"Accept": "application/vnd.hmrc.2.0+json",
                "Authorization": f"Bearer {tok}"})
    return r.status_code, r.json()

print(check("553557881"))