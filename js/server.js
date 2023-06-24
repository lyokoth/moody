/** express script */
var express = require('express');
var app = express();
app.use(express.static(__dirname + '/public'));
console.log('Listening on 6543')
app.listen(6543);

