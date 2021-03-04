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

async function data() {
    try {
        await API.login(inputs.activision_username, inputs.activision_password);
        console.log("Login success")
    } catch(Error) {
        console.log("LOGIN ERROR")
    }

    let csv__header_data = "teamPlacement," +
        "kills," +
        "start," + 
        "end," +
        "mode," +
        "matchID\r\n"
    fs.writeFile('data.csv', csv__header_data, function (err) {
        if (err) return console.log(err);
    });

    var end_moment = moment()
    var hour_interval = inputs.hour_interval
    for (var x = 0; x <= inputs.query_loops; x++) {
        log("Looping on "+ x + " " + end_moment.toDate())
        var end = end_moment.valueOf()
        var start = end_moment.subtract(hour_interval, 'hours').valueOf();
        try {
            await API.MWcombatwzdate(inputs.gamertag, start=start, end=end, platform=inputs.platform).then((data) => {
                try {
                    if (data['matches'].length == 20) {
                        error(end_moment.toDate())
                        error("########################### 20 match limit hit")
                    }
                    log("   "+data['matches'].length)
                
                    for (var i = 0; i <= data['matches'].length; i++) {
                        try {
                            let csv_data = data['matches'][i]["playerStats"]["teamPlacement"] + "," +
                                data['matches'][i]["playerStats"]["kills"] + "," +
                                moment.unix(data['matches'][i]["utcStartSeconds"]).toDate()  + "," +
                                moment.unix(data['matches'][i]["utcEndSeconds"]).toDate() + "," +
                                data['matches'][i]["mode"] + "," +
                                data['matches'][i]["matchID"] + "x\r\n"
                            fs.appendFile('data.csv', csv_data, function (err) {
                                if (err) return console.log(err);
                            });
                        } catch {
                            // console.log("miss")
                        }
                    }
                } catch {
                    log("   No matches")
                }
                
            });
        } catch(Error) {
            console.log(Error)
        }
    }

}

data()