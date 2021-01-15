from bs4 import BeautifulSoup
import requests

def getMDHeadlines():
    url = 'https://www.michigandaily.com/'
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'html.parser')
    headlines = []
    main_stories = soup.find_all('h2')
    main_stories_refined = main_stories[1:7]
    for n in main_stories_refined:
        temp = n.contents[0]
        temp_final = temp.string
        headlines.append(temp_final)

    return headlines

def main():
    getMDHeadlines()

if __name__ == "__main__":
    main()
