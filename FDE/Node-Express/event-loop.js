console.log("1. Start");

setTimeout(() => {
    console.log("2. Timer");
}, 0);

Promise.resolve().then(() => {
    console.log("3. Promise");
});

console.log("4. End");