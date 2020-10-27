import json
import requests

data = {}
apps_to_copy = []

with open ("config.json", 'r') as f:
    data = json.load(f)
    SOURCE_ORG = data['SOURCE_ORG']
    TARGET_ORG = data['TARGET_ORG']
    SRC_KEY = data['SRC_KEY']
    TRGT_KEY = data['TRGT_KEY']
    f.close()

src_headers = {"Accept": "application/json", "Content-Type":"application/json", "Authorization": f"SSWS {SRC_KEY}"}
src_session = requests.Session()
src_session.headers.update(src_headers)
trg_headers = {"Accept": "application/json", "Content-Type":"application/json", "Authorization": f"SSWS {TRGT_KEY}"}
trg_session = requests.Session()
trg_session.headers.update(trg_headers)

app_list = src_session.get(SOURCE_ORG + "/api/v1/apps")

for app in app_list.json():
    if app['name'] == 'oidc_client':
        apps_to_copy.append(app)

with open("report.csv", 'w') as f:
    for app in apps_to_copy:
        app.pop('id')
        del(app['status'])
        del(app['lastUpdated'])
        del(app['created'])
        del(app['accessibility'])
        del(app['visibility'])
        del(app['features'])
        del(app['_links'])
        del(app['credentials']['signing'])
        del(app['credentials']['oauthClient']['client_id'])
        r = trg_session.post(TARGET_ORG + "/api/v1/apps", json.dumps(app))
        status = 0
        if r.status_code == 200:
            f.write(f"{app['label']},SUCCESS\n")
        else:
            f.write(f"{app['label']},FAIL\n")
    f.close()
