import matplotlib.pyplot as plt
import numpy as np
np.random.seed(1)
import pickle
import pandas as pd
import numpy as np
import os
from sklearn.manifold import TSNE

os.chdir(r"C:\Users\PT18999\downloads/")

pickle_in = open(r"code2vec.pkl","rb")
ex_dict = pickle.load(pickle_in)
list_of_code=list(ex_dict.keys())
list_of_values=list(ex_dict.values())
df=pd.read_csv("data_helper/Diagnosis_code.csv")

dff=pd.DataFrame()
dff["DIAGNOSIS_CODE"]=list_of_code
dff["Embeddings"]=list_of_values
df_final=pd.merge(dff,df,how="inner",on="DIAGNOSIS_CODE")

input_tsne=np.array(df_final["Embeddings"].tolist())

markers_s=list(range(len(df_final["DIAGNOSIS_DESCRIPTION"])))

clf=TSNE(n_components=2,n_iter=400).fit_transform(input_tsne)

diagnosis=pd.read_csv("data_helper/Diagnosis_head.csv")
keep=list(diagnosis.DIAGNOSIS_CODE.value_counts()[0:150].index)
df_final['2D']=list(clf)
df_top=df_final[df_final["DIAGNOSIS_CODE"].isin(keep)]
def remove(x):
    x=x.split(',')[0]
    x=x.split('(')[0]

    return x
df_top.DIAGNOSIS_DESCRIPTION=df_top.DIAGNOSIS_DESCRIPTION.apply(remove)

x_coords=[]
y_coords=[]
for index,row in df_top.iterrows():
    x_coords.append(row['2D'][0])
    y_coords.append(row['2D'][1])



x = x_coords
y = y_coords
names =df_top['DIAGNOSIS_DESCRIPTION'].tolist()
c = np.random.randint(1,5,size=len(x_coords))

norm = plt.Normalize(1,4)
cmap = plt.cm.RdYlGn

fig,ax = plt.subplots()
sc = plt.scatter(x,y,c=c, s=100, cmap=cmap, norm=norm)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
                           " ".join([names[n] for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
