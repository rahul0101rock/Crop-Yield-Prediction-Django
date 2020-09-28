from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pylab
plt.rc("font", size=14)
import PIL, PIL.Image
from io import StringIO
from sklearn.linear_model import LinearRegression
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)
def ploting(request) :
    data=pd.read_csv("/home/predictcrop/crop_predict/production/apy.csv", header=0)
    data=data.dropna()
    inp=str(request.GET['inp']).split('@')
    dis=inp[0]
    season=inp[1]
    s=list(data["Season"].unique())
    for x in s:
        if season.title() in x:
            sin=s.index(x)
    d = data[data["District_Name"]==dis.upper()][data["Season"]==s[sin]]["Crop"].unique()
    c=[]
    p=[]
    for crop in d:
        c.append(crop)
        a = data[data["Crop"]==crop][data["District_Name"]==dis.upper()][data["Season"]==s[sin]]["Area"]
        y = data[data["Crop"]==crop][data["District_Name"]==dis.upper()][data["Season"]==s[sin]]["Production"]
        reg=LinearRegression()
        reg.fit(a.values.reshape(-1,1),y.values.reshape(-1,1))
        coeff=(reg.coef_)
        p.append(coeff[0][0])
    fig=plt.figure()
    ax = fig.add_axes([0,0,1,1])
    crname=[]
    pr=p.copy()
    pr.sort(reverse=True)
    for x in pr:
        crname.append(c[p.index(x)])
    tstr='Approx Prodction in        District: '+dis.title()+'      Season: '+season.title()
    ax.set_title(tstr,fontsize=15)
    ax.set_ylabel('Production', fontsize=14)
    ax.set_xlabel('Crop', fontsize=13)
    plot=ax.bar(crname[:5],pr[:5 ])
    plt.savefig('static/plot.png', dpi=400, bbox_inches='tight')
    response="""<html><head>
    <meta http-equiv="refresh" content="2; URL=http://predictcrop.pythonanywhere.com/static/plot.png" />
    </head></html>"""
    return HttpResponse(response)