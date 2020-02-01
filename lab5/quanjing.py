import requests
import bs4

f = open("img_page_urls.txt")

while True:
    try:
        url = f.readline().strip()
        if not url:
            break
        r = requests.get(url, headers={'User-Agent':'Chrome/1.0.0'})
        if 'Img1' in r.text:
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
            img_src = soup.find(id = "Img1").get('src').strip()
            img_src = img_src[:img_src.index('?')]
            tit = soup.find('title').string.strip().replace(' ','')
            tags = soup.find(id = 'Ul1')
            tags_list = list()
            if tags:
                tags_list = tags.find_all('a')
                for i in range(len(tags_list)):
                    tags_list[i] = tags_list[i].string.strip()
            g= open("complete.txt", 'a')
            g.write(url+' '+img_src+' '+tit+' '.join(tags_list)+'\n')
            g.close()
    except:
        pass