import requests

url = 'https://hacker-news.firebaseio.com/v0/item/27680136.json'

myObj = {
  'title': 'title',
  'url': 'url',
  'by': 'by'
}

response = requests.get(url, data=myObj)
r = response.json()

print(r['title'], r['by'], r['url'])
