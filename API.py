import pandas as pd
import requests
import json
from entsoe import EntsoePandasClient

#%%%###API#############
def EPIAS_API():
    down = './test.json'
    # you must download postman for api key and should analyze EXIST API documentation which data you want to take
    url = 'https://seffaflik.epias.com.tr/transparency/service/market/day-ahead-mcp?endDate=2019-12-31&startDate=2017-01-01'
    outpath=down
    generatedURL=url
    response = requests.get(generatedURL)
    if response.status_code == 200:
        with open(outpath, "wb") as out:
            for chunk in response.iter_content(chunk_size=128):
                out.write(chunk)
    with open(down) as json_file:
        data = json.load(json_file)
    body=data.get('body')
    gen=body.get('dayAheadMCPList')
    df=pd.DataFrame(gen)
    return(df)

#%%#############ENTSOE-API####################
def ENTSOE_API():
    client = EntsoePandasClient(api_key="------------------") # Sign up to ENTSO-E and contact ENTSO-E help center for api key.

    country_code = 'EE', 'PT', 'ES', 'FR', 'FI', 'HU', 'SI', 'LV', 'NL', 'GR', 'BE'

    start = [pd.Timestamp('2016-12-31T22:00Z'), pd.Timestamp('2016-12-31T23:00Z'), pd.Timestamp('2016-12-31T23:00Z'), pd.Timestamp('2016-12-31T23:00Z'), pd.Timestamp('2016-12-31T22:00Z'), pd.Timestamp('2016-12-31T23:00Z'), pd.Timestamp('2016-12-31T23:00Z'), pd.Timestamp('2016-12-31T22:00Z'), pd.Timestamp('2016-12-31T23:00Z'), pd.Timestamp('2016-12-31T22:00Z'), pd.Timestamp('2016-12-31T23:00Z')]
    end= [pd.Timestamp('2019-12-31T21:00Z'), pd.Timestamp('2019-12-31T22:00Z'), pd.Timestamp('2019-12-31T22:00Z'), pd.Timestamp('2019-12-31T22:00Z'), pd.Timestamp('2019-12-31T21:00Z'), pd.Timestamp('2019-12-31T23:00Z'), pd.Timestamp('2019-12-31T23:00Z'), pd.Timestamp('2019-12-31T21:00Z'), pd.Timestamp('2019-12-31T23:00Z'), pd.Timestamp('2019-12-31T21:00Z'), pd.Timestamp('2019-12-31T22:00Z')]

    df1=[]
    iteration2=0
    ElectricityPrice=[]
    for iiii in range(len(country_code)):
        ElectricityPrice=client.query_day_ahead_prices(country_code[iteration2], start=start[iteration2], end=end[iteration2])
        if iiii==0:
            df1=pd.DataFrame({country_code[iteration2]:ElectricityPrice.values})
            iteration2=iteration2+1
            print(df1)
        else:
            df1[country_code[iteration2]]=pd.DataFrame({country_code[iteration2]:ElectricityPrice.values})
            iteration2=iteration2+1
            print(df1)
    return(df1)

df = ENTSOE_API()
df1 = EPIAS_API()

countrycode = 'TR'
df[countrycode]=pd.DataFrame({countrycode:df1['priceEur'].values})



