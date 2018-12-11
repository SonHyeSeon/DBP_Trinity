import pandas as pd
import numpy as np
import datetime as dt

import category
import refinement
import result
import predict

def category_rank():
    print('select Nation [US/CA/GB/FR/DE] :', end=' ')
    nation=input()
    if nation in ['US','CA','GB']:
        language='English'
    elif nation=='FR':
        language='French'
    elif nation=='DE':
        language='German'
    else:
        print('잘못된 입력입니다.')
        return;
    print('Language :',language,'\n')
    videos = pd.read_csv('../youtube-new/'+nation+'videos.csv')
    kedoo_rank = category.kedooRank(language)
    
    # refine dataset - essential
    print('refine datas')
    refinement.retypeDate(videos)
    refinement.dropRows_duplicated(videos)
    
    # refine dataset - optional
    print('drop comments_disabled=True?[y/n] :', end=' ')
    if input()=='y':
        refinement.dropRows_disabled(videos, 'comments_disabled')
    print('drop ratings_disabled=True?[y/n] :', end=' ')
    if input()=='y':
        refinement.dropRows_disabled(videos, 'ratings_disabled')
    print('drop video_error_or_removed=True?[y/n] :', end=' ')
    if input()=='y':
        refinement.dropRows_disabled(videos, 'video_error_or_removed')
        
    print('drop by publish_time?[y/n] :', end=' ')
    if input()=='y':
        print('input publish_time duration')
        print('\tstart date[yyyymmdd] :',end=' ')
        publish_time_start = pd.to_datetime(input(), format='%Y%m%d', errors='ignore').date()
        print('\tend date[yyyymmdd] :',end=' ')
        publish_time_end = pd.to_datetime(input(), format='%Y%m%d', errors='ignore').date()
        refinement.dropRows_dates(videos, 'publish_time', publish_time_start, publish_time_end)
    
    print('drop by trending_date?[y/n] :', end=' ')
    if input()=='y':
        print('input trending_date duration')
        print('\tstart date[yyyymmdd] :',end=' ')
        trending_date_start = pd.to_datetime(input(), format='%Y%m%d', errors='ignore').date()
        print('\tend date[yyyymmdd] :',end=' ')
        trending_date_end = pd.to_datetime(input(), format='%Y%m%d', errors='ignore').date()
        refinement.dropRows_dates(videos, 'trending_date', trending_date_start, trending_date_end)
    
    print()
    
    # predict
    
    print('init unique_videos')
    unique_videos = predict.init_unique(videos)
    print('init stat_category')
    stat_category = predict.init_stat(unique_videos, category.list_category())
    
    print('select method')
    method_list = list(stat_category.columns)
    selected_method=[]
    selected_weight=[]
    for i in range(len(method_list)):
        print('\tselect method '+(method_list[i])+'?[y/n] :',end=' ')
        if input()=='y':
            selected_method.append(method_list[i])
            print('\t\tinput method '+(method_list[i])+' weight(default=1, weight>0) :',end=' ')
            w = input()
            if w.isdigit():
                selected_weight.append(int(w))
            else:
                selected_weight.append(1) 
    print('selected method and weight is')
    for i in range(len(selected_method)):
        print('\t',selected_method[i],'\t',selected_weight[i])
        
    result_data = category.info_category()
    predict.score(result_data,stat_category, selected_method, selected_weight)

    print()

    #result
    print('select reliability_method[1/2/3, default=1] :', end=' ')
    r = input()
    if (r=='1') or (r=='2') or (r=='3'):
        result.calc(result_data, 'rank', kedoo_rank[language].values, int(r))
    else:
        result.calc(result_data, 'rank', kedoo_rank[language].values, 1)
    
    final_result = result.resultType(result_data, 'rank', 'category_TITLE', 'score', 'reliability')
    return final_result