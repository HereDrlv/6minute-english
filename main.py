import os
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def _download():
    """Download 6 Minute English Podcast"""

    _dir = os.path.dirname(os.path.realpath(__file__))
    _dir = os.path.join(_dir + '/podcasts')
    if not os.path.exists(_dir):
        os.makedirs(_dir)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,bg;q=0.6,mk;q=0.4,ru;q=0.2,uk;q=0.2,mn;q=0.2,ko;q=0.2,ja;q=0.2,da;q=0.2,fr-FR;q=0.2,fr;q=0.2,ar;q=0.2,he;q=0.2,fi;q=0.2,pt-PT;q=0.2,pt;q=0.2,lt;q=0.2,tr;q=0.2',
        'Host': 'www.bbc.co.uk',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'http://www.bbc.co.uk/learningenglish/english/features/6-minute-english',
    }
    session = requests.Session()
    url = 'http://www.bbc.co.uk/learningenglish/english/features/6-minute-english'
    response = session.get(url, headers=headers).content

    # find all podcast links
    soup = BeautifulSoup(response, 'html.parser')
    soup = soup.find('div', attrs={'id': 'bbcle-content'})
    soup = soup.find('div', attrs={'class': 'widget-container widget-container-full'})
    podcast_links = soup.findAll('div', attrs={'class': 'text'})

    # loop through the links
    for p in podcast_links:
        # fetch podcast page and download pdf, mp3 files
        a = p.find('h2').find('a')
        title = a.get_text()
        date = p.find('div', attrs={'class': 'details'}).find('h3').get_text()
        match = re.search(r'(?P<date>\d{2}\s\w{3}\s\d{4})', date)
        date = datetime.strptime(match.group('date'), '%d %b %Y').strftime('%Y-%m-%d')
        title = date + ' ' + title

        url = 'http://www.bbc.co.uk' + a['href']
        response = session.get(url, headers=headers).content

        soup = BeautifulSoup(response, 'html.parser')
        soup = soup.find('div', attrs={'id': 'bbcle-content'})
        soup = soup.find('div', attrs={'class': 'widget-container widget-container-right'})

        pdf = soup.find('div', attrs={'class': 'widget-pagelink-download-inner bbcle-download-linkparent-extension-pdf'})
        mp3 = soup.find('div', attrs={'class': 'widget-pagelink-download-inner bbcle-download-linkparent-extension-mp3'})

        pod_path = os.path.join(_dir + '/' + title)
        if not os.path.exists(pod_path):
            os.makedirs(pod_path)

            pdf_path = os.path.join(pod_path + '/transcript.pdf')
            mp3_path = os.path.join(pod_path + '/audio.mp3')

            response = session.get(pdf.find('a')['href'], headers=headers)
            with open(pdf_path, 'wb') as f:
                f.write(response.content)

            response = session.get(mp3.find('a')['href'], headers=headers)
            with open(mp3_path, 'wb') as f:
                f.write(response.content)

            print('Done .....', title)
        else:
            print('Skip.....', title)
            continue


if __name__ == "__main__":
    _download()
