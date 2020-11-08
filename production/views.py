from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pylab
plt.rc("font", size=14)
import PIL, PIL.Image
from io import StringIO
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)
def ploting(request) :
    data=pd.read_csv("/home/predictcrop/crop_predict/production/Crop_Production_with_rainfall.csv")
    rain=pd.read_csv("/home/predictcrop/crop_predict/production/Rainfall Predicted.csv")
    data=data.dropna()
    inp=str(request.GET['inp']).split('@')
    dis=inp[0]
    season=inp[1]
    area_in=inp[2]
    s=list(data["Season"].unique())
    for x in s:
        if season.title() in x:
            sin=s.index(x)
    state=list(data[data["District_Name"]==dis.upper()]["State_Name"][:1])[0]
    data_cu=data[data["District_Name"]==dis.upper()][data["Season"]==s[sin]]
    data1 = data_cu.drop(["State_Name","Crop_Year"],axis=1)
    data_dum = pd.get_dummies(data1)
    x = data_dum.drop("Production",axis=1)
    y = data_dum[["Production"]]

    model = RandomForestRegressor()
    model.fit(x,y.values.ravel())

    ch=pd.DataFrame()
    for crop in list(data_cu["Crop"].unique()):
        t=(x[x["Crop_{}".format(crop)]==1])[:1]
        ch=pd.concat([ch,t])
    ch["Area"]=area_in
    predict=model.predict(ch)
    crname=data.loc[ch.index]["Crop"]
    crdata= {'Crop': list(crname),
            'Production': list(predict)}
    crpro = pd.DataFrame(crdata)
    ch["Rainfall"]=list(rain[rain["State_Name"]==state]["Rainfall"])[0]
    crpro=crpro.sort_values(by=['Production'], ascending=False)
    print(crpro)
    fig=plt.figure()
    ax = fig.add_axes([0,0,1,1])
    tstr='Predicted Production in        District: '+dis.title()+'      Season: '+season.title()
    ax.set_title(tstr,fontsize=15)
    ax.set_ylabel('Production in Tones', fontsize=14)
    ax.set_xlabel('Crop', fontsize=13)
    ax.bar(list(crpro["Crop"])[:5], list(crpro["Production"])[:5])
    plt.savefig('static/plot.png', bbox_inches='tight')
    response="""<html><head>
    </head><body><a href="http://predictcrop.pythonanywhere.com/static/plot.png">Graph</a></body></html>"""
    return HttpResponse(response)
