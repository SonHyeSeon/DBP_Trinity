import pandas as pd
import numpy as np

n=18
reliability_table_1 = pd.DataFrame([], index=np.array(range(1,n+1)))
for i in range (1,n+1):
    reliability_table_1[i] = 100-(abs(reliability_table_1.index-i)/(n-1))*100
    
reliability_table_2 = pd.DataFrame([], index=np.array(range(1,n+1)))
for i in range (1,n+1):
    if n-i > i-1:
        max_val = n-i
    else:
        max_val = i-1
    reliability_table_2[i] = 100-(abs(reliability_table_2.index-i)/max_val)*100
    
reliability_table_3 = pd.DataFrame(np.eye(n)*100, index=np.array(range(1,n+1)), columns=np.array(range(1, n+1)))

def reliability_1(result_data, column, kedoo_data, result_language):
    if (result_data.index == kedoo_data.index).all():
        reliability_1 = []
        for i in result_data.index:
            reliability_1.append(reliability_table_1[kedoo_data[result_language][i]][result_data[column][i]])
        result_data['reliability_1'] = reliability_1
    else:
        print("category_ID로 정렬필요")
    
def reliability_2(result_data, column, kedoo_data,  result_language):
    if (result_data.index == kedoo_data.index).all():
        reliability_2 = []
        for i in result_data.index:
            reliability_2.append(reliability_table_2[kedoo_data[result_language][i]][result_data[column][i]])
        result_data['reliability_2'] = reliability_2
    else:
        print("category_ID로 정렬필요")
    
def reliability_3(result_data, column,  kedoo_data, result_language):
    if (result_data.index == kedoo_data.index).all():
        reliability_3 = []
        for i in result_data.index:
            reliability_3.append(reliability_table_3[kedoo_data[result_language][i]][result_data[column][i]])
        result_data['reliability_3'] = reliability_3
    else:
        print("category_ID로 정렬필요")
    
def calc(result_data, column, kedoo_data, result_language, reliability):
    if reliability==1:
        reliability_1(result_data, column, kedoo_data, result_language)
    elif reliability==2:
        reliability_2(result_data, column, kedoo_data, result_language)
    elif reliability==3:
        reliability_3(result_data, column, kedoo_data, result_language)

def resultType(result_data, rank, title, score, reliability):
    result_data = result_data.sort_values(by=rank)
    result_data[reliability] = round(result_data[reliability], 2)
    result_data.rename(columns = {rank:'Rank'}, inplace = True)
    result_data.rename(columns = {title:'Category'}, inplace = True)
    result_data.rename(columns = {score:'Score'}, inplace = True)
    result_data.rename(columns = {reliability:'Reliability(%)'}, inplace = True)
    result_data = result_data.set_index('Rank')
    return result_data    
