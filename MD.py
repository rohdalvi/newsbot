from bs4 import BeautifulSoup
import requests

def getMDHeadlines():
    url = 'https://www.michigandaily.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    main_stories = soup.find_all('h2')
    return

def main():
    getMDHeadlines()

if __name__ == "__main__":
    main()
