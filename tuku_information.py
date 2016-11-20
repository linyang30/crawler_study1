import json
import requests

url = 'http://exh.zhankoo.com/Decorate/DecorateCase/DecorateCaseSearchJson'
img_base_url = 'http://res.zhankoo.com'
datas = list()

pages = 20

for j in range(1, pages):

    data = {'pageIndex':j}

    web_response_data = requests.post(url, data=data)
    data = json.loads(web_response_data.text)
    total = data['total']
    length = len(data['data'])
    for i in range(length):
        title = data['data'][i]['Title']
        price = data['data'][i]['Price']
        img_url = img_base_url + data['data'][i]['ImageUrl']
        area = data['data'][i]['Area']
        style = data['data'][i]['Style']
        industry_name = data['data'][i]['IndustryName']
        color = data['data'][i]['Color']
        material = data['data'][i]['Material']
        description = data['data'][i]['Description']
        tuku_info = {'title':title, 'price':price, 'img_url':img_url, 'area':area, 'style':style, 'industry_name':industry_name, 'color':color, 'material':material, 'description':description}
        datas.append(tuku_info)

for unit in datas:
    print(unit)


