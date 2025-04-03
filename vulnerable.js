// A Node.js application with 100+ bugs, code smells, and issues

const express = require("express");
const mysql = require("mysql");
const fs = require("fs");
const app = express();
const port = 3000;

// Database connection (SQL injection vulnerability)
const connection = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "password",
    database: "test"
});
connection.connect();

// Memory leak: Unnecessary event listeners
app.on("request", (req, res) => {
    console.log("Request received");
});

// Unhandled promise rejection
async function fetchData() {
    let result = await connection.query("SELECT * FROM users");
    console.log(result);
}
fetchData();

// Undefined variable usage
function brokenFunction() {
    console.log(notDefinedVar);
}
brokenFunction();

// Infinite loop
function infiniteLoop() {
    let i = 0;
    while (i < 1) {
        console.log("Looping forever!");
    }
}
infiniteLoop();

// Incorrect API response (returning undefined)
app.get("/bad-response", (req, res) => {
    let data;
    res.send(data);
});

// Improper error handling
app.get("/error", (req, res) => {
    try {
        let x = y; // y is undefined
    } catch {
        console.log("Error occurred but not handled properly");
    }
});

// Blocking the event loop (Synchronous file read in request handler)
app.get("/block", (req, res) => {
    let data = fs.readFileSync("largefile.txt");
    res.send(data);
});

// Hardcoded credentials
const apiKey = "12345-ABCDE";

// Open port for incoming connections (Security risk)
app.listen(port, "0.0.0.0", () => {
    console.log(`Server running on port ${port}`);
});
