import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


regex_str=r"B;\d+;(\d+);RLO_BEGIN;"

logfile_path="/home/maglione/SEVNproject/sevn_output_0.02/logfile_1.dat"

with open(logfile_path,"r") as fo:
	ma=re.findall(regex_str,fo.read())

BID = pd.DataFrame({'ID':np.asarray(ma,dtype=int)})

print(BID)

BID= BID.groupby(['ID']).size().reset_index(name='NCE')

output_path="/home/maglione/SEVNproject/sevn_output_0.02/output_1.csv"
df = pd.read_csv(output_path)

idx_compact_primary= (df.RemnantType_0==1) | (df.RemnantType_0==4) | (df.RemnantType_0==5) | (df.RemnantType_0==6) 
idx_compact_secondary= (df.RemnantType_1==1) | (df.RemnantType_1==4) | (df.RemnantType_1==5) | (df.RemnantType_1==6)
idxcomp=(idx_compact_primary) & (idx_compact_secondary) & (df.Semimajor.notnull())
idxcomp=(idx_compact_primary) & (df.Semimajor.notnull())
dfcomp=df[idxcomp]

dfmerged=pd.merge(dfcomp,BID,on='ID',how="left")

print(dfmerged)


### defyining time ranges in Myr within which plotting the HR diagrams###

tranges=((0,2),(2,3),(3,5),(5,7),(7,10),(10,13),(13,15),(15,17),(17,20)) #Myr
plt.figure(figsize=(20,20))

### plotting the HR diagrams with plt.subplot ###

for i,tim in enumerate(tranges):
    tlow,tup=tim

    plt.subplot(3,3,i+1)
    
### defyning two coefficients to fullfill conditions on BWolrdtime, Phase and Event ###
    
    c_0_RLO=(dfmerged.BWorldtime>=tlow) & (dfmerged.BWorldtime<=tup) & (dfmerged.Phase_0<7)
    c_1_RLO=(dfmerged.BWorldtime>=tlow) & (dfmerged.BWorldtime<=tup) & (dfmerged.Phase_1<7)
   
### concatenating values for Luminosity and Temperature in RLO and RLO+merger###
    
    Lum_RLO = pd.concat([dfmerged.Luminosity_0[c_0_RLO],dfmerged.Luminosity_1[c_1_RLO]])
    Temp_RLO = pd.concat([dfmerged.Temperature_0[c_0_RLO],dfmerged.Temperature_1[c_1_RLO]])
    
### plotting the HR diagram with hexbin - tried also with scatter ###
    
    plot1=plt.hexbin(np.log10(Temp_RLO),np.log10(Lum_RLO),cmap="winter",mincnt=1)
    
    cbar1=plt.colorbar(mappable=plot1,pad=0)
    cbar1.set_label(label="N",size=10)
    plt.xlim(5.5,3.5)
    plt.ylim(1.,7.5)
    plt.xlabel("$\log T/\mathrm{K}$",fontsize=15)
    plt.ylabel("$\log L/\mathrm{L_\odot}$",fontsize=15)
    plt.title("{tlow}<Age/Myr<{tup}",fontsize=18)
    
plt.tight_layout()
plt.show()

