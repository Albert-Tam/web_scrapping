import requests

url_odm_organisations = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"

headers = {
    'x-rapidapi-key': "286f6e2b01mshbde2e5493219cdcp1ac1b4jsn7a824a055a5b",
    'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com"
    }

response = requests.request("GET", url_odm_organisations, headers=headers)

print(response.text)



url_odm_people = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-people"

headers2 = {
    'x-rapidapi-key': "286f6e2b01mshbde2e5493219cdcp1ac1b4jsn7a824a055a5b",
    'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com"
    }

response2 = requests.request("GET", url_odm_organisations, headers=headers2)
print(response2.json())

