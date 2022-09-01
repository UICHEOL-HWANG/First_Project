import numpy as np
import pandas as pd 

import statistics
import plotly.offline as py 
import plotly.figure_factory as ff
import plotly.express as px
import matplotlib.pyplot as plt # 라이브러리들 호출 

data = pd.read_csv("C:\\Users\\UICHEOL_HWANG\\new_project\\books_1.Best_Books_Ever.csv",usecols=['title', 'series', 'author', 'rating', 'language', 'genres', 'characters', 'pages', 'publishDate', 'awards', 'numRatings', 'likedPercent', 'price'])
data.head(5) #데이터 프레임 추출 

data.info() #데이터 프레임안 컬럼들의 속성 추출 

#데이터 전처리 과정.

# 수치형으로 다뤄야 할 데이터인 pages, price의 datatype을 바꿔준다

# convert datatypes 
# https://stackoverflow.com/questions/15891038/change-column-type-in-pandas
data['price'] = pd.to_numeric(data['price'], errors='coerce')
data['pages'] = pd.to_numeric(data['pages'], errors='coerce')

#결측치 확인 

'''Missing Value Chart'''
data.isnull().mean(axis=0).plot.barh()
plt.title("Ratio of missing values per columns")

data.drop(data[data['price'].isnull()].index, inplace=True)
data.drop(data[data['pages'].isnull()].index, inplace=True)
data.reset_index(drop=True, inplace=True) # reindex
#결측치가 있는 값들을 제거함 

# 시리즈물인지 여부 'is_series'
data['is_series'] = 1
data['is_series'].loc[data['series'].isnull()] = 0

# 캐릭터 수 'num_characters'
data['num_characters'] = 0
for i in range(len(data)):
    if data['characters'][i] == '[]':
        continue
    else:
        data['num_characters'][i] = len(data['characters'][i].split(','))

# 받은 상의 개수 'num_awards'
data['num_awards'] = 0
for i in range(len(data)):
    if data['awards'][i] == '[]':
        continue
    else:
        data['num_awards'][i] = len(data['awards'][i].split(','))

# 장르별 빈도 카운팅
genre_dict = {}
for i in range(len(data)):
    if data['genres'][i] == '[]':
        continue
    lst = data['genres'][i][2:-2].split("', '")
    for s in lst:
        genre_dict[s] = genre_dict.get(s, 0) + 1

# 상위 15개 장르만 선정, 나머지는 etc로 분류
import operator
genre_lst = sorted(genre_dict.items(), key=operator.itemgetter(1), reverse=True)[:15]

#선정된 상위 15개의 장르
genre_lst

# 주요 장르로 재배치, 해당되는 장르가 없으면 etc
data['main_genre'] = 'etc'
for i in range(len(data)):
    for g, num in genre_lst:
        if g in data['genres'][i]:
            data['main_genre'][i] = g
            break

#최종 데이터셋 확인 
del data['series']
del data['genres']
del data['characters']
del data['awards']

data.head(5)


data.describe #기초 통계분석 

fig = px.imshow(data.corr(), template='plotly_dark', title='Heatmap')
fig.show()

# 시리즈물인 책과 그렇지 않은 책의 평점 분포가 다른지 알고 싶어서 두 그룹의 평점 분포를 그려보았다.
# plotly.figure_factory를 이용해 distplot을 그렸다.

# 시리즈물과 단편의 평점 분포

# group data
hist_data = [data[data['is_series'] == 1]['rating'], data[data['is_series'] == 0]['rating']]
group_labels = ['is_series', 'not_series']
colors = ['#2BCDC1', '#F66095']

# create distplot
fig = ff.create_distplot(hist_data, group_labels, bin_size=.2, colors=colors)
fig.update_layout(title_text='Rating Distribution', template='plotly_dark')
fig.show()

# 장르별 평점 분포를 비교하기 위해 boxplot을 여러개 그려보았다.
px.box(data, x="main_genre", y="rating", color='main_genre')
# 장르별 평점 분포 

fig = px.box(data, x="main_genre", y="rating", color='main_genre', template='plotly_dark')
fig['layout'].update(title='Rating Distributions by Genre')
fig.show()

# 책이 너무 두꺼우면 사람들이 많이 읽지 못했을 것 같다는 생각에 likedPercent와 pages의 관련성을 시각화 해보았다.
# density heatmap은 처음 그려보는데 꽤나 직관적인듯 하다.
# x와 y의 범위를 적절히 조절해 그렸고, 히트맵 바깥에 히스토그램도 추가할 수 있다.
fig = px.density_heatmap(data, x="pages", y="likedPercent", marginal_x="histogram", marginal_y="histogram", range_x=[0, 500], range_y=[80, 100], template='plotly_dark')
fig['layout'].update(title='Density Heatmap of LikedPercent vs Pages')
fig.show()

#마지막으로, best books에 이름을 올린 책들이 어떤 장르들을 가지고 있는지, 
#비율을 파악하고 싶어서 pie chart를 그려보았다.

# 장르의 비율

# count values by main_genre
df2 = pd.DataFrame(data['main_genre'].value_counts()).reset_index()
df2.columns = ['main_genre', 'counts']

labels = df2['main_genre'].tolist()
values = df2['counts'].tolist()

fig = px.pie(df2, values=values, names=labels, template='plotly_dark')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
fig['layout'].update(title='Genre Ratio', boxmode='group')
fig.show()