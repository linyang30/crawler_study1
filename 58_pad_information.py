from bs4 import BeautifulSoup
import requests

#url = 'http://sz.58.com/pbdn/0/pn1/'
#url = 'http://sz.58.com/pbdn/1/pn1/'
urls = ['http://sz.58.com/pbdn/1/pn{}/'.format(str(i)) for i in range(1, 8)]
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'Cookie': 'id58=c5/ns1gvxx0QW2BvAz/aAg==; ipcity=sz%7C%u6DF1%u5733%7C0; als=0; myfeet_tooltip=end; bj58_id58s="UzJYdGFwdkRaclM3Mzg4OQ=="; sessionid=f3b6988d-a1c2-4477-ad39-73e10a929c77; bangbigtip2=1; channel=58_pc_listing; city=sz; 58home=sz; 58tj_uuid=cebbf905-1d55-4829-a021-dcba11eb0107; new_session=0; new_uv=6; utm_source=; spm=; init_refer=; final_history=28101058728652%2C27180896833987%2C28092350259526%2C28091958846908%2C26122712434093; bj58_new_session=0; bj58_init_refer="http://sz.58.com/sale.shtml?PGTID=0d100000-0000-4981-a21b-90bb6d64fa54&ClickID=1"; bj58_new_uv=7',
            'Referer': 'http://jinzhou.58.com/pingbandiannao/28101058728652x.shtml?adtype=1&PGTID=0d305a36-0000-4ae5-842a-e8fe9a5c6d92&entinfo=28101058728652_0&psid=152171752193929620141641060&iuType=q_1&ClickID=2'
        }

def get_target_urls(urls):
    res_urls = list()
    for url in urls:
        web_response_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_response_data.text, 'lxml')
        pad_informations = soup.select('table.tbimg > tr')
        for pad_information in pad_informations:
            infoid = pad_information.get('logr')[19:33]
            link = pad_information.select('a')[0].get('href')
            unit = {'url':link, 'infoid':infoid}
            res_urls.append(unit)
    return res_urls


def extract_infos(urls):
    datas = list()
    for url in urls:
        web_response_data = requests.get(url['url'], headers=headers)
        soup = BeautifulSoup(web_response_data.text, 'lxml')
        category = soup.select('span.crb_i')[0].get_text().strip()
        title = soup.select('div.col_sub.mainTitle > h1')[0].get_text().strip()
        posting_time = soup.select('li.time')[0].get_text().strip()
        price = soup.select('span.price.c_f50')[0].get_text().strip()
        qulity = soup.select('li > div.su_con > span')[1].get_text().strip()
        if qulity == '-':
            qulity = None
        try:
            region = soup.select('span.c_25d')[0].get_text().strip().replace('\t', '').replace('\r', '').replace('\n', '')
        except Exception:
            region = None

        total_count_url = 'http://jst1.58.com/counter?infoid=%s&userid=&uname=&sid=532883521&lid=2354&px=&cfpath=5,38484' % url['infoid']
        wd_data = requests.get(total_count_url, headers=headers)
        total_count = wd_data.text.split('total=')[1]
        data = [category, title, posting_time, price, qulity, region, total_count]

        datas.append(data)
    return datas


s = get_target_urls(urls)



infos = extract_infos(s)

for info in infos:
    print(info)
