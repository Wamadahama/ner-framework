const fs = require("fs")
let dir = "US State Department"

let filenames = [
    "documents.json",
    "entities.json",
].map((filename) => {
    return dir + "/" + filename
});

let json = filenames.reduce(function (accumulator, current_file) {
    let file_content = fs.readFileSync(current_file);
    accumulator.push(JSON.parse(file_content))
    return accumulator
}, []);

let documents = json[0]
let entities = json[1]

console.log(documents[0])
console.log(entities[0])
