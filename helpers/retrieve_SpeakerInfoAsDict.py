
# coding: utf-8

"""
retrieve_SpeakerInfoAsDict.py

## Example uses: 

    ## retrieve_SpeakerInfoAsDict(DF0)
    where DF0 = makeDFfromJson(ibm_out)
    returns speakerDict (seeBelow)
    

---------------------------------------------------------------------------
    ** if using functions separately:
    
    ## from makeDFfromJson import makeDFfromJson
    ## DF0 = makeDFfromJson(ibm_out)


    DF1 = addTimeDiff_toDF(DF0) 
    # DF1 

    TimeDiffIDX = findTimeDiffIDX(DF1)
    # TimeDiffIDX

    tofromSent = get_SentenceNtofrom(DF1,TimeDiffIDX)
    # tofromSent

    SentenceInfo = get_SentenceInfo(DF1,TimeDiffIDX)
    # SentenceInfo.reset_index(drop=True)

    DF2 = pd.concat([SentenceInfo.reset_index(drop=True),tofromSent],axis=1)
    # DF2

    speakerDict = make_SpeakerDict(DF2)
    # speakerDict
    # speakerDict['1']
    
---------------------------------------------------------------------------

h-rm.tan 4oct2017

"""

import pandas as pd
import numpy as np
import json 

# from makeDFfromJson import makeDFfromJson
# DF0 = makeDFfromJson(ibm_out)
# DF0



def addTimeDiff_toDF(df): ## from df = makeDFfromJson(ibm_out)
    df['timeDiff']='0'

    for i in range(1, len(df)):
        df.loc[i, 'timeDiff'] = df.loc[i-1, 'to'] - df.loc[i, 'from']

    return df


def findTimeDiffIDX(df):
    TimeDiffIDX = df[df.timeDiff!=0].index.tolist()
    
    if (len(df)-1 in TimeDiffIDX) == True:
        TimeDiffIDX.extend([len(df)])
        
    return TimeDiffIDX


def get_SentenceNtofrom(df,TimeDiffIDX):
    
    AllSents=[]
    AllS=[]
    AllE=[]

    for i,idx in enumerate (range(1, len(TimeDiffIDX))) :
        #  print (i, idx)
        wdL = df.loc[TimeDiffIDX[idx-1]:TimeDiffIDX[idx]-1,'Wd_list'].tolist()
        sentence = ' '.join(wdL)
        AllSents.append(sentence)

        S, E = df.loc[TimeDiffIDX[idx-1],'from'] , df.loc[TimeDiffIDX[idx]-1,'to']
        AllS.extend([S])
        AllE.extend([E])

        #print(sentence,S,E)
        tofromSent_tmp = dict(zip(['from','to','sentences'],[AllS,AllE,AllSents]))
        tofromSent = pd.DataFrame(tofromSent_tmp, columns=['from','to','sentences'])

    return tofromSent


def get_SentenceInfo(df,TimeDiffIDX):

    dftmp=pd.DataFrame()

    for i,idx in enumerate (range(1, len(TimeDiffIDX))) :
        tmp = df.loc[TimeDiffIDX[idx-1]:TimeDiffIDX[idx]-1,
                      ['resultIDX','SentConf', 'SpkConf', 'final', 'speaker',  'timeDiff'] ].drop_duplicates(subset='speaker')
        #print(tmp)
        dftmp = pd.concat([dftmp,pd.DataFrame(tmp)])
    
    return dftmp


def getSpeakerDur(df):
    
    '''get individual speaker's total speech duration | normalize by all speakers combined speech duration'''
    
    df['Sdur'] = df[['from','to']].diff(axis=1).values[:,1]
    
    SpeakerDur = [] 
    speakerList = df.speaker.unique().tolist()
    for i in speakerList:
        SpeakerDur.extend( [df[df.speaker==i].Sdur.values.sum()] )
    
    SpeakerDur_norm = SpeakerDur/sum(SpeakerDur)
    
    return SpeakerDur_norm, df 



def get_SpeakerDict(df, SpeakerDur_norm):
    from collections import defaultdict

    speakerList = df.speaker.unique().tolist()

    speakerDict = defaultdict(lambda: defaultdict(int))

    for i in speakerList:
        speakerDict[str(i)] = {'sentences' : ' \n '.join(df[df.speaker==i].sentences.values.tolist()),
                              'duration' : SpeakerDur_norm[i]}

    # add other info in dict of dict: speakerDict['0']['dur'] = 10000

    return speakerDict



def make_SpeakerDict(df):
    from collections import defaultdict

    speakerList = df.speaker.unique().tolist()

    speakerDict = defaultdict(lambda: defaultdict(int))

    for i in speakerList:
        speakerDict[str(i)] = {'sentences' : ' \n '.join(df[df.speaker==i].sentences.values.tolist())}

    # add other info in dict of dict: speakerDict['0']['dur'] = 10000

    return speakerDict



### Uses All functions above 
def retrieve_SpeakerInfoAsDict(DF0): ## from DF0 = makeDFfromJson(ibm_out)
    

    DF1 = addTimeDiff_toDF(DF0) 

    TimeDiffIDX = findTimeDiffIDX(DF1)

    tofromSent = get_SentenceNtofrom(DF1,TimeDiffIDX)

    SentenceInfo = get_SentenceInfo(DF1,TimeDiffIDX)

    DF2 = pd.concat([SentenceInfo.reset_index(drop=True),tofromSent],axis=1)
    
    SpeakerDur_norm, DF2 = getSpeakerDur(DF2)
    
    ## speakerDict = make_SpeakerDict(DF2)
    
    speakerDict = get_SpeakerDict(DF2,SpeakerDur_norm)
    
    return speakerDict
