const path = require("path");

const filePath = "C:/Users/Abhiram/project/app.js";

console.log(path.basename(filePath));

console.log(path.dirname(filePath));

console.log(path.extname(filePath));

console.log(path.join("users", "documents", "file.txt"));

console.log(path.resolve("app.js"));
