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


    var match_list = fs.readFileSync('match_list.csv')
        .toString() // convert Buffer to string
        .split('\n') // split string to lines
        .map(e => e.trim()) // remove white spaces for each line
        .map(e => e.split(',').map(e => e.trim())); // split each line to array


    //console.log(match_list);
    console.log("MATCH COUNT", match_list[0].length);

    for (var x = 0; x <= match_list[0].length; x++) {
        try {
            await API.MWFullMatchInfowz(match_list[0][x], platform=inputs.platform).then((data) => {
                //console.log(data)
                //  Match Detail Files
                // MWfullcombatwzdate version
                let match_data = JSON.stringify(data);
                let file_name = 'full_matches/' + match_list[0][x] + '.json'
                fs.writeFileSync(file_name, match_data);
            });
        } catch(Error) {
            console.log(Error)
        }
    }
}
data()