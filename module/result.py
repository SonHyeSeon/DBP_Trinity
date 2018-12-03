import pandas as pd
import numpy as np
import seaborn as sns
cm = sns.light_palette("green", as_cmap=True)
n=18

reliability_table_1 = pd.DataFrame([], index=np.array(range(1,n+1)))
for i in range (1,n+1):
    reliability_table_1[i] = 100-(abs(reliability_table_1.index-i)/(n-1))*100
style_reliability_table_1 = reliability_table_1.style.background_gradient(cmap=cm)
style_reliability_table_1

reliability_table_2 = pd.DataFrame([], index=np.array(range(1,n+1)))
for i in range (1,n+1):
    if n-i > i-1:
        max_val = n-i
    else:
        max_val = i-1
    reliability_table_2[i] = 100-(abs(reliability_table_2.index-i)/max_val)*100
style_reliability_table_2 = reliability_table_2.style.background_gradient(cmap=cm)
style_reliability_table_2

reliability_table_3 = pd.DataFrame(np.eye(n)*100, index=np.array(range(1,n+1)), columns=np.array(range(1, n+1)))
style_reliability_table_3 = reliability_table_3.style.background_gradient(cmap=cm)
style_reliability_table_3

def reliability_1(kedoo, result):
    reliability = []
    if len(kedoo) == len(result):
        for i in range(len(kedoo)):
            reliability.append(reliability_table_1[kedoo[i]][result[i]])
        return reliability
    else:
        print('kedoo와 result의 길이 다름')   
        
def reliability_2(kedoo, result):
    reliability = []
    if len(kedoo) == len(result):
        for i in range(len(kedoo)):
            reliability.append(reliability_table_2[kedoo[i]][result[i]])
        return reliability
    else:
        print('kedoo와 result의 길이 다름')
        
def reliability_3(kedoo, result):
    reliability = []
    if len(kedoo) == len(result):
        for i in range(len(kedoo)):
            reliability.append(reliability_table_3[kedoo[i]][result[i]])
        return reliability
    else:
        print('kedoo와 result의 길이 다름')
        
def calc(result_data, column, kedoo_rank, method):
    if method==1:
        result_data['reliability'] = reliability_1(kedoo_rank,result_data[column].values)
    elif method==2:
        result_data['reliability'] = reliability_2(kedoo_rank,result_data[column].values)
    elif method==3:
        result_data['reliability'] = reliability_3(kedoo_rank,result_data[column].values)

def resultType(result_data, rank, title, score, reliability):
    result_data = result_data.sort_values(by=rank)
    result_data[reliability] = round(result_data[reliability], 2)
    result_data.rename(columns = {rank:'Rank'}, inplace = True)
    result_data.rename(columns = {title:'Category'}, inplace = True)
    result_data.rename(columns = {score:'Score'}, inplace = True)
    result_data.rename(columns = {reliability:'Reliability(%)'}, inplace = True)
    result_data = result_data.set_index('Rank')
    return result_data
