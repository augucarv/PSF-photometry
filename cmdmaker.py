# Makes CMD and GCLF diagrams from .raw DAOPHOT files

import pandas as pd

survey = 'SURV_NAME'
galname = 'GAL_NAME'
band1 = 'i' # e.g. i
band2 = 'g' # e.g. g
raw_file = survey+'_'+band1+'.raw' # Or input directly your own, but don't forget to add _(band) for the code to work
ext_band1 = 0 # Extinction for band 1 filter
ext_band2 = 0 # Extinction for band 2 filter

df = pd.read_csv(raw_file,sep = '\s+',skiprows=2,header=None) # Importing raw file
df.rename(columns={3:'MAG_'+band1,4:'ERR_'+band1,5:'MAG_'+band2,6:'ERR_'+band2}, inplace=True) # Renaming columns
index_list = df[((df['MAG_'+band1] == 99.9999)&(df['ERR_'+band1] == 9.9999)) | ((df['MAG_'+band2] == 99.9999)&(df['ERR_'+band2] == 9.9999))].index.tolist() # checking for 9999
cat = df[['MAG_'+band1,'MAG_'+band2]].drop(index_list) # Dropping non-matched objects

cat['MAG_'+band1]=cat['MAG_'+band1]+ext_band1
cat['MAG_'+band2]=cat['MAG_'+band2]+ext_band2

comb = cat['MAG_'+band2]-cat['MAG_'+band1]

import matplotlib.pyplot as plt

plt.figure(0)
plt.scatter(comb,cat['MAG_'+band2],c='red',s=1)
plt.xlabel('$'+band2+'-'+band1+'$',fontsize = 14)
plt.ylabel('$g$',fontsize = 14)
plt.rc('xtick', labelsize=10) 
plt.rc('ytick', labelsize=10) 
plt.title('CMD for '+galname+' ('+raw_file[:-6]+')',fontsize = 16)
plt.grid()
plt.tight_layout()
plt.savefig('CMD_'+raw_file[:-6]+'.png',dpi=300)

plt.figure(1)
plt.hist(cat['MAG_'+band2],color='green')
plt.xlabel('$'+band2+'$',fontsize = 14)
plt.ylabel('N',fontsize = 14)
plt.rc('xtick', labelsize=10) 
plt.rc('ytick', labelsize=10) 
plt.title('GCLF '+galname+' ('+raw_file[:-6]+')'+' - $'+band2+'_{band}$',fontsize = 16)
plt.grid()
plt.tight_layout()
plt.savefig('GCLF_'+raw_file[:-6]+'_'+band2+'.png',dpi=300)

plt.figure(2)
plt.hist(cat['MAG_'+band1],color='red')
plt.xlabel('$'+band1+'$',fontsize = 14)
plt.ylabel('N',fontsize = 14)
plt.rc('xtick', labelsize=10) 
plt.rc('ytick', labelsize=10) 
plt.title('GCLF '+galname+' ('+raw_file[:-6]+')'+' - $'+band1+'_{band}$',fontsize = 16)
plt.grid()
plt.tight_layout()
plt.savefig('GCLF_'+raw_file[:-6]+'_'+band1+'.png',dpi=300)

plt.figure(3)
plt.hist(comb)
plt.xlabel('$'+band2+'-'+band1+'$',fontsize = 14)
plt.ylabel('N',fontsize = 14)
plt.rc('xtick', labelsize=10) 
plt.rc('ytick', labelsize=10) 
plt.title('GCLF '+galname+ ' ('+raw_file[:-6]+')'+' - $('+band2+'-'+band1+')_{band}$',fontsize = 16)
plt.grid()
plt.tight_layout()
plt.savefig('GCLF_'+raw_file[:-6]+'_'+band2+band1+'.png',dpi=300)
