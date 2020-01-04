
# coding: utf-8

# # Projet Text Mining

# ## Apport de données

# 
# les données quand a importé sont separés par des tabulation

# In[1]:

import pandas as pd 

# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
data = pd.read_csv("/home/toutou/nyt.csv/nyt.csv",sep='\t') 
# Preview the first 5 lines of the loaded data 
data.head()


# In[333]:

data.describe


# In[13]:

data.texts[0]


# ## Exploration des differentes possiblités pour exploiter la librairy Spacy pour extraire les entités (Descripteur de Personnes des Lieux et des Evenements)

# On commence par appliquer les differents traitements sur un seul fichier

# In[2]:

import spacy
from collections import Counter
#from collections import Counter
#import en_core_web_sm
nlp = spacy.load('en')
article = nlp(data.texts[0])
#article = nlp(ny_bb)
#print(doc.text)
for token in article:
    print(token.text, token.pos_, token.dep_,token.ent_type_,token.tag_)



# In[15]:

(article.ents)


# In[3]:

labels = [x.label_ for x in article.ents]
Counter(labels)


# In[12]:

from spacy import displacy
sentences = [x for x in article.sents]
#sentences
displacy.render(nlp(str(sentences[1])), jupyter=True, style='dep')


# In[8]:

displacy.render(nlp(str(sentences)), jupyter=True, style='ent')


# ## Detection Des Entités; les lieux "GPE", les personnes "PERSON" et les evenements "EVENT" sur un seul document

# In[20]:


import numpy as np
places = [x for x in article.ents if x.label_=='GPE']
people = [x for x in article.ents if x.label_=='PERSON']
events= [x for x in article.ents if x.label_=='EVENT']
#list_loc = [token.i for token in article if token.ent_type_=='GPE' ]

used = []
for x in sorted(people):
    if str(x) not in used:
        used.append(str(x))
        
        
people=used
###################
used = []
for x in sorted(places):
    if str(x) not in used:
        used.append(str(x))
        
        
places=used
###################
used = []
for x in sorted(events):
    if str(x) not in used:
        used.append(str(x))
        
        
events=used

people,events,places


# Now we redo the same process for every article then create a colomn for every meta data we're aiming to add places, events and people 

# In[21]:

len(data)


# ## Elimination des entités dupliquées ou similaires

# In[22]:

p=[ 'Mai Chi Tho','Chi Mai Tho','Mai DO Tho','Mai Tho','Tho',"Hing Mai Do tho","Sara T","T Sara"]
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(ngram_range=(1, 2))
vectorizer.fit(p)
X_bag_of_words = vectorizer.transform(p)
X_bag_of_words.shape
vectorizer.get_feature_names()
D = X_bag_of_words.toarray()

import math

# fonction calculant le cosinus entre deux vecteurs
def cosinus(i, j):
    num = np.dot(i, j)
    den = math.sqrt(sum(i*i))*math.sqrt(sum(j*j))
    if (den>0):    
        return (num/den)
    else:
        return 0

ones_array = np.ones( (len(D), len(D)), dtype=np.float64 ) 
    
for i in range(len(D)):
    for j in range(len(D)):
        ones_array[i][j]=(cosinus(D[i, :], D[j, :]))
        
print(ones_array)
indexes=np.where(ones_array >0.4)
print(indexes)
repeated=[]
for i,j in zip(indexes[0],indexes[1]) :
    if (i!=j and len(p[i])>len(p[j])):
        repeated.append(p[j])
        #print(repeated)
        #p.pop(i)
        #print("+",p[i],"+",p[j],ones_array[i][j],"+++++",len(p[i]),"++",i,"++++++++",len(p[j]),"++",j)
        print("+",p[i],"+",p[j],"++similarité++ :",ones_array[i][j])

print("liste initiale",p)
print("element à eliminer",repeated)


# les entités tel "Mai Chi Tho" et  "Chi Mai Tho" et "Mai Tho" represente la même chose d'où la chaine la plus grande est celle à garder 
# 
# Les entités tel "Chi Mai Tho" et "Mai DO Tho" ayant une similarité de 0.3999999999999999  
# ne represente pas la même personne du coup on les garde les deux ce qui explique pour qoi on a prit le seuil de 0.4
# 

# In[297]:

# proccessing still in progress
new_people=[x for x in sorted(p) if x not in repeated]
print("nouvelle liste",new_people)
final_entity=[]
used=[]
used2=[]

for i in (range(len(new_people))):
    for j in (range(len(new_people))):
        #print("++++++++",i,"+",j)

        if i!=j and (sorted((new_people[i]).split(" "))==sorted((new_people[j]).split(" "))) and i not in used:
            print(new_people[i],"+",(new_people[j]),"les memes!")
            #new_people.remove(new_people[i])
            used.append(i)
            used.append(j)
            final_entity.append(new_people[i])  
            #print(final_entity,"en progres")
for i in (range(len(new_people))):             
    if i not in used:
        #print(new_people[i])
        final_entity.append(new_people[i])
        #print(final_entity,"en progres")
print("Liste de Personnes finale",final_entity)


# ## Traitement des Articles: (sprint 1)

# On a choisit de traiter que les 1000 documents premiers represantant l'année 1987

# In[210]:

import en_core_web_sm
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import math

    # fonction calculant le cosinus entre deux vecteurs
def cosinus(i, j):
    num = np.dot(i, j)
    den = math.sqrt(sum(i*i))*math.sqrt(sum(j*j))
    if (den>0):    
        return (num/den)
    else:
        return 0
    
nlp = spacy.load('en')
all_people=[0 for i in range(1000)]
all_places=[0 for i in range(1000)]
all_events=[0 for i in range(1000)]

for k in range(1000):
    txt_propre = data.texts[k]
    for c in clean_unicode:
        txt_propre = re.sub(c, clean_unicode[c], txt_propre)

#    print(txt_propre)
    article = nlp(txt_propre)
    
    #article = nlp(data.texts[k])
    places = [x for x in article.ents if x.label_=='GPE']
    people = [x for x in article.ents if x.label_=='PERSON']
    events= [x for x in article.ents if x.label_=='EVENT']
    print("++++++events ",k," ",events)
    print("++++++places ",k," ",places)

    #list_loc = [token.i for token in article if token.ent_type_=='GPE' ]
    ########### enlever les elements dupliqués
    if len(people)>0:
        used = []
        for x in sorted(people):
            if str(x) not in used:
                used.append(str(x))


    people=used
    ###################
    if len(places)>0:
        used1 = []
        for x in sorted(places):
            if str(x) not in used1:
                used1.append(str(x))


    places=used1
    ###################
    print(events)

    if len(events)>0:  
        used2 = []
        for x in sorted(events):
            if str(x) not in used2:
                used2.append(str(x))

    events=used2
    print(events)

   
    ###############################people preprocessing in progress reducing names based on similarity of words 
    if len(people)>0:
        p=people
      #print("article ",k,"+","people avant traitement",p)
        vectorizer = CountVectorizer(ngram_range=(1, 2))
        vectorizer.fit(p)
        X_bag_of_words = vectorizer.transform(p)
        X_bag_of_words.shape
        vectorizer.get_feature_names()
        D = X_bag_of_words.toarray()

        ones_array = np.ones( (len(D), len(D)), dtype=np.float64 ) 

        for i in range(len(D)):
            for j in range(len(D)):
                ones_array[i][j]=(cosinus(D[i, :], D[j, :]))

        #print(ones_array)
        indexes=np.where(ones_array >0.4)
        #print("indexes",indexes)
        repeated=[]
        for i,j in zip(indexes[0],indexes[1]) :
            if (i!=j and len(p[i])>len(p[j])):
                repeated.append(p[j])    
    #    indexes=np.where(ones_array >0.4)
    #    print("indexes",indexes)
    #    used=[]
    #    repeated=[]
    #    for i,j in zip(indexes[0],indexes[1]) :
    #        if (i!=j and len(p[i])>len(p[j])):
    #            repeated.append(p[j])
                #print(repeated)            #print(used)
                #p.pop(i)
                #print(p[i],p[j])

    #    new_people=[x for x in sorted(p) if x not in repeated]
        new_people=[x for x in sorted(p) if x not in repeated]
 #       print("nouvelle liste",new_people)
        final_entity=[]
        used=[]
        used2=[]

        for i in (range(len(new_people))):
            for j in (range(len(new_people))):
    #            print("++++++++",i,"+",j)

                if i!=j and (sorted((new_people[i]).split(" "))==sorted((new_people[j]).split(" "))) and i not in used:
     #               print(new_people[i],"+",(new_people[j]),"les memes!")
                    #new_people.remove(new_people[i])
                    used.append(i)
                    used.append(j)
                    final_entity.append(new_people[i])  
    #                print(final_entity,"en progres")
        for i in (range(len(new_people))):             
            if i not in used:
    #            print(new_people[i])
                final_entity.append(new_people[i])
    #            print(final_entity,"en progres")
        final_entity_people=final_entity
        all_people[k]=final_entity_people # if len(final_entity_people)>0 else 0)

  #      print("Liste de Personnes finale",final_entity_people)
    #    print("people apres traitement",new_people)
    ########################event's
    ###############################event's preprocessing in progress reducing names based on similarity of words 
    if len(events)>1:
        p=events
        #print("article ",k,"+","people avant traitement",p)
        vectorizer = CountVectorizer(ngram_range=(1, 2))
        vectorizer.fit(p)
        X_bag_of_words = vectorizer.transform(p)
        X_bag_of_words.shape
        vectorizer.get_feature_names()
        D = X_bag_of_words.toarray()

        ones_array = np.ones( (len(D), len(D)), dtype=np.float64 ) 

        for i in range(len(D)):
            for j in range(len(D)):
                ones_array[i][j]=(cosinus(D[i, :], D[j, :]))

        #print(ones_array)
        indexes=np.where(ones_array >0.4)
        #print("indexes",indexes)
        repeated=[]
        for i,j in zip(indexes[0],indexes[1]) :
            if (i!=j and len(p[i])>len(p[j])):
                repeated.append(p[j])    
    #    indexes=np.where(ones_array >0.4)
    #    print("indexes",indexes)
    #    used=[]
    #    repeated=[]
    #    for i,j in zip(indexes[0],indexes[1]) :
    #        if (i!=j and len(p[i])>len(p[j])):
    #            repeated.append(p[j])
                #print(repeated)            #print(used)
                #p.pop(i)
                #print(p[i],p[j])

    #    new_people=[x for x in sorted(p) if x not in repeated]
        new_people=[x for x in sorted(p) if x not in repeated]
  #      print("nouvelle liste",new_people)
        final_entity=[]
        used=[]
        used2=[]

        for i in (range(len(new_people))):
            for j in (range(len(new_people))):
    #            print("++++++++",i,"+",j)

                if i!=j and (sorted((new_people[i]).split(" "))==sorted((new_people[j]).split(" "))) and i not in used:
                    #print(new_people[i],"+",(new_people[j]),"les memes!")
                    #new_people.remove(new_people[i])
                    used.append(i)
                    used.append(j)
                    final_entity.append(new_people[i])  
    #                print(final_entity,"en progres")
        for i in (range(len(new_people))):             
            if i not in used:
    #            print(new_people[i])
                final_entity.append(new_people[i])
    #            print(final_entity,"en progres")
        final_entity_events=final_entity
        all_events[k]=final_entity_events# if len(final_entity_events)>0 else 0)
        
        
 #       print("Liste de events finale",final_entity_events)
    ###############################
    ###############################places preprocessing in progress reducing names based on similarity of words 
    if len(places)>1:
        p=places
        #print("article ",k,"+","people avant traitement",p)
        vectorizer = CountVectorizer(ngram_range=(1, 2))
        vectorizer.fit(p)
        X_bag_of_words = vectorizer.transform(p)
        X_bag_of_words.shape
        vectorizer.get_feature_names()
        D = X_bag_of_words.toarray()

        ones_array = np.ones( (len(D), len(D)), dtype=np.float64 ) 

        for i in range(len(D)):
            for j in range(len(D)):
                ones_array[i][j]=(cosinus(D[i, :], D[j, :]))

        #print(ones_array)
        indexes=np.where(ones_array >0.4)
        #print("indexes",indexes)
        repeated=[]
        for i,j in zip(indexes[0],indexes[1]) :
            if (i!=j and len(p[i])>len(p[j])):
                repeated.append(p[j])    
    #    indexes=np.where(ones_array >0.4)
    #    print("indexes",indexes)
    #    used=[]
    #    repeated=[]
    #    for i,j in zip(indexes[0],indexes[1]) :
    #        if (i!=j and len(p[i])>len(p[j])):
    #            repeated.append(p[j])
                #print(repeated)            #print(used)
                #p.pop(i)
                #print(p[i],p[j])

    #    new_people=[x for x in sorted(p) if x not in repeated]
        new_people=[x for x in sorted(p) if x not in repeated]
  #      print("nouvelle liste",new_people)
        final_entity=[]
        used=[]
        used2=[]

        for i in (range(len(new_people))):
            for j in (range(len(new_people))):
    #            print("++++++++",i,"+",j)

                if i!=j and (sorted((new_people[i]).split(" "))==sorted((new_people[j]).split(" "))) and i not in used:
                    #print(new_people[i],"+",(new_people[j]),"les memes!")
                    #new_people.remove(new_people[i])
                    used.append(i)
                    used.append(j)
                    final_entity.append(new_people[i])  
    #                print(final_entity,"en progres")
        for i in (range(len(new_people))):             
            if i not in used:
    #            print(new_people[i])
                final_entity.append(new_people[i])
    #            print(final_entity,"en progres")
        final_entity_places=final_entity
        all_places[k]=final_entity_places #if len(final_entity_places)>0 else 0)

  #      print("Liste de lieux finale",final_entity_places)
    #    print("people apres traitement",new_people)    
    ###############################




# In[ ]:




# In[212]:

events_nn=[x for x in all_events if  not(str(x)).isdigit()]
places_nn=[x for x in all_places if  not(str(x)).isdigit()]
people_nn=[x for x in all_people if  not(str(x)).isdigit()]

1000,len(people_nn),len(places_nn),len(events_nn)


#  Parmi 1000 article la reconnaissance des personnes mentionnées est suffisante , par contre il faut travailler 
#         plus sur la reconnaissance des lieux et surtout des evenements c'est pourquoi on va travailler non seulement sur le corps de text du text mais sur toutes les metadatas pour ameliorer les resultats

# ## Des resultats non  satisfesant? Solution : plus de preprocessing 
# on va commencer à traviller sur qlq articles spécifiques pour etre plus pratique

# In[237]:

## Essaie d'extraction
import re 
import dateutil.parser as parser
## l'article 175, ainsi que d'autres articles contient des symboles tel '' ou - qui empeche la detection des entités 
## pour la detection des events la librairie nlp arrive a detecter que qlq evenements , 
#pour ceci on a inclu le titre et la date de l'article 
#pour que si on arrive pas a detecter un evenement pour un article x
#l'event qui lui sera affecter est le titre de l'article + "on" + l'année de l'article
clean_unicode = {
    "'": "",
    "-":" ",
    "\[ | \]":" ",
    ":":" ",
    ",":" ",
    "。" :" ",
    "、":" ",
    "；":" ",
    "（":" ",
    "）":" ",
    "<":" ",
    "《":" ",
    "》":" ",
    "LEAD":"" ,
    "A12:4.":"",
    "U.S.":"United States",
    "US":"United States",
    "U.S. States":"United States",
    "the":"",
    "New Years Day":"New Years Eve"
    
}
## we cleaned our corpus more to get better results removing all ponctuation 
#CORPUS OF THE ARTICLE
txt_propre_2 = data.texts[25]+" "+(data.titles[25]).lower()+" about "+data.principal_classifier[25]+", "+data.second_classifier[25]+" and "+data.third_classifier[25]
for c in clean_unicode:
    txt_propre_2 = re.sub(c, clean_unicode[c], txt_propre_2)
    
#print(txt_propre_2)
article = nlp(txt_propre_2)
places = [x for x in article.ents if x.label_=='GPE']
people = [x for x in article.ents if x.label_=='PERSON']
events= [x for x in article.ents if  x.label_=='DATE']
print("+++",people)
print("+++",events)
print("+++",places )# meme si on fait des pretraitement par fois comme ici y'a des entites qui n'existe pas sur cet articleu
Counter(events)# we observe that for events it's not obvious to take only the date where the article was written 
#because it can refer to an event that happend in the past there for it's better to take 
#he latest year taking from the article as the date of the event and the the date of the article if 
# no event or latest year was found in the article we call event is what's called by x.label_=='Events'
#there for in the next section where we process all the 1000 articles we're going to start by extracting simply 
#the events if the event's or the event weren't found for an article x we're going to fill it value with 
# title of the article followed by "on" followed by the latest year found on the corpus of the article
# for example for the article 1 if we take only the entities labeled as or x.label_=='EVENT' we re not going to find 
#but we can take the article + on the date when it happened this way we're going to have our event
#as for the date we chose is the latest year mentionned in the article, and if no years where mentionned we
#will take the year mentionned in the meta data of the article 

txt_propre_2
# for some documents it is impossible to find where the event happened as for article 25


# In[113]:


##to extract years out of event's
years=[]
for elm in events:
    if (str(elm)).isdigit():
        years.append(int(str(elm)))
    
(sorted(set(years))) ## get the latest year


# In[114]:

#if no dates where found in the corpus of the article we use the date mentionned in the metadatas using
#str(parser.parse(data.dates[k]).year)


# ## Traitement des Articles: (sprint 2)

# In[296]:

import en_core_web_sm
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import math

number_of_articles=1000

    # fonction calculant le cosinus entre deux vecteurs
def cosinus(i, j):
    num = np.dot(i, j)
    den = math.sqrt(sum(i*i))*math.sqrt(sum(j*j))
    if (den>0):    
        return (num/den)
    else:
        return 0
    
nlp = spacy.load('en')
all_people=[0 for i in range(number_of_articles)]
all_places=[0 for i in range(number_of_articles)]
all_events=[0 for i in range(number_of_articles)]

for k in range(number_of_articles):
    txt_propre = data.texts[k]+" "+data.titles[k]+" about "+data.principal_classifier[k]+", "+data.second_classifier[k]+" and "+data.third_classifier[k]
    for c in clean_unicode:
        txt_propre = re.sub(c, clean_unicode[c], txt_propre)

#    print(txt_propre)
    article = nlp(txt_propre)
    
    #article = nlp(data.texts[k])
    places = [x for x in article.ents if x.label_=='GPE']
    people = [x for x in article.ents if x.label_=='PERSON']
    events= [x for x in article.ents if x.label_=='EVENT']
  #  print("++++++places ",k," ",places)
   # print("++++++events ",k," ",events)

    #list_loc = [token.i for token in article if token.ent_type_=='GPE' ]
    ########### People
    if len(people)>1:
        used = []
        for x in sorted(people):
            if str(x) not in used: #enlever les elements dupliqués de people
                used.append(str(x))


        people=used
    #### List of people still in progress reducing names based on similarity of words 
        p=people
      #print("article ",k,"+","people avant traitement",p)
        vectorizer = CountVectorizer(ngram_range=(1, 2))
        vectorizer.fit(p)
        X_bag_of_words = vectorizer.transform(p)
        X_bag_of_words.shape
        vectorizer.get_feature_names()
        D = X_bag_of_words.toarray()

        ones_array = np.ones( (len(D), len(D)), dtype=np.float64 ) 

        for i in range(len(D)):
            for j in range(len(D)):
                ones_array[i][j]=(cosinus(D[i, :], D[j, :]))

        #print(ones_array)
        indexes=np.where(ones_array >0.4)
        #print("indexes",indexes)
        repeated=[]
        for i,j in zip(indexes[0],indexes[1]) :
            if (i!=j and len(p[i])>len(p[j])):
                repeated.append(p[j])    
    #    indexes=np.where(ones_array >0.4)
    #    print("indexes",indexes)
    #    used=[]
    #    repeated=[]
    #    for i,j in zip(indexes[0],indexes[1]) :
    #        if (i!=j and len(p[i])>len(p[j])):
    #            repeated.append(p[j])
                #print(repeated)            #print(used)
                #p.pop(i)
                #print(p[i],p[j])

    #    new_people=[x for x in sorted(p) if x not in repeated]
        new_people=[x for x in sorted(p) if x not in repeated]
 #       print("nouvelle liste",new_people)
        final_entity=[]
        used=[]
        used2=[]

        for i in (range(len(new_people))):
            for j in (range(len(new_people))):
    #            print("++++++++",i,"+",j)

                if i!=j and (sorted((new_people[i]).split(" "))==sorted((new_people[j]).split(" "))) and i not in used:
     #               print(new_people[i],"+",(new_people[j]),"les memes!")
                    #new_people.remove(new_people[i])
                    used.append(i)
                    used.append(j)
                    final_entity.append(new_people[i])  
    #                print(final_entity,"en progres")
        for i in (range(len(new_people))):             
            if i not in used:
    #            print(new_people[i])
                final_entity.append(new_people[i])
    #            print(final_entity,"en progres")
        final_entity_people=final_entity
        all_people[k]=final_entity_people # if len(final_entity_people)>0 else 0)
    else:
        if len(people)==1:
            all_people[k]=people # if len(final_entity_people)>0 else 0)


##################### Places :  
    ###################
    if len(places)>1:
        used1 = []
        for x in sorted(places):
            if str(x) not in used1:
                used1.append(str(x))#enlever les elm dupliqué


        places=used1
        p=places
        #print("article ",k,"+","people avant traitement",p)
        vectorizer = CountVectorizer(ngram_range=(1, 2))     #enlever des lieux se basant sur la similarité
        vectorizer.fit(p)
        X_bag_of_words = vectorizer.transform(p)
        X_bag_of_words.shape
        vectorizer.get_feature_names()
        D = X_bag_of_words.toarray()

        ones_array = np.ones( (len(D), len(D)), dtype=np.float64 ) 

        for i in range(len(D)):
            for j in range(len(D)):
                ones_array[i][j]=(cosinus(D[i, :], D[j, :]))

        #print(ones_array)
        indexes=np.where(ones_array >0.4)
        #print("indexes",indexes)
        repeated=[]
        for i,j in zip(indexes[0],indexes[1]) :
            if (i!=j and len(p[i])>len(p[j])):
                repeated.append(p[j])    
    #    indexes=np.where(ones_array >0.4)
    #    print("indexes",indexes)
    #    used=[]
    #    repeated=[]
    #    for i,j in zip(indexes[0],indexes[1]) :
    #        if (i!=j and len(p[i])>len(p[j])):
    #            repeated.append(p[j])
                #print(repeated)            #print(used)
                #p.pop(i)
                #print(p[i],p[j])

    #    new_people=[x for x in sorted(p) if x not in repeated]
        new_people=[x for x in sorted(p) if x not in repeated]
  #      print("nouvelle liste",new_people)
        final_entity=[]
        used=[]
        used2=[]

        for i in (range(len(new_people))):
            for j in (range(len(new_people))):
    #            print("++++++++",i,"+",j)

                if i!=j and (sorted((new_people[i]).split(" "))==sorted((new_people[j]).split(" "))) and i not in used:
                    #print(new_people[i],"+",(new_people[j]),"les memes!")
                    #new_people.remove(new_people[i])
                    used.append(i)
                    used.append(j)
                    final_entity.append(new_people[i])  
    #                print(final_entity,"en progres")
        for i in (range(len(new_people))):             
            if i not in used:
    #            print(new_people[i])
                final_entity.append(new_people[i])
    #            print(final_entity,"en progres")
        final_entity_places=final_entity
        all_places[k]=final_entity_places #if len(final_entity_places)>0 else 0)
    else:
        if len(places)==1:
            all_places[k]=places #if len(final_entity_places)>0 else 0)
        
        
############## Events:
    ###################

    if len(events)>1:  
        used2 = []
        for x in sorted(events):
            if str(x) not in used2:
                used2.append(str(x))

        events=used2
        p=events
        #print("article ",k,"+","people avant traitement",p)
        vectorizer = CountVectorizer(ngram_range=(1, 2))
        vectorizer.fit(p)
        X_bag_of_words = vectorizer.transform(p)
        X_bag_of_words.shape
        vectorizer.get_feature_names()
        D = X_bag_of_words.toarray()

        ones_array = np.ones( (len(D), len(D)), dtype=np.float64 ) 

        for i in range(len(D)):
            for j in range(len(D)):
                ones_array[i][j]=(cosinus(D[i, :], D[j, :]))

        #print(ones_array)
        indexes=np.where(ones_array >0.4)
        #print("indexes",indexes)
        repeated=[]
        for i,j in zip(indexes[0],indexes[1]) :
            if (i!=j and len(p[i])>len(p[j])):
                repeated.append(p[j])    
    #    indexes=np.where(ones_array >0.4)
    #    print("indexes",indexes)
    #    used=[]
    #    repeated=[]
    #    for i,j in zip(indexes[0],indexes[1]) :
    #        if (i!=j and len(p[i])>len(p[j])):
    #            repeated.append(p[j])
                #print(repeated)            #print(used)
                #p.pop(i)
                #print(p[i],p[j])

    #    new_people=[x for x in sorted(p) if x not in repeated]
        new_people=[x for x in sorted(p) if x not in repeated]
  #      print("nouvelle liste",new_people)
        final_entity=[]
        used=[]
        used2=[]

        for i in (range(len(new_people))):
            for j in (range(len(new_people))):
    #            print("++++++++",i,"+",j)

                if i!=j and (sorted((new_people[i]).split(" "))==sorted((new_people[j]).split(" "))) and i not in used:
                    #print(new_people[i],"+",(new_people[j]),"les memes!")
                    #new_people.remove(new_people[i])
                    used.append(i)
                    used.append(j)
                    final_entity.append(new_people[i])  
    #                print(final_entity,"en progres")
        for i in (range(len(new_people))):             
            if i not in used:
    #            print(new_people[i])
                final_entity.append(new_people[i])
    #            print(final_entity,"en progres")
        final_entity_events=final_entity
        all_events[k]=final_entity_events# if len(final_entity_events)>0 else 0)
        #print(k,"++",type(final_entity_events),final_entity_events)
        
    else:## la liste des evenements soit contient au plus un elm
        if len(events)==1:# un seul elm pas besoin de faire des traitements
            all_events[k]=events# if len(final_entity_events)>0 else 0)
          #  print("++++++events final",k," ",events)
            #print(k,"++",type(events),events)

            
        else:# pas d'events detecter ..Solution? l'event est le titre+ " in " + l'année ou c'est passé l'evenement    
            events= [x for x in article.ents if  x.label_=='DATE']
            if len(events)>0:
                years=[]
                for elm in events:
                    if (str(elm)).isdigit():
                        years.append(int(str(elm)))
                if(len(years)>0):#année detecté 
                    year=(max(set(years)))
                    events.clear()
                    events.append(data.titles[k]+" in "+str(year))
                    all_events[k]=events
                    #print(k,"++",type(events),events)

                  #  print("++++++events final",k," ",all_events[k])

                else:#pas d'année detectée l'année est celle sur l'article
                    events.clear()
                    events.append(data.titles[k]+" in "+str(parser.parse(data.dates[k]).year))
                    all_events[k]=events
                    #print(k,"++",type(events),events)

                   # print("++++++events final",k," ",all_events[k])

            else :#pas d'annee detectée
                events.clear()
                events.append(data.titles[k]+" in "+str(parser.parse(data.dates[k]).year))
                all_events[k]=events
                #print(k,"++",type(events),events)

               # print("++++++events final",k," ",all_events[k])
                

   


# In[299]:

events_nn=[x for x in all_events if  not(str(x)).isdigit()]
places_nn=[x for x in all_places if  not(str(x)).isdigit()]
people_nn=[x for x in all_people if  not(str(x)).isdigit()]

print("for", number_of_articles,"article we got: \n",str(100*len(people_nn)/number_of_articles),"% of names of people \n",str(100*len(places_nn)/1000),"% of names of places \n",str(100*len(events_nn)/1000),"% of names of events ")


# ## Ajouter une granularité Temporelle: L'année

# In[259]:

all_years=[0 for i in range(number_of_articles)]

for k in range(number_of_articles):
    txt_propre = data.texts[k]+" "+data.titles[k]
    for c in clean_unicode:
        txt_propre = re.sub(c, clean_unicode[c], txt_propre)

    article = nlp(txt_propre)
    
    Dates= [x for x in article.ents if  x.label_=='DATE']
    
    
    

    if len(Dates)>0:
        years=[]
        for elm in Dates:
            if (str(elm)).isdigit():
                years.append(int(str(elm)))
        if(len(years)>0):#année detecté 
            year=(max(set(years)))
            all_years[k]=str(year)

        else:#pas d'année detectée (format detectables) ; Solution :l'année est celle sur l'article
            all_years[k]=str(parser.parse(data.dates[k]).year)

    else :#pas d'annee detectée
        all_years[k]=str(parser.parse(data.dates[k]).year)
      


# maintenant que les resultats sont satisfaisant on passe à l'étape prochaine!

# #    

# ## Visualiser Les intéractions entre les personnes et les lieux ou les evenements :

# Voyant comment on peut utiliser la librairy nx.
# 
# L'interaction entre les personnes et entre les lieux va etre interessante pour s'avoir quel endroit a été affécté par quel personne on annalysant phrase par phrase chaque article 
# 
# Pour l'interaction entre les personnes et les evenements plutot avec l'evenement marquant car pour la plupart des articles on a pas pu datecter plus qu'un seul evenement 

# In[182]:

import networkx as nx
import matplotlib.pyplot as plt
A=['Martin', 'Steadman']
B=['California', 'Florida', 'Louisiana', 'North Carolina']
new_A=[]
new_B=[]
for i in A:
    for j in B:
        new_A.append(i)
        new_B.append(j)
        
kg_df = pd.DataFrame({'source':new_A, 'target':new_B})
# create a directed-graph from a dataframe
G=nx.from_pandas_dataframe(kg_df, "source", "target", 
                          edge_attr=False, create_using=nx.MultiDiGraph())
plt.figure(figsize=(12,12))

pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()


# Appliquant ceci à un article de notre choix

# In[295]:

## ENTRER LE NUMERO DE L'ARTICLE QUE VOUS VOULEZ VISUALISEZ
Num_article_a_visualiser=0
article = nlp(data.texts[Num_article_a_visualiser])
sentences = [x for x in article.sents]


source=[]
target=[]
for sent in sentences:
############################
    clean_unicode = {
        "'": "",
        "-":" ",
        "\[ | \]":" ",
        ":":" ",
        ",":" ",
        "。" :" ",
        "、":" ",
        "；":" ",
        "（":" ",
        "）":" ",
        "<":" ",
        "《":" ",
        "》":" ",
        "LEAD":"" ,
        "A12:4.":"",
        "U.S.":"United States",
        "US":"United States",
        "U.S. States":"United States",
        "the":"",
        "New York's": "New York State"

    }
    ## we clean our sentences for a better extraction
    #CORPUS OF THE ARTICLE
    for c in clean_unicode:
        sent = re.sub(c, clean_unicode[c], str(sent))

##########################"
    
    article_sent = nlp(str(sent))
    places = [x for x in article_sent.ents if x.label_=='GPE']
    people = [x for x in article_sent.ents if x.label_=='PERSON']
    
    if len(people)>1:
        used = []
        for x in sorted(people):
            if str(x) not in used: #enlever les elements dupliqués de people
                used.append(str(x))


        people=used
    #### List of people still in progress reducing names based on similarity of words 
        p=people
      #print("article ",k,"+","people avant traitement",p)
        vectorizer = CountVectorizer(ngram_range=(1, 2))
        vectorizer.fit(p)
        X_bag_of_words = vectorizer.transform(p)
        X_bag_of_words.shape
        vectorizer.get_feature_names()
        D = X_bag_of_words.toarray()

        ones_array = np.ones( (len(D), len(D)), dtype=np.float64 ) 

        for i in range(len(D)):
            for j in range(len(D)):
                ones_array[i][j]=(cosinus(D[i, :], D[j, :]))

        #print(ones_array)
        indexes=np.where(ones_array >0.4)
        #print("indexes",indexes)
        repeated=[]
        for i,j in zip(indexes[0],indexes[1]) :
            if (i!=j and len(p[i])>len(p[j])):
                repeated.append(p[j])    
    #    indexes=np.where(ones_array >0.4)
    #    print("indexes",indexes)
    #    used=[]
    #    repeated=[]
    #    for i,j in zip(indexes[0],indexes[1]) :
    #        if (i!=j and len(p[i])>len(p[j])):
    #            repeated.append(p[j])
                #print(repeated)            #print(used)
                #p.pop(i)
                #print(p[i],p[j])

    #    new_people=[x for x in sorted(p) if x not in repeated]
        new_people=[x for x in sorted(p) if x not in repeated]
 #       print("nouvelle liste",new_people)
        final_entity=[]
        used=[]
        used2=[]

        for i in (range(len(new_people))):
            for j in (range(len(new_people))):
    #            print("++++++++",i,"+",j)

                if i!=j and (sorted((new_people[i]).split(" "))==sorted((new_people[j]).split(" "))) and i not in used:
     #               print(new_people[i],"+",(new_people[j]),"les memes!")
                    #new_people.remove(new_people[i])
                    used.append(i)
                    used.append(j)
                    final_entity.append(new_people[i])  
    #                print(final_entity,"en progres")
        for i in (range(len(new_people))):             
            if i not in used:
    #            print(new_people[i])
                final_entity.append(new_people[i])
    #            print(final_entity,"en progres")
        final_entity_people=final_entity
    else:
        if len(people)==1:
            final_entity_people=people # if len(final_entity_people)>0 else 0)


##################### Places :  
    ###################
    if len(places)>1:
        used1 = []
        for x in sorted(places):
            if str(x) not in used1:
                used1.append(str(x))#enlever les elm dupliqué


        places=used1
        p=places
        #print("article ",k,"+","people avant traitement",p)
        vectorizer = CountVectorizer(ngram_range=(1, 2))     #enlever des lieux se basant sur la similarité
        vectorizer.fit(p)
        X_bag_of_words = vectorizer.transform(p)
        X_bag_of_words.shape
        vectorizer.get_feature_names()
        D = X_bag_of_words.toarray()

        ones_array = np.ones( (len(D), len(D)), dtype=np.float64 ) 

        for i in range(len(D)):
            for j in range(len(D)):
                ones_array[i][j]=(cosinus(D[i, :], D[j, :]))

        #print(ones_array)
        indexes=np.where(ones_array >0.4)
        #print("indexes",indexes)
        repeated=[]
        for i,j in zip(indexes[0],indexes[1]) :
            if (i!=j and len(p[i])>len(p[j])):
                repeated.append(p[j])    
    #    indexes=np.where(ones_array >0.4)
    #    print("indexes",indexes)
    #    used=[]
    #    repeated=[]
    #    for i,j in zip(indexes[0],indexes[1]) :
    #        if (i!=j and len(p[i])>len(p[j])):
    #            repeated.append(p[j])
                #print(repeated)            #print(used)
                #p.pop(i)
                #print(p[i],p[j])

    #    new_people=[x for x in sorted(p) if x not in repeated]
        new_people=[x for x in sorted(p) if x not in repeated]
  #      print("nouvelle liste",new_people)
        final_entity=[]
        used=[]
        used2=[]

        for i in (range(len(new_people))):
            for j in (range(len(new_people))):
    #            print("++++++++",i,"+",j)

                if i!=j and (sorted((new_people[i]).split(" "))==sorted((new_people[j]).split(" "))) and i not in used:
                    #print(new_people[i],"+",(new_people[j]),"les memes!")
                    #new_people.remove(new_people[i])
                    used.append(i)
                    used.append(j)
                    final_entity.append(new_people[i])  
    #                print(final_entity,"en progres")
        for i in (range(len(new_people))):             
            if i not in used:
    #            print(new_people[i])
                final_entity.append(new_people[i])
    #            print(final_entity,"en progres")
        final_entity_places=final_entity
    else:
        if len(places)==1:
            final_entity_places=places #if len(final_entity_places)>0 else 0)
        
        
#
    
    if(len(final_entity_people)>=1 and len(final_entity_places)>=1):

        for i in final_entity_people:
            for j in final_entity_places:
                #print("type",type(i),"++",type(j))
                if (str(i),str(j)) in zip(source,target):#toute les combinaisons sur les personnes et les lieux dans la mm phrase
                    print(i,"+",j,"Already in")
                else:
                    source.append(str(i))
                    target.append(str(j))
                    print(i,j)
        




# In[190]:


d1 = pd.DataFrame({'source':source, 'target':target})
# create a directed-graph from a dataframe
G=nx.from_pandas_dataframe(d1, "source", "target", 
                          edge_attr=False, create_using=nx.MultiDiGraph())
plt.figure(figsize=(8,8))
titre="Connections Personnes-> Lieux pour l'article "+str(Num_article_a_visualiser)+" :"+data.titles[Num_article_a_visualiser]
plt.title(titre)


pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()


# In[272]:

#Connection Personne->Event pour un article
num_article=78
source=[]
target=[]

import networkx as nx
import matplotlib.pyplot as plt
A=all_people[num_article]
B=all_events[num_article]
new_A=[]
new_B=[]
for i in A:
    for j in B:
        new_A.append(i)
        new_B.append(j)
        
kg_df = pd.DataFrame({'source':new_A, 'target':new_B})
# create a directed-graph from a dataframe
G=nx.from_pandas_dataframe(kg_df, "source", "target", 
                          edge_attr=False, create_using=nx.MultiDiGraph())
plt.figure(figsize=(8,8))
titre="Connections Personnes-> Evenement pour l'article "+str(num_article)+" :"+data.titles[num_article]
plt.title(titre)

pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()


# ## Création du nouvelle Dataset enrichie de méta informations

# In[260]:

df = pd.DataFrame({'Texts': data.texts[0:1000],
                   'Titles': data.titles[0:1000],
                   'Dates':data.dates[0:1000],
                   'Week':data.week[0:1000],
                   'Years':all_years,                       
                   'People':all_people,
                   'Places':all_places,
                   'Events':all_events,
                   'Principal_classifier':data.principal_classifier[0:1000],
                   'Scnd_classifier':data.second_classifier[0:1000],
                   'Third_classifier':data.third_classifier[0:1000]})


# In[261]:

df.to_csv("/home/toutou/nyt.csv/nyt5.csv",sep='\t')


# In[263]:

import pandas as pd
data2 = pd.read_csv("/home/toutou/nyt.csv/nyt5.csv",sep='\t') 
data2.head()


# ## Moteur de Recherche

# In[273]:

query='Alfred Del Bello'
q = CountVectorizer(ngram_range=(1, 2))
q.fit([query])
query_comb= q.get_feature_names()


# In[274]:

from sklearn.feature_extraction.text import TfidfVectorizer
texts = data2.Texts
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_vectorizer.fit(texts)
X_texts = tfidf_vectorizer.transform(texts)
ngram_comb_texts= tfidf_vectorizer.get_feature_names()
D_texts = X_texts.toarray()
n_docs, n_terms_texts = D_texts.shape
n_terms_texts,n_docs


# In[275]:

titles = data2.Titles
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_vectorizer.fit(titles)
X_titles = tfidf_vectorizer.transform(titles)
ngram_comb_titles= tfidf_vectorizer.get_feature_names()
D_titles = X_titles.toarray()
n_docs, n_terms_titles = D_titles.shape
n_terms_titles,n_docs


# In[276]:

People = data2.People
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_vectorizer.fit(People)
X_People = tfidf_vectorizer.transform(People)
ngram_comb_People= tfidf_vectorizer.get_feature_names()
D_People = X_People.toarray()
n_docs, n_terms_People = D_People.shape
n_terms_People,n_docs


# In[277]:

Places = data2.Places
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_vectorizer.fit(Places)
X_Places = tfidf_vectorizer.transform(Places)
ngram_comb_Places= tfidf_vectorizer.get_feature_names()
D_Places = X_Places.toarray()
n_docs, n_terms_Places = D_Places.shape
n_terms_Places,n_docs


# In[278]:

Events = data2.Events
tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_vectorizer.fit(Events)
X_Events = tfidf_vectorizer.transform(Events)
ngram_comb_Events= tfidf_vectorizer.get_feature_names()
D_Events = X_Events.toarray()
n_docs, n_terms_Events = D_Events.shape
n_terms_Events,n_docs


# Les Indexes qui reresentes la requette query par rapport à chaque Meta Information et par rapport au corp de l'article

# In[279]:

indexes_texts = [ngram_comb_texts.index(q) for q in query_comb if q in ngram_comb_texts]
indexes_titles = [ngram_comb_titles.index(q) for q in query_comb if q in ngram_comb_titles]
indexes_people = [ngram_comb_People.index(q) for q in query_comb if q in ngram_comb_People]
indexes_places = [ngram_comb_Places.index(q) for q in query_comb if q in ngram_comb_Places]
indexes_events = [ngram_comb_Events.index(q) for q in query_comb if q in ngram_comb_Events]



# In[280]:

query_vec_text = np.zeros(n_terms_texts)
query_vec_text[indexes_texts] = 1

query_vec_title = np.zeros(n_terms_titles)
query_vec_title[indexes_titles] = 1

query_vec_people = np.zeros(n_terms_People)
query_vec_people[indexes_people] = 1

query_vec_places = np.zeros(n_terms_Places)
query_vec_places[indexes_places] = 1

query_vec_events = np.zeros(n_terms_Events)
query_vec_events[indexes_events] = 1



# In[281]:

cosinus(D_texts[3, :], query_vec_text),cosinus(D_titles[3, :], query_vec_title),cosinus(D_People[3, :], query_vec_people),cosinus(D_Places[3, :], query_vec_places),cosinus(D_Events[3, :], query_vec_events)


#  Vu que les indexes Resume mieux l'information et que l'utilisateur cherchera en utilisant une requette syntetique on donnera un score plus élevé aux indexes titre, person, lieux et evenement égale à 2 
#  et un poid de 1 aux score pour celui du text

# In[282]:

def search(query, data2,n_gram):
    q = CountVectorizer(ngram_range=n_gram)
    q.fit([query])
    query_comb= q.get_feature_names()    
    
    texts = data2.Texts
    tfidf_vectorizer = TfidfVectorizer(ngram_range=n_gram)
    tfidf_vectorizer.fit(texts)
    X_texts = tfidf_vectorizer.transform(texts)
    ngram_comb_texts= tfidf_vectorizer.get_feature_names()
    D_texts = X_texts.toarray()
    n_docs, n_terms_texts = D_texts.shape

    titles = data2.Titles
    tfidf_vectorizer = TfidfVectorizer(ngram_range=n_gram)
    tfidf_vectorizer.fit(titles)
    X_titles = tfidf_vectorizer.transform(titles)
    ngram_comb_titles= tfidf_vectorizer.get_feature_names()
    D_titles = X_titles.toarray()
    n_docs, n_terms_titles = D_titles.shape

    Places = data2.Places
    tfidf_vectorizer = TfidfVectorizer(ngram_range=n_gram)
    tfidf_vectorizer.fit(Places)
    X_Places = tfidf_vectorizer.transform(Places)
    ngram_comb_Places= tfidf_vectorizer.get_feature_names()
    D_Places = X_Places.toarray()
    n_docs, n_terms_Places = D_Places.shape

    Events = data2.Events
    tfidf_vectorizer = TfidfVectorizer(ngram_range=n_gramd)
    tfidf_vectorizer.fit(Events)
    X_Events = tfidf_vectorizer.transform(Events)
    ngram_comb_Events= tfidf_vectorizer.get_feature_names()
    D_Events = X_Events.toarray()
    n_docs, n_terms_Events = D_Events.shape    
    
    indexes_texts = [ngram_comb_texts.index(q) for q in query_comb if q in ngram_comb_texts]
    indexes_titles = [ngram_comb_titles.index(q) for q in query_comb if q in ngram_comb_titles]
    indexes_people = [ngram_comb_People.index(q) for q in query_comb if q in ngram_comb_People]
    indexes_places = [ngram_comb_Places.index(q) for q in query_comb if q in ngram_comb_Places]
    indexes_events = [ngram_comb_Events.index(q) for q in query_comb if q in ngram_comb_Events]

    
    query_vec_text = np.zeros(n_terms_texts)
    query_vec_text[indexes_texts] = 1

    query_vec_title = np.zeros(n_terms_titles)
    query_vec_title[indexes_titles] = 1

    query_vec_people = np.zeros(n_terms_People)
    query_vec_people[indexes_people] = 1

    query_vec_places = np.zeros(n_terms_Places)
    query_vec_places[indexes_places] = 1

    query_vec_events = np.zeros(n_terms_Events)
    query_vec_events[indexes_events] = 1    
    cc = {i: cosinus(D[i, :], q) for i in range(n_docs)}
    cc = sorted(cc.items(), key=lambda x: x[1], reverse=True)
    return cc


# In[283]:

cosinus(D_texts[2, :], query_vec_text)+2*cosinus(D_titles[2, :], query_vec_title)+2*cosinus(D_People[2, :], query_vec_people)+2*cosinus(D_Places[2, :], query_vec_places)+2*cosinus(D_Events[2, :], query_vec_events)


# In[284]:

cc = {i: cosinus(D_texts[i, :], query_vec_text)+2*cosinus(D_titles[i, :], query_vec_title)+2*cosinus(D_People[i, :], query_vec_people)+2*cosinus(D_Places[i, :], query_vec_places)+2*cosinus(D_Events[i, :], query_vec_events) for i in range(n_docs)}
cc = sorted(cc.items(), key=lambda x: x[1], reverse=True)


# In[285]:

#cc=search(query, data2,(1,2))
cc[0:10]


# In[288]:

nb_top_docs = 10
top_docs = [r for (r,v) in cc[0:nb_top_docs]]
print("Les Meuilleurs",str(nb_top_docs)," Resultats Corespandant à la requette ",'"',query,'"',":")
for i, td in zip(range(nb_top_docs), top_docs):
    #print(top_feats_in_doc(X_hp, features_hp, td))
    print("%s (%s): %s" % (i+1, td, titles[td]))



# In[290]:

nb_top_docs = 10
top_docs = [r for (r,v) in cc[0:nb_top_docs]]
print("Les Personnes Corespandant à chaque article par rapport à la requette ",'"',query,'"',":")

for i, td in zip(range(nb_top_docs), top_docs):
    #print(top_feats_in_doc(X_hp, features_hp, td))
    print("%s (%s): %s" % (i+1, td, People[td]))

