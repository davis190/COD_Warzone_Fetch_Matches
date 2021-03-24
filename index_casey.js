const API = require('call-of-duty-api')({ platform: "battle" });
const moment = require('moment');
const fs = require('fs');
const inputs = require('./inputs.js')
const converter = require('json-2-csv');


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

// function login(){
//     try {
//         await API.login(inputs.activision_username, inputs.activision_password);
//         console.log("Login success")
//     } catch(Error) {
//         console.log("LOGIN ERROR")
//     }
// }
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
            console.log("Search for matches from", start, "to", end)
            for([key, val] of Object.entries(inputs.gamers)) {
                try{
                    console.log(key);
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
    // Update info for Dashboard - RUNS ON LAMBDA NOW
    //MWBattleData() // update file: MWBattleData/all_battle_data.json
    //MWweeklystats()// update file: MWBattleData/weekly_battle_data.json
}

async function MWBattleData() {
    try {
        await API.login(inputs.activision_username, inputs.activision_password);
        console.log("Login success")
    } catch(Error) {
        console.log("LOGIN ERROR")
    }

    //create all_battle_data file (current stats)
    var all_battle_data = []


    var nodes = [
    "Kelshaw#1225",
    "cdawg009",
    "badgers819",
    "beefSNAKE22#1201",
    "mooseattack90",
    "DirtyUndies#11373",
    "MkeBeers54"
    ]

    // var nodes = []
    // var lines = []
    
    // var dict = []

    for([key, val] of Object.entries(inputs.pewpers)) {
        try {
            //await sleep(1500);
            // nodes.push(key)
            await API.MWBattleData(gamertag=key, platform=val).then((data) => {
                console.log('Get MWBattleData for: ', key)

                let user_dict ={}
                user_dict[key] = data
                // console.log(user_dict)

                // dict["Items"].push({
                //     key:   key,
                //     value: data
                // });

                all_battle_data.push(user_dict)
            });
            // lines.push(data) 
        } catch(Error) {
            console.log(Error)
        }
    }

    all_battle_data = JSON.stringify(all_battle_data)

    let file_name = 'MWBattleData/all_battle_data.json' 
    

    fs.writeFileSync(file_name, all_battle_data);
    console.log(file_name)

    //console.log('list', all_battle_data)
}


async function MWweeklystats() {
    try {
        await API.login(inputs.activision_username, inputs.activision_password);
        console.log("Login success")
    } catch(Error) {
        console.log("LOGIN ERROR")
    }

    //create all_battle_data file (current stats)
    all_battle_data = []

    for([key, val] of Object.entries(inputs.pewpers)) {
        try {
            //await sleep(1500);
            // nodes.push(key)
            await API.MWweeklystats(gamertag=key, platform=val).then((data) => {
                console.log('Get MWweeklystats for: ', key)

                let user_dict ={}
                user_dict[key] = data

                all_battle_data.push(user_dict)
            });
            // lines.push(data) 
        } catch(Error) {
            console.log(Error)
        }
    }

    all_battle_data = JSON.stringify(all_battle_data)

    let file_name = 'MWBattleData/weekly_battle_data.json' 
    fs.writeFileSync(file_name, all_battle_data);
    console.log(file_name)
}
function test_loop(){
    let date_ob = new Date();

    d = date_ob.toLocaleString('en-US', { timeZone: 'America/Chicago' });
    console.log(d)
    // current date
    // adjust 0 before single digit date
    let date = ("0" + date_ob.getDate()).slice(-2);

    // current month
    let month = ("0" + (date_ob.getMonth() + 1)).slice(-2);

    // current year
    let year = date_ob.getFullYear();

    // current hours
    let hours = date_ob.getHours();

    // current minutes
    let minutes = date_ob.getMinutes();

    // prints date & time in YYYY-MM-DD HH:MM:SS format
    let timestamp = year + "-" + month + "-" + date + " " + hours + ":" + minutes

    console.log(timestamp);


}

data()
//test_loop()
//MWBattleData()
//MWweeklystats()


function round5(x)
{
    base = 0.005

    nearest_multiple = base * (x/base).toFixed(3)
    if (x >= 1) {
        x = x - 1
        z = 1
    }
    else{
        z = 0
    }
    y = x - x.toFixed(2)
    // if between .000 and .004
    if (y < .005){
        kd_up = (Math.ceil(x/base)*base) + z;
        kd_down = (Math.floor(x/base)*base) + z- base;
    }


    // if between .005 and .009
    if (y < 0){
        kd_up = (Math.ceil(x/base)*base) + z + base;
        kd_down = (Math.floor(x/base)*base) + z;
    }
    console.log(x, nearest_multiple, y)

    //unconfirmed
    // kd_down = (Math.floor(x/base)*base) + z;

    console.log('kd_up', kd_up, 'kd_down', kd_down)
    return ;
}

//round5(0.6113)