const API = require('call-of-duty-api')({ platform: "battle" });
const moment = require('moment');
const fs = require('fs');
const inputs = require('./inputs.js')


function log(message) {
    fs.appendFile('log.log', message+"\r\n", function (err) {
        if (err) return console.log(err);
    });
}

function error(message) {
    fs.appendFile('error.log', message+"\r\n", function (err) {
        if (err) return console.log(err);
    });
}

function sleep(ms) {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
}   

async function data() {
    try {
        await API.login(inputs.activision_username, inputs.activision_password);
        console.log("Login success")
    } catch(Error) {
        console.log("LOGIN ERROR")
    }

    // let csv__header_data = "teamPlacement," +
    //     "kills," +
    //     "start," + 
    //     "end," +
    //     "mode," +
    //     "matchID\r\n"
    // fs.writeFile('data.csv', csv__header_data, function (err) {
    //     if (err) return console.log(err);
    // });
    // for([key, val] of Object.entries(inputs.gamers)) {
    //     console.log(key, val);
    // }
    var end_moment = moment()
    var hour_interval = inputs.hour_interval
    try{
        var match_list = JSON.parse(fs.readFileSync('./full_match_list.json'));
        console.log('MATCH_LIST FOUND')
    } catch{
        console.log('NO MATCH_LIST FOUND')
        var match_list = []
    }
    console.log(match_list.length)
    var run_match_list = []
    // LOOP THRU X AMOUNT OF QUERY LOOPS
    for (var x = 0; x <= inputs.query_loops; x++) {
        log("Looping on "+ x + " " + end_moment.toDate())
        var end = end_moment.valueOf()
        var start = end_moment.subtract(hour_interval, 'hours').valueOf();
        try {
            // LOOP THRU INPUTS.GAMERS
            for([key, val] of Object.entries(inputs.gamers)) {
                try{
                    console.log(key, val, start, end);
                    log(key)
                    // await sleep(1000);
                    await API.MWcombatwzdate(gamertag=key, start=start, end=end, platform=val).then((data) => {
                        try {
                            if (data['matches'].length == 20) {
                                error(end_moment.toDate())
                                error("########################### 20 match limit hit")
                            }
                            log("   "+data['matches'].length)
                        
                            for (var i = 0; i <= data['matches'].length; i++) {
                                try{
                                    console.log(data['matches'][i]["matchID"])
                                    //ADD UNIQUE MATCHES TO MATCH_LIST
                                    if (!match_list.includes(data['matches'][i]["matchID"])){
                                        match_list.push(data['matches'][i]["matchID"]);
                                        run_match_list.push(data['matches'][i]["matchID"]);
                                    }
                                } catch {
                                    // console.log("miss")
                                }
                                // try {
                                //     let csv_data = data['matches'][i]["playerStats"]["teamPlacement"] + "," +
                                //         data['matches'][i]["playerStats"]["kills"] + "," +
                                //         moment.unix(data['matches'][i]["utcStartSeconds"]).toDate()  + "," +
                                //         moment.unix(data['matches'][i]["utcEndSeconds"]).toDate() + "," +
                                //         data['matches'][i]["mode"] + "," +
                                //         data['matches'][i]["matchID"] + "x\r\n"
                                //     fs.appendFile('match_data.csv', csv_data, function (err) {
                                //         if (err) return console.log(err);
                                //     });

                                //     // Match Detail Files
                                //     let match_data = JSON.stringify(data['matches'][i]);
                                //     let id = data['matches'][i]["matchID"]
                                //     //MWcombatwzdate version
                                //     let file_name = 'matches/' + id + '_match.json'
                                //     fs.writeFileSync(file_name, match_data);
                                // } catch {
                                //     // console.log("miss")
                                // }
                            }
                        } catch {
                            log("   No matches")
                        }
                    });
                } catch(Error){
                    console.log(Error)
                }   
            }
        } catch(Error) {
            console.log(Error)
        }
    }
    console.log('MATCH LIST COUNT FOR ALL USERS:')
    console.log(match_list.length)
    console.log(match_list)
    console.log('RUN_MATCH LIST COUNT FOR ALL USERS:')
    console.log(run_match_list.length)
    console.log(run_match_list)
    // SAVE MATCH_LIST TO FILE
    let j_list = JSON.stringify(match_list)
    fs.writeFileSync('full_match_list.json', j_list)

    // Create Files for every new found Match
    for (var x = 0; x <= run_match_list.length; x++) {
        try {
            await API.MWFullMatchInfowz(match_list[x], platform=inputs.platform).then((data) => {
                //console.log(data)
                //  Match Detail Files
                // MWfullcombatwzdate version
                let match_data = JSON.stringify(data);
                let file_name = 'all_matches/' + match_list[x] + '.json'
                fs.writeFileSync(file_name, match_data);
            });
        } catch(Error) {
            console.log(Error)
        }
    }

}

data()