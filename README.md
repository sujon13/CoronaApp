# CoronaApp
It is corona virus information related app. It has rest endpint to get corona virus info 

## How to use endpoint from front end ##
Base url: https://covid-19-info-bd.herokuapp.com

#### Endpoint ####
```GET https://covid-19-info-bd.herokuapp.com/api/v1/corona_stats/(day)/```
Example: ```https://covid-19-info-bd.herokuapp.com/api/v1/corona_stats/today/``` 
You can also use yesterday in place of day

#### Response ####
```
Response code [200 OK,...]
[
    {
        "serial": 24,
        "country": "Bangladesh",
        "total cases": 32078,
        "new cases": 1873,
        "total deaths": 452,
        "new deaths": 20,
        "total recovered": 6486,
        "active cases": 25140,
        "serious/ critical": 1,
        "total cases/1M": 195,
        "deaths/1M": 3,
        "total tests": 234675,
        "test/1M population": 1427,
        "population": 164510959,
        "region": "Asia"
    },
    ...
]
```
