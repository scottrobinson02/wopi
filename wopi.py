import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import datetime

configfile = sys.argv[2] ##name of json file

savepng = False
if (len(sys.argv) > 3) and sys.argv[3] == "-s":
    savepng = True
    if len(sys.argv) > 4 :
        if ((str(sys.argv[4]))[-4:] != ".png"): ##if name has no .png, add .png
            savefile = sys.argv[4] + ".png"
        else:
            savefile = sys.argv[4]
    else:
        savefile = ("output " + str(datetime.datetime.now())[0:-7] + ".png") ##if name unspecified, default to output [time] .png

with open(configfile,"r") as j:
    joutput = json.load(j)

valuenames = (np.array(joutput["axesNames"])) ##Names of the axes
title = (joutput["title"])

ax = plt.axes([0,0,1,1],projection = "polar")
plt.title(title)

valuesno = (len(valuenames) + 1) ##number of variables +1

webs = (len(joutput["groups"])) ##number of web plots to draw

def webplot(id) :

    initvalues = (np.array(joutput["groups"][id]["axesValues"]))

    values= np.append(initvalues,initvalues[0]) ##adds first value to end so that polygon is connected

    namelocations= (np.linspace(0,1, num = valuesno)) * (2 *np.pi) ##locations to put labels/ticks
    namelocations = np.delete(namelocations,-1) ##deletes final value to avoid duplicating the first label's text

    X = np.linspace(0, (2 * np.pi), valuesno)
    Y = values

    plt.fill_between(X, Y,alpha = 0.2)
    plt.xticks(namelocations, valuenames)
    
    ax.plot(X,Y, label=joutput["groups"][id]["group"])

    if (savepng == True):
        ax.legend(loc="upper right", bbox_to_anchor=(1.15, 1.15)) ##legend 
    else:
        ax.legend(fontsize = "small", loc="upper right", bbox_to_anchor=(1.1, 1)) ##legend closer when showing vs saving, otherwise it would get cropped

for x in range(webs):
    webplot(x) ##draws all graphs

if (savepng == True):
    plt.savefig(savefile, dpi=100, bbox_inches="tight")
else:
    plt.show()
