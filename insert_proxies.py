import re
from supabase import create_client, Client

# Supabase setup (replace with your actual Supabase details)
url = "https://ubputvpvywbqevyuwupd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVicHV0dnB2eXdicWV2eXV3dXBkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQyNTYxOTAsImV4cCI6MjA0OTgzMjE5MH0.hR1JCWCateTCb3TWi9V6hw2iCQ8Cxj738nFsnGVygvM"
supabase: Client = create_client(url, key)

# Function to parse a proxy URL
def parse_proxy(proxy_url):
    regex = r'(\w+)://([a-f0-9\-]+)@([a-zA-Z0-9\.\-]+):(\d+)\?path=(.*?)&security=(.*?)&encryption=(.*?)&host=(.*?)&fp=(.*?)&type=(.*?)&sni=(.*?)#(.*)'
    match = re.match(regex, proxy_url)

    if match:
        proxy_type, uuid, server, port, path, security, encryption, host, fp, ptype, sni, remark = match.groups()
        return {
            "type": proxy_type,
            "uuid": uuid,
            "server": server,
            "port": int(port),
            "path": path,
            "security": security,
            "encryption": encryption,
            "host": host,
            "fp": fp,
            "network": ptype,
            "sni": sni,
            "remark": remark
        }
    else:
        return None

# Function to insert proxy data into Supabase
def insert_proxy_to_supabase(proxy_data):
    response = supabase.table("db").insert(proxy_data).execute()
    if response.status_code == 201:
        print(f"Inserted proxy: {proxy_data['uuid']}")
    else:
        print(f"Error inserting proxy: {response.error_message}")

# Read the data.txt file and process each line
with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()  # Remove any extra whitespace
        proxy_data = parse_proxy(line)
        if proxy_data:
            insert_proxy_to_supabase(proxy_data)
        else:
            print(f"Invalid proxy URL: {line}")
