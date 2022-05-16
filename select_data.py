# Obtain data from looping over provided schools, select only those stating Primary or Secondary
#create data frame for storage

import pandas as pd
def select_data(li_tags, choice, school_data):

    for item in range(len(li_tags)):
        info=(li_tags[item].text).split('\n')
        category=info[1].split(':')[1].strip()
        if category==choice:
            if len(info)==6:
                rating=info[-3].split(':')[1].strip()
            elif len(info)==5:
                rating='NA'
            else: continue
            name=info[0]
            address=info[2]
            if len(info[-2].split(':'))<2:
                last_report='NA'
            else:
                last_report=info[-2].split(':')[1].strip()


            df_temp=pd.DataFrame({'name':[name], 'address':[address], 'rating':[rating], 'last_report':[last_report]})    
            school_data=pd.concat([school_data,df_temp], ignore_index=True, axis=0)
    return school_data