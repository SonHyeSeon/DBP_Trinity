import pandas as pd
import numpy as np
import datetime as dt

def init_unique(videos):
    unique = pd.DataFrame(np.unique(videos['video_id']), columns=['video_id'])
    category_id = []
    total_views=[]
    trending_duration = []
    publish_time = []
    first_trending_date = []
    last_trending_date = []
    thumbnail_link = []
    video_title = []
    channel_title=[]
    for i in unique.index:
        videos_by_video_id = videos[videos['video_id']==unique['video_id'][i]]
        category_id.append(videos_by_video_id['category_id'].values[0])
        total_views.append(max(videos_by_video_id['views']))
        trending_duration.append(len(videos_by_video_id))
        publish_time.append((videos_by_video_id['publish_time'].values[0]))
        first_trending_date.append(min(videos_by_video_id['trending_date']))
        last_trending_date.append(max(videos_by_video_id['trending_date']))
        thumbnail_link.append(videos_by_video_id['thumbnail_link'].values[0])
        video_title.append(videos_by_video_id['title'].values[0])
        channel_title.append(videos_by_video_id['channel_title'].values[0])
    unique['thumbnail_link'] = thumbnail_link
    unique['video_title']=video_title
    unique['category_id'] = category_id
    unique['trending_duration'] = trending_duration
    unique['publish_time'] = publish_time
    unique['first_trending_date'] = first_trending_date
    unique['last_trending_date'] = last_trending_date
    unique['total_views'] = total_views
    unique['days'] = unique['last_trending_date'] - unique['publish_time'] + dt.timedelta(1)
    unique['channel_title']=channel_title
    
    return unique

def init_stat(unique, category_id):
    stat = pd.DataFrame([], index = category_id)
    sum_total_views=[]
    mean_total_views=[]
    number_of_unique_videos=[]
    sum_trending_duration=[]
    mean_trending_duration=[]
    for i in stat.index:
        videos_by_category_id = unique[unique['category_id']==i]
        sum_total_views.append(sum(videos_by_category_id['total_views']))
        mean_total_views.append(np.mean(videos_by_category_id['total_views']))
        number_of_unique_videos.append(len(videos_by_category_id))
        sum_trending_duration.append(sum(videos_by_category_id['trending_duration']))
        mean_trending_duration.append(np.mean(videos_by_category_id['trending_duration']))
    stat['sum_total_views']=sum_total_views
    stat['mean_total_views']=mean_total_views
    stat['number_of_unique_videos']=number_of_unique_videos
    stat['sum_trending_duration']=sum_trending_duration
    stat['mean_trending_duration']=mean_trending_duration
    return stat

def score(result, stat, method):
    result[method] = stat[method]
    result['rank'] = (result[method].rank(ascending=False)).astype(int)

# def showVideos(unique, category_id):
#     print(category_id)
#     videos_by_category_id = unique[unique['category_id']==category_id].copy()
#     for i in videos_by_category_id.index:
        
    
        