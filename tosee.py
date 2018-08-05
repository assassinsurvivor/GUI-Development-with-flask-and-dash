import pandas as pd

df=pd.read_csv("helper_data/data.csv")
tohave=df["Unnamed: 0"].tolist()

colors= [
    '#1f77b4',  
    '#ff7f0e',  
    '#2ca02c',  
    '#d62728',  
    '#9467bd',  
    '#8c564b',  
    '#e377c2',  
    '#7f7f7f',  
    '#bcbd22',  
    '#17becf'   
]

df_2=pd.read_csv("helper_data/Diagnosis_important.csv")

lister=df_2["code"].tolist()

indices=[]

for i in lister:
    #print(i)
    try:
        x=tohave.index(i)
        indices.append(x)
        
    except:
        pass



trapcolors=['#1f77b4']*len(df)
cache=15
counter=0
marker=[1]*len(df)
kk=1
for i in indices:
    counter+=1
    if kk==0:
        break
    if counter>150:
        counter=0
        kk+=1
        if kk==9:
            kk=0
    
    trapcolors[i]=colors[kk]
    marker[i]=cache
    cache=cache-.003



        
    
