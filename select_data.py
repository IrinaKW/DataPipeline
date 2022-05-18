# Obtain data from looping over provided schools, select only those stating Primary or Secondary
#create data frame for storage
import json

def select_data(li_tags, outfile):

    for item in range(len(li_tags)):
        info=(li_tags[item].text).split('\n')
        name=info[0]
        category=info[1].split(':')[1].strip()
        address=info[2]
        try:
            last_report=info[-2].split(':')[1].strip()
        except IndexError:
            last_report='NA'
    
        if len(info)==6:
            rating=info[-3].split(':')[1].strip()
        elif len(info)==5:
            rating='NA'
        else: continue
        
        data_json=json.dumps({'name':[name], 'category':[category], 'address':[address], 'rating':[rating], 'last_report':[last_report]}, indent=4)  
        outfile.write(data_json)    