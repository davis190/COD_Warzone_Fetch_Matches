const fs = require('fs')

const dir = './matches/'
const files = fs.readdirSync(dir)
var matches = []
for (const file of files) {
    matchID = file.split('_')[0]
    matches.push(matchID)
    console.log(matchID)
}

//match_data = JSON.stringify(matches);
let file_name = 'match_list.csv'
fs.writeFileSync(file_name, matches);


var data = fs.readFileSync('match_list.csv')
    .toString() // convert Buffer to string
    .split('\n') // split string to lines
    .map(e => e.trim()) // remove white spaces for each line
    .map(e => e.split(',').map(e => e.trim())); // split each line to array

console.log(data);
console.log(JSON.stringify(data, '', 2)); // as json