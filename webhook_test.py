import requests
import json

########## CONFIG ##########
WEBHOOK_URI = "https://webhook.site/5995a36a-ab17-44f5-b257-4759d90eed9b"

data = {
  '名前':'テスト太郎',
  '性別':'男性',
  'URL':'https://laboratory.kazuuu.net/'
}

r = requests.post(
  WEBHOOK_URI,
  data=json.dumps(data),
  headers={
    'Content-Type':'application/json'
  }
)
