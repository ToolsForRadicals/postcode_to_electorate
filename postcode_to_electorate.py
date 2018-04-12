import pandas as pd
import requests
frame = pd.read_csv('https://raw.githubusercontent.com/ToolsForRadicals/postcode_to_electorate/master/australian_postcodes.csv')
apikey = "YOUR OPENAUSTRALIA API KEY GOES HERE"
from multiprocessing.dummy import Pool
pool = Pool(4)

def getelectorates(postcode):
    pair = dict()
    pair['postcode'] = postcode
    pair['electorates'] = ""
    url = "http://www.openaustralia.org/api/getDivisions?postcode={}&key={}".format(postcode,apikey)
    api_result = requests.get(url)
    if 'error' not in str(api_result.content):
        json_result = api_result.json()
        if len(json_result) == 1:
            pair['electorates'] = json_result[0]['name']
            return pair
        else:
            pair['electorates'] = [result['name'] for result in json_result]
    return pair

    postcodes = list(set(frame['postcode']))

shortcodes = [code for code in postcodes if 2000 <= code <= 8000]
electorates = pool.map(getelectorates,shortcodes)
pool.join()
pool.close()
postframe = pd.DataFrame(electorates)
postframe.to_csv('postcode_to_electorate.csv')
