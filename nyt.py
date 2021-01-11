import os
import requests
import json
from api_fetch import getNYT_API_KEY

API_KEY = getNYT_API_KEY()

def getHeadlines(topic):
    print("Fetching " + topic +  " headlines")

    base_url = "https://api.nytimes.com/svc/topstories/v2/{}.json?api-key={}"
    request_url = base_url.format(topic,API_KEY) 

    r = requests.get(request_url)
    data = r.text
    data_dict = json.loads(data)
    relevant_data_dict = data_dict['results']
    headlines = []
    abstracts = []
    for key in relevant_data_dict:
        headlines.append(key['title'])
        abstracts.append(key['abstract'])

    headlines = headlines[0:3]  
    abstracts = abstracts[0:3]  

    nyt_dict = dict(zip(headlines, abstracts))
    
    return nyt_dict

def main():
    getHeadlines("us")

if __name__ == "__main__":
    main()