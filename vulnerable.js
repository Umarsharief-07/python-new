const express = require("express");
const mysql = require("mysql");
const crypto = require("crypto");
const jwt = require("jsonwebtoken");

const app = express();
app.use(express.json());

// ❌ Hardcoded secret key - Security vulnerability
const SECRET_KEY = "mysecretpassword";
const DB_PASSWORD = "root123"; // ❌ Hardcoded DB password

// ❌ Insecure database connection
const db = mysql.createConnection({
    host: "localhost",
    user: "admin",
    password: DB_PASSWORD, 
    database: "users",
});

db.connect(err => {
    if (err) console.log("Database Connection Failed!");
});

// ❌ SQL Injection Vulnerability
app.post("/login", (req, res) => {
    const { username, password } = req.body;
    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    
    db.query(query, (err, result) => {
        if (err) {
            res.status(500).json({ error: "Internal Server Error" });
        } else if (result.length > 0) {
            res.json({ message: "Login Successful", token: generateToken(username) });
        } else {
            res.status(401).json({ error: "Invalid Credentials" });
        }
    });
});

// ❌ Insecure password hashing - MD5 is weak
function hashPassword(password) {
    return crypto.createHash("md5").update(password).digest("hex");
}

// ❌ Insecure JWT token generation
function generateToken(username) {
    return jwt.sign({ user: username }, SECRET_KEY, { expiresIn: "9999y" }); // ❌ Extremely long expiry
}

// ❌ Insecure eval() usage
app.post("/execute", (req, res) => {
    const { code } = req.body;
    try {
        const result = eval(code); // ❌ Remote Code Execution (RCE) vulnerability
        res.json({ output: result });
    } catch (err) {
        res.status(500).json({ error: "Execution Failed" });
    }
});

// ❌ Memory Leak - Unstoppable interval
setInterval(() => {
    console.log("Memory Leak Running...");
}, 1000);

// ❌ Denial of Service - Infinite loop
app.get("/infinite-loop", (req, res) => {
    while (true) {} // ❌ Blocks event loop
});

// ❌ Sensitive Data Exposure - Logs user passwords
app.post("/signup", (req, res) => {
    console.log("User signed up with password:", req.body.password); // ❌ Should not log passwords
    res.json({ message: "User signed up" });
});

// ❌ Cross-Site Scripting (XSS) - Directly returns user input
app.get("/xss", (req, res) => {
    res.send(`<h1>Welcome ${req.query.name}</h1>`); // ❌ No input sanitization
});

app.listen(3000, () => {
    console.log("Server is running on port 3000");
});
