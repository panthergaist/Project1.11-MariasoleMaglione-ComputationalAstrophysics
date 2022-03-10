import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### using pandas to read SEVN outputs ###

dtt=pd.read_csv("/home/maglione/SEVNproject/sevn_output_0.04/output_1.csv")
print(dtt)
print(dtt.columns)

### defyining time ranges in Myr within which plotting the HR diagrams###

tranges=((0,1),(1,2),(2,3),(3,3.5),(3.5,4),(4,4.5)) #Myr
plt.figure(figsize=(20,20))

### plotting the HR diagrams with plt.subplot ###

for i,tim in enumerate(tranges):
    tlow,tup=tim

    plt.subplot(2,3,i+1)
    
### defyning two coefficients to fullfill conditions on BWolrdtime and Phase ###
    
    c_0=(dtt.BWorldtime>=tlow) & (dtt.BWorldtime<=tup) & (dtt.Phase_0<7)
    c_1=(dtt.BWorldtime>=tlow) & (dtt.BWorldtime<=tup) & (dtt.Phase_1<7)
    
    
### printing the BEvent of the BS ###
    
    BEvent = pd.concat([dtt.BEvent[c_0],dtt.BEvent[c_1]])
    
    RLO_num=[]
    RLO_merge_num=[]
    RLO_ce_num=[]
    coll_merge_num=[]
    coll_ce_num=[]
     
    for eve in BEvent:
        if eve==4: #Roche-Lobe Overflow (RLO) start
            RLO_num.append(eve)
        if eve==10: #Roche-Lobe Overflow (RLO) + Merger
            RLO_merge_num.append(eve)
        if eve==11: #Roche-Lobe Overflow (RLO) + Common Envelope
            RLO_ce_num.append(eve)
        if eve==13: #Collision + Merger
            coll_merge_num.append(eve)
        if eve==14: #Collision + Common Envelope
            coll_ce_num.append(eve)

    #fname="ssefile.txt" #ouput filename as a string
    #f=open(fname,"w") #creating file w which will be for writing

    #for j in range(len(m)):
    	#f.write((RLO_num[j])+" "+(RLO_merge_num[j])+" "+(RLO_ce_num[j])+" "+(coll_merge_num[j])+" "+(coll_ce_num[j])+"\n")
    #f.close()

           
    print("RLO start events from", tlow, "<Age<", tup, "are ",len(RLO_num), "\n", "RLO+merge events from", tlow, "<Age<", tup, "are ",len(RLO_merge_num), "\n", "RLO+CE events from", tlow, "<Age<", tup, "are ",len(RLO_ce_num), "\n", "C+merge events from", tlow, "<Age<", tup, "are ",len(coll_merge_num), "\n", "C+CE events from", tlow, "<Age<", tup, "are ",len(coll_ce_num))
    
   
### concatenating values for Luminosity and Temperature ###
    
    Luminosity = pd.concat([dtt.Luminosity_0[c_0],dtt.Luminosity_1[c_1]])
    Temperature = pd.concat([dtt.Temperature_0[c_0],dtt.Temperature_1[c_1]])

    
### plotting the HR diagram with hexbin - tried also with scatter ###
    
    plt.hexbin(np.log10(Temperature),np.log10(Luminosity),cmap="plasma",mincnt=1)
    
    cbar=plt.colorbar(pad=0)
    cbar.ax.tick_params(axis='both', which='major', labelsize=16)
    cbar.set_label(label="$N$",size=15)
    plt.xlim(5.5,3.5)
    plt.ylim(1.,7.)
    plt.xlabel("$\log T/\mathrm{K}$",fontsize=18)
    plt.ylabel("$\log L/\mathrm{L_\odot}$",fontsize=18)

    #plt.gca().tick_params(axis='both', which='major',labelsize=18)
    plt.title(f"{tlow}<Age/Myr<{tup}",fontsize=20)
    
plt.tight_layout()
plt.show()

lum_min=min(np.log10(Luminosity))

print('The minimum Luminosity reached is: ', lum_min)

plt.tight_layout()
plt.show()
