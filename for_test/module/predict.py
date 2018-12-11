import pandas as pd
import numpy as np
import datetime as dt
import math
from tqdm import tqdm_notebook

def init_unique(videos):
    # unique : 영상별 정보 저장
    unique = pd.DataFrame(np.unique(videos['video_id']), columns=['video_id'])
    
    category_id = []
    total_views=[]             # 누적 조회수
    trending_duration = []     # trending list에 등록된 기간
    publish_time = []          # upload 날짜
    first_trending_date = []   # 처음으로 trending list에 등록된 날짜
    last_trending_date = []    # 마지막으로 trending list에 등록된 날짜
    thumbnail_link = []        # 섬네일 이미지 주소
    video_title = []           # 영상 제목
    channel_title=[]           # 채널 이름
    
    for i in tqdm_notebook(unique.index):
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
    
    unique['video_title']=video_title
    unique['category_id'] = category_id
    unique['trending_duration'] = trending_duration
    unique['publish_time'] = publish_time
    unique['first_trending_date'] = first_trending_date
    unique['last_trending_date'] = last_trending_date
    unique['total_views'] = total_views
    
    # days : 조회수가 기록된 기간(publish_time ~ last_trending_date)
    unique['days'] = unique['last_trending_date'] - unique['publish_time'] + dt.timedelta(1)
    unique['thumbnail_link'] = thumbnail_link
    unique['channel_title']=channel_title
    
    return unique

def init_stat(unique, category_id):
    # stat : category_id 별 통계치 저장
    stat = pd.DataFrame([], index = category_id)
    sum_total_views=[]            # 영상별 누적 조회수의 합
    mean_total_views=[]           # 영상별 누적 조회수의 평균
    number_of_unique_videos=[]    # 영상 갯수
    sum_trending_duration=[]      # trending list에 등록된 기간의 합
    mean_trending_duration=[]     # trending list에 등록된 기간의 평균
    for i in tqdm_notebook(stat.index):
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
    
    method_list=list(stat.columns)
    for method in method_list:
        for i in stat.index:
            if math.isnan(stat[method][i]): # NaN
                stat[method][i]=0
    return stat

def score(result, stat, method, weight):
    result['rank']=0
    result['score'] = 0
    max_score = []
    if len(weight)==0:
        max_score=[100/len(method)]*len(method)
    else:
        unit_weight = 100/sum(weight)
        max_score = np.array(weight)*unit_weight
    for i in range(len(method)):
        result[method[i]] = stat[method[i]]
        max_stat = max(result[method[i]])
        result['score_'+method[i]+'(max='+str(max_score[i])+')']=(result[method[i]]/max_stat)*max_score[i]
        result['score']+=result['score_'+method[i]+'(max='+str(max_score[i])+')']
    for i in result.index:
        if math.isnan(result['score'][i]):
            result['score'][i] = 0
    result['rank'] = (result['score'].rank(ascending=False)).astype(int)

# def showVideos(unique, category_id):
#     print(category_id)
#     videos_by_category_id = unique[unique['category_id']==category_id].copy()
#     for i in videos_by_category_id.index:
        
    
        