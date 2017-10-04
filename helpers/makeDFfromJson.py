
# coding: utf-8

def makeDFfromJson(ibm_out):
    '''
        Reformat Json output from IBM API call via Speech Recognition with relevant parameters as a pandaDataFrame
        
    '''

    DFtmp_spkInfo = pd.DataFrame.from_dict(ibm_out['speaker_labels'])
    DFtmp_spkInfo = DFtmp_spkInfo.rename(columns = {'confidence':'SpkConf'})

    r_list=[]
    Wd_list=[]
    Sconf_list=[]

    for i,r in enumerate (ibm_out['results']):
        
        Wd_list.extend(r['alternatives'][0]['transcript'].split())
        n_wds = len(r['alternatives'][0]['transcript'].split())

        Sconf_list.extend( np.repeat(r['alternatives'][0]['confidence'],n_wds) )

        r_list.extend( np.repeat(i,n_wds) )


    DFtmp_wdSconf = pd.DataFrame([r_list, Wd_list,Sconf_list], index=['resultIDX','Wd_list','SentConf']).T

    DF = pd.concat([DFtmp_wdSconf, DFtmp_spkInfo], axis=1)
    
    return DF
