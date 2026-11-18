const fs = require("fs");

// Create and write a file
fs.writeFileSync(
    "notes.txt",
    "Learning Node.js and Express.js"
);

// Read the file
const data = fs.readFileSync(
    "notes.txt",
    "utf8"
);

console.log(data);

// Append additional content
fs.appendFileSync(
    "notes.txt",
    "\nLearning Node modules"
);

// Read updated content
console.log(fs.readFileSync("notes.txt", "utf8"));