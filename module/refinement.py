import pandas as pd
import numpy as np
import datetime as dt

def retypeDate(videos):
    if type(videos['publish_time'][0]) == str:
        new_publish_time = []
        for item in videos['publish_time']:
            new_publish_time.append(dt.date(int(item[0:4]),int(item[5:7]),int(item[8:10])))
        videos.update(pd.DataFrame({'publish_time': new_publish_time}))
    if type(videos['trending_date'][0]) == str:
        new_trending_date=[]
        for item in videos['trending_date']:
            new_trending_date.append(dt.date(2000 + int(item[0:2]),int(item[6:8]),int(item[3:5])))
        videos.update(pd.DataFrame({'trending_date': new_trending_date}))

def dropRows_disabled(videos, column):
    # column : 비교 및 삭제할 열 이름 문자열
    # dropRows_disabled(videos, 'comments_disabled')
    # dropRows_disabled(videos, 'ratings_disabled')
    # dropRows_disabled(videos, 'video_error_or_removed')
    if column not in videos.columns:
        print(column,'이 존재하지 않음')
    else:
        find = videos[videos[column] == True]
        drop = videos[videos['video_id'].isin(find['video_id'])]
        videos.drop(drop.index, inplace=True)
        videos.reset_index(inplace=True, drop=True)
        del videos[column]
    

def dropColumns(videos, column):
    # column : 'tags', 'description' .etc
    if column in videos.columns:
        del videos[column]
    else:
        print(column,'이 존재하지 않음')

def dropRows_dates(videos, column, start, end):
    # column : publish_time
    # start, end : datetime.date(yyyy, mm, dd)
    if type(videos[column][0]) == dt.date:
        old = videos[videos[column]<start]
        young = videos[videos[column]>end]
        videos.drop(old.index, inplace=True)
        videos.drop(young.index, inplace=True)
        videos.reset_index(inplace=True, drop=True)
    else:
        print('videos[',column,']이 datetime.date 형식이 아님')
