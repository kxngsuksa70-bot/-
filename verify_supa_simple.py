
import requests

url = "https://hbbqwcesmwqnfgkmdayp.supabase.co/rest/v1/teachers?select=count"
headers = {
    "apikey": "sb_publishable_Ln1_Vu-1Moho5_l6CsfMIQ_ZwVpPcj6",
    "Authorization": "Bearer sb_publishable_Ln1_Vu-1Moho5_l6CsfMIQ_ZwVpPcj6"
}

try:
    print(f"Testing connection to {url}...")
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
