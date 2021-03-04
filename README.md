# CoD WarZone Game Data
This small nodejs application is used to fetch game data from every game played on warzone and drop it into a csv for easy/quick analysis.

Next iteration of this would probably be to drop the data into a database somewhere for easy querying.

## References
This uses the following NPM package to interact with the CoD APIs -> https://github.com/lierrmm/Node-CallOfDuty

## How to use
1) Clone the repo
2) Populate the inputs.js file (see below for help)
3) `npm install`
4) `node index.js`

Once the script is running it will store all data into a `data.csv`. It will log progress into a `log.log` file and if it encounters any error it will put those into `error.log`. 

### Errors
The only error that the script currently catches and inserts into `error.log` is if the API is not returning all games for a given interval. The CoD API will return a maximum of 20 matches for a given period. If you played 21 matches in the queried period then you will miss one.


## Inputs.js
First section are the credentials that you use to login to activision.com with. These will authenticate your API calls.
```
module.exports.activision_username = "my_email@gmail.com"
module.exports.activision_password = "##PASSWORD##"
```

Second section is the user information that you want to query and the platform they play on. A list of playforms can be found [here](https://lierrmm.github.io/capi-docs/#/?id=platforms)
```
module.exports.gamertag = "gammers_gonna_game"
module.exports.platform = "xbl"
```


Third section tell the script how many times it should loop and how large the query time frame is (in hours). The main thing to keep in mind here is that whatever time from you use you can't have more than 20 games in it or else it won't return every game.

Math is your friend when figuring these things out.

(hour_interval * query_loops) / 24 = number of days queried
    
Example:
    If you have played warzone for 1 year (365 days) and you want to use a 4 hour interval to make sure you don't miss anything then your query loops would be calculated as such.

    query_loops = 365 days * (24 hours in a day / 4 hour intervals) = 2190 query_loops

```
module.exports.hour_interval = 4
module.exports.query_loops = 2190
```

