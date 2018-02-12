import urllib.request
import requests

def getHTML(url):
    print("getting " + url)
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    return html


def Post(url, text):
    headers = {
        'Content-Type': 'text/plain'
    }
    r = requests.post(url, headers=headers, data=text)
    res = r.json()
    return res


if __name__ == '__main__':
    urls = getHTML('https://www.oyohyee.com/sitemap.txt')
    res = Post(
        'http://data.zz.baidu.com/urls?site=www.oyohyee.com&token=Ah36uCNcnwq2q7LX', urls)
    print(res)
