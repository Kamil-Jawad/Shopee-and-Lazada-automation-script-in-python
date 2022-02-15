import requests as rq

for api in range(0, 450, 6):
    # Endpoint
    url = f'https://shopee.com.my/api/v2/item/get_ratings?filter=0&flag=1&itemid=4441789004&limit=6&offset={api}&shopid=37861061&type=0'
    v = rq.get(url)
    v = v.json()

    # print(v['data']['ratings'][1]['comment'])
    for i in range(0, 6):
        print("Comment :: ", v['data']['ratings'][i]['comment'])
    print('\n-------\n')
