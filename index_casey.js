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
    var end_moment = moment()
    var day_interval = inputs.day_interval
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
    for (var x = 0; x < inputs.query_loops; x++) {
        log("Looping on "+ x + " " + end_moment.toDate())
        var end = end_moment.valueOf()
        var start = end_moment.subtract(day_interval, 'days').valueOf();
        try {
            // LOOP THRU INPUTS.GAMERS
            for([key, val] of Object.entries(inputs.gamers)) {
                try{
                    console.log(key, 'start:', start, 'end:',end);
                    log(key)
                    await sleep(1500);
                    await API.MWfullcombatwzdate(gamertag=key, start=start, end=end, platform=val).then((data) => {
                        try {
                            console.log('Matches found: ', data.length)
                            for (var i = 0; i <= data.length; i++) {
                                try{
                                    //console.log(data[i]['matchId'])
                                    //ADD UNIQUE MATCHES TO MATCH_LIST
                                    if (!match_list.includes(data[i]['matchId'])){
                                        match_list.push(data[i]['matchId']);
                                        run_match_list.push(data[i]['matchId']);
                                    }
                                } catch {
                                    // console.log("miss")
                                }
                                //end = data[i]['timestamp']
                            }
                            //console.log('end',end)
                            let r_list = JSON.stringify(run_match_list)
                            fs.writeFileSync('run_match_list.json', r_list)
                            
                        } catch {
                            log("   No matches")
                        }
                    });
                } catch(Error){
                    console.log(Error)
                    log(Error)
                }   
            }
        } catch(Error) {
            console.log(Error)
        }
    }
    console.log('MATCH LIST COUNT FOR ALL USERS:')
    console.log(match_list.length)
    //console.log(match_list)
    console.log('RUN_MATCH LIST COUNT FOR ALL USERS:')
    console.log(run_match_list.length)
    console.log(run_match_list)
    // SAVE MATCH_LIST TO FILE
    let j_list = JSON.stringify(match_list)
    fs.writeFileSync('full_match_list.json', j_list)

    // Create Files for every new found Match
    for (var x = 0; x <= run_match_list.length; x++) {
        try {
            //await sleep(1500);
            await API.MWFullMatchInfowz(run_match_list[x], platform=inputs.platform).then((data) => {
                //console.log(data)
                //  Match Detail Files
                let match_data = JSON.stringify(data);
                let file_name = 'all_matches/' + run_match_list[x] + '.json'
                fs.writeFileSync(file_name, match_data);
                console.log(file_name)
            });
        } catch(Error) {
            console.log(Error)
        }
    }

}

async function data2() {
    try {
        await API.login(inputs.activision_username, inputs.activision_password);
        console.log("Login success")
    } catch(Error) {
        console.log("LOGIN ERROR")
    }

    var d = [
        {
          platform: 'battle',
          title: 'mw',
          timestamp: 1614743802000,
          type: '6552125305277136',
          matchId: '9169489683060559581',
          map: '3227376819739457'
        },
        {
          platform: 'battle',
          title: 'mw',
          timestamp: 1614742828000,
          type: '6552125305277136',
          matchId: '17662233243740431819',
          map: '3227376819739457'
        }
    ]
    var end_moment = moment()
    var day_interval = inputs.day_interval
    for([key, val] of Object.entries(inputs.gamers)) {
        try{
            console.log(key, val);
            log(key)
            await API.MWfullcombatwzdate(gamertag=key, start=0, end=0, platform=val).then((data) => {

                // console.log("   "+data['matches'].length)
                // log("   "+data['matches'].length)
            });
            await sleep(1500);
        } catch(Error){
            console.log(Error)
            log(Error)
        }
    }
}


async function test() {
    var d = [
        {
          platform: 'battle',
          title: 'mw',
          timestamp: 1614743802000,
          type: '6552125305277136',
          matchId: '9169489683060559581',
          map: '3227376819739457'
        },
        {
          platform: 'battle',
          title: 'mw',
          timestamp: 1614742828000,
          type: '6552125305277136',
          matchId: '17662233243740431819',
          map: '3227376819739457'
        }
    ]

    for (var x = 0; x < d.length; x++){
        console.log('-----------',x)
        console.log(d[x]['matchId'])
    }

}
data()