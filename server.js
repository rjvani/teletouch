var express = require("express");
var bodyParser = require("body-parser");
var mongodb = require("mongodb");
var ObjectID = mongodb.ObjectID;

var RECORD = "recordings";
var IP_ADDR = "ip";

var app = require('express');

app.use(bodyParser.json({limit: '4096mb'}));
app.use(bodyParser.urlencoded({
  extended: true,
  limit: '4096mb'
}));

// Create a database variable outside of the database connection callback to reuse the connection pool in your app.
var db;

// Connect to the database before starting the application server.
mongodb.MongoClient.connect(process.env.MONGODB_URI, function (err, database) {
  if (err) {
    console.log(err);
    process.exit(1);
  }

  // Save database object from the callback for reuse.
  db = database;
  console.log("Database connection ready");

  // Initialize the app.
  var server = app.listen(8540, function () {
    var port = server.address().port;
    console.log("App now running on port", port);
  });
});

// CONTACTS API ROUTES BELOW

app.all('*', function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'accept, content-type, x-parse-application-id, x-parse-rest-api-key, x-parse-session-token');
     // intercept OPTIONS method
    if ('OPTIONS' == req.method) {
      res.sendStatus(200);
    }
    else {
      next();
    }
});

// Generic error handler used by all endpoints.
function handleError(res, reason, message, code) {
  res.status(code || 500).send(message);
}

/*  "/api/contacts"
 *    GET: finds all contacts
 *    POST: creates a new contact
 */

app.get("/api/recordings", function(req, res) {
  db.collection(RECORD).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
      return;
    } else {
      res.status(200).json(docs);
    }
  });
});

app.post("/api/recordings", function(req, res) {
  var recording = req.body;
  recording.createDate = new Date();

  db.collection(RECORD).insertOne(recording, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new recording.");
      return;
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.get("/api/address", function(req, res) {
  db.collection(IP_ADDR).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
      return;
    } else {
      res.status(200).json(docs);
    }
  });
});

app.post("/api/address", function(req, res) {
  var ip_addr = req.body;
  ip_addr.createDate = new Date();

  // Remove the old IP Address
  db.collection(IP_ADDR).remove({}, function(err){});

  db.collection(IP_ADDR).insertOne(ip_addr, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new recording.");
      return;
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});
