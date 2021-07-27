#!/usr/bin/env node

let port = process.env.NLP_WS_PORT || 3000;
var http = require('http'),
    fs = require('fs'),
    index = fs.readFileSync(__dirname + '/index.html');

var app = http.createServer(function (req, res) {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(index);
});


var io = require('socket.io')(app, {cors: {
    origin: "*",
    methods: ["GET", "POST"]
}});

io.on('connection', function (socket) {
    socket.emit('connected', { message: 'Welcome!', id: socket.id });
});
var readline = require('readline');
var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

rl.on('line', function (line) {
    io.emit('data', { line: line });
})
app.listen(port);




