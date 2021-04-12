const express = require('express');
const path = require('path');
const http = require('http');
const app = express();

const port = process.env.PORT || '8000';

app.set('port', port);

app.use(express.static(path.join(__dirname, '../build')));

const server = http.createServer(app);
server.listen(port, () => {
    console.log(`Server running at port ${port}`);
});
