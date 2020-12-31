import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import scale
from .cts import build_training_set
import os
from random import shuffle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
from googlesearch import search 



  

#region not my get_reco() 
# def get_recommendations():
# 	module_dir = os.path.dirname(__file__)

# 	train_df = build_training_set()
# 	if train_df is None:
# 		return []
# 	x_train = train_df.iloc[:, 5:]
# 	try:
# 		x_train = scale(x_train)
# 	except:
# 		print("First migrations")
# 	y_train = train_df.iloc[:, 3]
# 	x_train_labels = train_df.iloc[:, 0]

# 	target_df = pd.read_csv(os.path.join(module_dir,'data.csv'))
# 	target_df = pd.DataFrame(target_df)
# 	target_df = target_df.append(train_df)
# 	target_df = target_df.append(train_df)
# 	target_df = target_df.drop_duplicates('SeriesName', keep=False)

# 	x_target = scale(target_df.iloc[:, 5:])
# 	x_target_labels = target_df.iloc[:, 0]

# 	clf = RandomForestClassifier()
# 	clf.fit(x_train,y_train)

# 	y_target = clf.predict(x_target)

# 	new_df = pd.DataFrame()
# 	new_df['seriesName'] = x_target_labels
# 	new_df['tvdbID'] = target_df.iloc[:, 1]
# 	new_df['PredictedRating'] = y_target
# 	new_df['indicator'] = (target_df.iloc[:, 4]/target_df.iloc[:, 3])*new_df['PredictedRating']

# 	new_df = new_df.sort_values(['indicator'], ascending=False)
# 	initial_list = list(new_df.iloc[:4, 1])
# 	latter_list =  list(new_df.iloc[5:15, 1])
# 	shuffle(latter_list)
# 	return list(initial_list + latter_list[:5])
#endregion
dfc6 = pd.read_csv('tvshow\\utils\dfc6.csv')

cv = CountVectorizer()
count_matrix = cv.fit_transform(dfc6['combine_features'])
cosine_sim = cosine_similarity(count_matrix)

def get_recommendations(imdb_id):
  list_rec=[]
  ind=next(iter(dfc6[dfc6['imdbId']==imdb_id].index), 'no match')
  for i in pd.Series(cosine_sim[ind,:]).sort_values(ascending=False).head(6).index:
    l=dfc6.loc[i]['imdbId']
    list_rec.append(l)
  return list_rec

def find_imdbid_from_title(title):
    # query = title + " imdb"
    # imdbid = []
    # for j in googlesearch.search(query, num=10, stop=1, pause=2): 
    #   imdbid = j
    # imdbid = imdbid[-10:-1]
    # print (imdbid)
    # return imdbid
  # try: 
  #     from googlesearch import search 
  # except ImportError:  
  #     print("No module named 'google' found") 
  
# to search 
  query = title + " imdbd"
  
  for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
      if any(dfc6['imdbId'].str.contains(j[-10:-1])):
        return j[-10:-1]
  return None


  #  return dfc6[dfc6.title == title]['imdbId'].values[0]

def get_info_from_id(key):
  req=requests.get('http://www.omdbapi.com/?i='+key+'&apikey=58bc3b10')
  f = {}
  f = json.loads(req.text)
  f['Genre'] = f['Genre'].split(',')
  return f

def rec_info(title):
  list_info=[]
  IMDBID=find_imdbid_from_title(title)
  if(IMDBID is not None):
    recom=get_recommendations(IMDBID)
    for i in recom:
      info=get_info_from_id(i)

      list_info.append(info)
    return list_info
  return None


