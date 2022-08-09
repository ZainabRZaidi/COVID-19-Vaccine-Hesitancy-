import csv
import pandas as pd
import numpy as np
import ast 

# This script classifies tweets of each class (keyword) into subtopics (classes and keywords)

num1 = 1
#input('Enter the number of the first file: ')
num2 = 370
#input('Enter the number of the last file: ')
keyword = 'FAVOR'
#input('Enter keyword (FAVOR or AGAINST): ')

# the output file
file_class = 'classes_'+keyword+'.csv'

df_keywords = pd.read_csv('keywords_classes.csv',lineterminator='\n',index_col=None).drop(['Unnamed: 0'],axis=1)
df_class = df_keywords
print(df_class)
df_class['keywords'] = [ast.literal_eval(item) for item in df_class['keywords']]
#df_class['keywords'].apply(lambda x:  ",".join(x))
df_class.loc[len(df_class),'class']='Misc/Missclassified'
print(df_class)
if keyword == 'FAVOR':
	topic_end = 43
	topic_start = 0
else:
	topic_end = 53
	print(keyword)
	#len(df_keywords)
	topic_start = 22
keywords = set(df_keywords.keywords.loc[topic_start])
print(keywords)
for k in range(topic_start+1,topic_end):
	keywords = keywords.union(set(df_keywords.keywords.loc[k]))
	print(keywords)
df_class.loc[len(df_class)-1,'keywords'] = keywords


for x in range(int(num1),int(num2)+1):
	if x < 10 :
		y = '00'+str(x)
	elif x < 100 :
		y = '0'+str(x)
	else :
		y = str(x)
	input_file = 'anti-vax_'+y+'.csv'
	df = pd.read_csv(input_file,lineterminator='\n')
	df = df.rename(columns={'text':'Tweet'})
	# first drop the duplicate tweets
	df.drop_duplicates(subset ="tweet_id",keep = 'first', inplace = True)
	#print(len(df.index))
	# filter the tweets according to the keyword
	df = df[df['Stance'].str.contains(keyword, na=False)]
	df = df['Tweet'].value_counts().rename_axis('Tweets').reset_index(name='counts')
	# Classification
	df_class[y] = 0
	for i in range(0,len(df_keywords.index)):
		keywords = df_keywords.loc[i,'keywords']
		if df_class.loc[i,'class'] == 'WHO':
			df_new = df[df['Tweets'].str.contains('|'.join(keywords),case=True)]
		else:
			df_new = df[df['Tweets'].str.contains('|'.join(keywords),case=False)]
		df_class.loc[i,y]=df_new['counts'].sum()
	print(df_class)
	#Left overs
	keywords = df_class.loc[len(df_class)-1,'keywords']
	df_new = df[~df['Tweets'].str.contains('|'.join(keywords),case=False)]
	df_class.loc[len(df_class)-1,y] = df_new['counts'].sum()
	df_class[y] = df_class[y].div(df['counts'].sum())
	df_class.to_csv(file_class)

df_class = df_class.drop(columns=['keywords'])

df_class.to_csv(file_class)
