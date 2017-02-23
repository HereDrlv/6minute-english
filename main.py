import os
import re
from datetime import datetime
import requests
import wget
from bs4 import BeautifulSoup


def _download():
    """Download 6 Minute English Podcast"""

    _dir = os.path.dirname(os.path.realpath(__file__))
    _dir = os.path.join(_dir + '/podcasts')
    if not os.path.exists(_dir):
        os.makedirs(_dir)

    headers = {
        # 'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        # 'Content-Type': 'text/plain;charset=UTF-8',
        'Host': 'www.bbc.co.uk',
        # 'Origin': 'http://www.bbc.co.uk/learningenglish/english/features/6-minute-english',
        # 'Referer': 'http://www.bbc.co.uk/learningenglish/english/features/6-minute-english',
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

        pod_path = os.path.join(_dir + '/' + title)
        pdf_path = os.path.join(pod_path + '/transcript.pdf')
        mp3_path = os.path.join(pod_path + '/audio.mp3')

        if not os.path.exists(pod_path) or not os.path.exists(pdf_path) or not os.path.exists(mp3_path):
            if not os.path.exists(pod_path):
                os.makedirs(pod_path)

            url = 'http://www.bbc.co.uk' + a['href']
            response = requests.get(url, headers=headers).content

            soup = BeautifulSoup(response, 'html.parser')
            soup = soup.find('div', attrs={'id': 'bbcle-content'})
            soup = soup.find('div', attrs={'class': 'widget-container widget-container-right'})

            pdf = soup.find('a', attrs={'class': 'download bbcle-download-extension-pdf'})
            mp3 = soup.find('a', attrs={'class': 'download bbcle-download-extension-mp3'})

            if not os.path.exists(pdf_path):
                wget.download(pdf['href'], pdf_path)

            if not os.path.exists(mp3_path):
                wget.download(mp3['href'], mp3_path)

            print('Done .....', title)
        else:
            print('Skip.....', title)
            continue


if __name__ == "__main__":
    _download()
