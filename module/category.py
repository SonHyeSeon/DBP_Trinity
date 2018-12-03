import pandas as pd
import numpy as np
import json 

# csv파일 read - video_data(video_id, publish_time, trending_date, views .etc)
videos_us = pd.read_csv('../youtube-new/USvideos.csv')
videos_ca= pd.read_csv('../youtube-new/CAvideos.csv')
videos_de = pd.read_csv('../youtube-new/DEvideos.csv')
videos_fr = pd.read_csv('../youtube-new/FRvideos.csv')
videos_gb = pd.read_csv('../youtube-new/GBvideos.csv')

used_category_1 = np.union1d(videos_us['category_id'], videos_ca['category_id']) # english(us + ca)
used_category_2 = np.union1d(used_category_1, videos_gb['category_id']) # english(us + ca + gb)
used_category_3 = np.union1d(videos_de['category_id'], videos_fr['category_id']) # french(fr) + germany(de)
used_category_entire = list(np.union1d(used_category_2, used_category_3))

used_category_by_nation = pd.DataFrame([], index = used_category_entire, columns=['US','CA','GB','FR','DE'])
used_category_by_nation.index.name='category_ID'
for idx in used_category_by_nation.index:
    if idx in videos_us['category_id']:
        used_category_by_nation['US'][idx] = 1
    else:
        used_category_by_nation['US'][idx] = 0
    if idx in videos_ca['category_id']:
        used_category_by_nation['CA'][idx] = 1
    else:
        used_category_by_nation['CA'][idx] = 0
    if idx in videos_gb['category_id']:
        used_category_by_nation['GB'][idx] = 1
    else:
        used_category_by_nation['GB'][idx] = 0
    if idx in videos_fr['category_id']:
        used_category_by_nation['FR'][idx] = 1
    else:
        used_category_by_nation['FR'][idx] = 0
    if idx in videos_de['category_id']:
        used_category_by_nation['DE'][idx] = 1
    else:
        used_category_by_nation['DE'][idx] = 0

# json파일 read - category_id, category_title
with open('../youtube-new/US_category_id.json') as f:
    categorys_us = json.load(f)
categorys_data_us = categorys_us['items']
category_datas=pd.DataFrame([], index=used_category_entire, columns={'category_TITLE'})
category_datas.index.name='category_ID'
for item in categorys_data_us:
        if int(item['id']) in category_datas.index:
            category_datas.loc[int(item['id'])][('category_TITLE')] = item['snippet']['title']

# kedoo rank
kedoo_rank = category_datas.copy()
kedoo_rank['English']=[5,12,2,13,8,14,4,3,9,1,11,7,6,10,15,17,16,18]
kedoo_rank['French']=[5,11,1,13,9,14,4,3,6,2,10,7,8,12,15,17,16,18]
kedoo_rank['German']=[5,8,3,14,7,13,2,4,11,1,12,6,9,10,15,17,16,18]

def list_category():
    # return [1, 2, 10, 15, 17, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 43, 44]
    return used_category_entire

def isCategory(nation):
    # nation : 'US', 'CA', 'GB', 'FR', 'DE'
    return used_category_by_nation[nation] # TYPE : series

def info_category():
    return category_datas.copy() # category_ID, category_TITLE

def kedooRank(language):
    # language : 'English', 'French', 'German'
    rank = kedoo_rank[['category_TITLE',language]].copy()
    rank.rename(columns = {'category_TITLE':'kedoo_category'}, inplace = True)
#     rank = rank.set_index(language)
    return rank
