import numpy as np
import pandas as pd 

import statistics
import plotly.offline as py 
import plotly.figure_factory as py 
import plotly.express as px
import matplotlib.pyplot as plt # 라이브러리들 호출 

data = pd.read_csv("C:\\Users\\UICHEOL_HWANG\\new_project\\books_1.Best_Books_Ever.csv",usecols=['title', 'series', 'author', 'rating', 'language', 'genres', 'characters', 'pages', 'publishDate', 'awards', 'numRatings', 'likedPercent', 'price'])
data.head(5) #데이터 프레임 추출 