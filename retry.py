
#!/usr/bin/env python
 
import re
import sys
import datetime
import math  
import pandas as pd


def intf(v):
    try:
        val=int(v)
        return(val)
    except:
      val = ''.join([c for c in v if c in '1234567890.'])
    #print(v, val)
      try:
          return(int(val))
      except:
          return(0)  


def floatf(v):
                  
    try:
        val=float(v)
        return(val)
    except:
      val = ''.join([c for c in v if c in '1234567890.e'])
    #print(v, val)
      try:
          return(float(val))
      except:
          return(0)  
          
##### LOAD THESE TABLES INTO ARRAYS ########## 
dealLk = {}
obs=0
dealInfo=pd.read_csv("K:\FASB ASU 2015-09\Loss triangles\code\deals.txt", sep='\t',header=1)
for a in range(0,dealInfo.shape[0]):
    obs = obs + 1
    dl = dealInfo.iat[a,0]
    dealLk[dl]=a
 
durs_lkup = {}   
dur=pd.read_csv("K:\FASB ASU 2015-09\Loss triangles\code\durations.txt", sep='\t',header=1)
for a in range(0,dur.shape[0]):
    dl = dur.iat[a,0]
    durs_lkup[dl]=a
    #print(a, dl, durs_lkup[dl])

deal_part = {}   
curr_part = {}   
deal_Curr = {}   
tot_ult = {}  #by deal + curr (Those in the valid range)
tot_ult_2bAlloc = {}  #by deal + curr (Those in the valid range)
alloc_ult = {}  #by deal + curr + accyr
perc_ult = {}
active_years = {}
AY_Ult = {}

ultsin=pd.read_csv("K:\FASB ASU 2015-09\Loss triangles\code\ultimates.txt", sep='\t',header=1)
for a in range(1,ultsin.shape[0]):
    dealio = ultsin.iat[a,0]
    tmp = ultsin.iat[a,1]
    dlcurr = ultsin.iat[a,2]
    deal_Curr[dlcurr]=a
    deal_part[dlcurr]=dealio
    curr_part[dlcurr]=tmp #currency
    
    try:
      durtn= dur.iat[durs_lkup[dealio],1]  
    except:
      #print("No duration for ", dealio)
      durtn=2
    warn=0
    try:
      strt= dealInfo.iat[dealLk[dealio],10]
      expire_dtin= dealInfo.iat[dealLk[dealio],11]  
    except:
      #print("No info for ",dealio)#
      warn=1
    x_d = expire_dtin.split('/')
    x_yr=int(x_d[2])
    last_valid_year = x_yr + 1

    #initialize allocations to zeros
    for yrs in range(2006,2017):
         deal_curr_yr = dlcurr + str(yrs)
         alloc_ult[deal_curr_yr]=0
         
    tot_ult[dlcurr]=float(0)
    tot_ult_2bAlloc[dlcurr]=float(0)
    
    everActive = 0
    #active_years[dlcurr] = []
    for indx in range(17,28):
      yr=2016-27+indx #nada
      deal_curr_yr = dlcurr + str(yr)
      incremental = floatf(ultsin.iat[a,indx])
      everActive = abs(incremental) + everActive
      if yr <= last_valid_year and incremental > 0:
         tot_ult[dlcurr]=tot_ult[dlcurr] + incremental
         if dlcurr not in active_years:
           active_years[dlcurr] = [yr]  
         else:             
           active_years[dlcurr] = active_years[dlcurr].append(yr)
      else:
         #print("hm ", ultsin.iat[a,indx], x)
         tot_ult_2bAlloc[dlcurr] =  tot_ult_2bAlloc[dlcurr] +  incremental
    if dlcurr not in active_years:
          active_years[dlcurr] = [0]
    #we now know totals so lets allocate             
    for indx in range(17,28):
      yr=2016-27+indx #nada
      deal_curr_yr = dlcurr + str(yr)
      incremental = floatf(ultsin.iat[a,indx])

      try:  #doing it this way because some deals have no active years
          if yr in active_years[dlcurr]:
              actv='Y'
      except:
           actv='N'

      print(dlcurr, active_years[dlcurr])
      #if actv == 'Y':         
      if yr  in active_years[dlcurr]:
         AY_Ult[deal_curr_yr] = incremental 
      else:
         for ay in active_years[dlcurr]:
             indexTmp = 2016 - 27 + intf(ay)
             numerator = floatf(ultsin.iat[a,indexTmp])             
             deal_curr_yr_tmp = dlcurr + str(ay)
             toAdd = incremental * numerator / tot_ult[dlcurr] 
             if deal_curr_yr_tmp in AY_Ult:
                 AY_Ult[deal_curr_yr_tmp] = AY_Ult[deal_curr_yr_tmp] + toAdd
             else:
                 AY_Ult[deal_curr_yr_tmp] = toAdd
                  
    if warn==1 and everActive>0:
       print(dealio, tot_ult[dlcurr])
    for yrs in range(2006,2017):
       deal_curr_yr = dlcurr + str(yrs)
       #perc_ult
       #  alloc_ult[deal_curr_yr] = alloc_ult[deal_curr_yr] + ultsin.iat[a,indx]
    
  
           
deal=48
print("here", deal, strt, expire_dtin,x_yr )
#print(dur)