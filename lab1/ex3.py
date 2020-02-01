import bs4
import requests
from urllib.parse import urljoin

def parseDailyZhihu(url):
    try:
        r = requests.get(url, headers = {"User-Agent":"Chrome"})
        #change headers to avoid being denied by the server.
        r.raise_for_status()
        #this will raise an HTTPError unless the status is 200 which means we get the page successfully
        
        r.encoding = r.apparent_encoding
        #using apparent_coding instead of the encoding in the headers to avoid 
        soup = bs4.BeautifulSoup(r.text,'html.parser')
        l = soup.find_all('a', {'class':'link-button'})
        total = list()
        for m in l:
            ans = [urljoin(url, m.find('img').get('src')), m.find('span').string, urljoin(url, m.get('href'))]
            total.append(ans)
        return total
    except:
        return None

def writeAns(ans, filename):
    with open(filename, 'w') as f:
        for itm in ans:
            f.write(itm[0]+'\n'+itm[1]+'\n'+itm[2])
            f.write('\n')

def main():
    url = "http://daily.zhihu.com/"
    content = parseDailyZhihu(url)      
    writeAns(content, 'res3.txt')

if __name__ == "__main__":
    main()