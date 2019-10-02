var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
});

io.on('connection', function(socket){
  socket.on('move', function(msg){
    io.emit('move', msg);

    console.log('commamnd sent : ' + msg);
  });
});

http.listen(3001, function(){
  console.log('listening on *:3001');
});