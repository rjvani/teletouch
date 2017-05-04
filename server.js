var express = require("express");
var bodyParser = require("body-parser");
var mongodb = require("mongodb");
var ObjectID = mongodb.ObjectID;

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

app.get("/api/exchange", function(req, res) {
  db.collection(BEER_EXCHANGE).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
    } else {
      res.status(200).json(docs);
    }
  });
});

app.get("/api/newsletters", function(req, res) {
  db.collection(NEWS).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
    } else {
      res.status(200).json(docs);
    }
  });
});

app.get("/api/carnival", function(req, res) {
  db.collection(CARNIVAL).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
    } else {
      res.status(200).json(docs);
    }
  });
});

app.get("/api/fight", function(req, res) {
  db.collection(COMPETE).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
    } else {
      res.status(200).json(docs);
    }
  });
});

app.get("/api/caro_data", function(req, res) {
  db.collection(LANDING).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
    } else {
      res.status(200).json(docs);
    }
  });
});

app.get("/api/roster", function(req, res) {
  db.collection(ROSTER).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
    } else {
      res.status(200).json(docs);
    }
  });
});

app.get("/api/sweetheart", function(req, res) {
  db.collection(LSROSTER).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
    } else {
      res.status(200).json(docs);
    }
  });
});

app.get("/api/donations", function(req, res) {
  db.collection(DONATION).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
    } else {
      res.status(200).json(docs);
    }
  });
});

app.get("/api/active", function(req, res) {
  db.collection(ACTIVE).find({}).toArray(function(err, docs) {
    if (err) {
      handleError(res, err.message, "Failed to get contacts.");
    } else {
      res.status(200).json(docs);
    }
  });
});

app.get("/api/wake", function(req, res) {
  res.status(200).json({wake: true});
});

app.post("/api/exchange", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();

  if (!req.body.name || !req.body.state || !req.body.beer) {
    handleError(res, "Invalid user input", "Must provide all fields.", 400);
  }

  db.collection(BEER_EXCHANGE).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.post("/api/active", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();

  if (!req.body.first || !req.body.last) {
    handleError(res, "Invalid user input", "Must provide all fields.", 400);
  }

  db.collection(ACTIVE).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.post("/api/fight", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();
  newContact.wins = 0;
  newContact.losses = 0;
  newContact.cups = 0;
  newContact.mmr = 1500;
  newContact.password = Math.random().toString(36).slice(-5);

  if (!req.body.first || !req.body.last || !req.body.email) {
    handleError(res, "Invalid user input", "Must provide all fields.", 400);
    return;
  }

  app.mailer.send('email', {
    to: req.body.email, // REQUIRED. This can be a comma delimited string just like a normal email to field.
    subject: 'Welcome to Sigma Nu IPL, Password: '+newContact.password, // REQUIRED.
  }, function (err) {
    if (err) {
      // handle error
      console.log(err);
      return;
    }
  });

  db.collection(COMPETE).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.post("/api/auth", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();

  if (req.body.password !== PASSWORD) {
    handleError(res, "Invalid password.", "Invalid password.", 400);
    return;
  }

  db.collection(PASS_AUTH).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.post("/api/sweetheart", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();

  if (!req.body.first || !req.body.last || !req.body.lsds) {
    handleError(res, "Invalid user input", "Must provide all fields.", 400);
  }

  db.collection(LSROSTER).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.post("/api/carnival", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();

  if (!req.body.name || !req.body.email || !req.body.ds) {
    handleError(res, "Invalid user input", "Must provide all fields.", 400);
  }

  db.collection(CARNIVAL).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.post("/api/caro_data", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();

  if (!req.body.title || !req.body.photo || !req.body.photo_name) {
    handleError(res, "Invalid user input", "Must provide all fields.", 400);
  }

  db.collection(LANDING).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.post("/api/roster", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();

  if (!req.body.name || !req.body.ds) {
    handleError(res, "Invalid user input", "Must provide all fields.", 400);
  }

  db.collection(ROSTER).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.post("/api/donations", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();

  if (!req.body.first || !req.body.last || !req.body.donation) {
    handleError(res, "Invalid user input", "Must provide all fields.", 400);
  }

  db.collection(DONATION).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.post("/api/newsletters", function(req, res) {
  var newContact = req.body;
  newContact.createDate = new Date();

  if (!req.body.semester || !req.body.volume || !req.body.year || !req.body.link) {
    handleError(res, "Invalid user input", "Must provide all fields.", 400);
  }

  db.collection(NEWS).insertOne(newContact, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to create new contact.");
    } else {
      res.status(201).json(doc.ops[0]);
    }
  });
});

app.put("/api/donations/:id", function(req, res) {
  var updateDoc = req.body;
  delete updateDoc._id;

  db.collection(DONATION).updateOne({_id: new ObjectID(req.params.id)}, updateDoc, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to update contact");
    } else {
      updateDoc._id = req.params.id;
      res.status(200).json(updateDoc);
    }
  });
});

app.put("/api/active/:id", function(req, res) {
  var updateDoc = req.body;
  delete updateDoc._id;

  db.collection(ACTIVE).updateOne({_id: new ObjectID(req.params.id)}, updateDoc, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to update contact");
    } else {
      updateDoc._id = req.params.id;
      res.status(200).json(updateDoc);
    }
  });
});

app.put("/api/sweetheart/:id", function(req, res) {
  var updateDoc = req.body;
  delete updateDoc._id;

  db.collection(LSROSTER).updateOne({_id: new ObjectID(req.params.id)}, updateDoc, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to update contact");
    } else {
      updateDoc._id = req.params.id;
      res.status(200).json(updateDoc);
    }
  });
});

app.put("/api/newsletters/:id", function(req, res) {
  var updateDoc = req.body;
  delete updateDoc._id;

  db.collection(NEWS).updateOne({_id: new ObjectID(req.params.id)}, updateDoc, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to update contact");
    } else {
      updateDoc._id = req.params.id;
      res.status(200).json(updateDoc);
    }
  });
});

app.put("/api/caro_data/:id", function(req, res) {
  var updateDoc = req.body;
  delete updateDoc._id;

  db.collection(LANDING).updateOne({_id: new ObjectID(req.params.id)}, updateDoc, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to update contact");
    } else {
      updateDoc._id = req.params.id;
      res.status(200).json(updateDoc);
    }
  });
});

app.put("/api/fight/:id", function(req, res) {
  var updateDoc = req.body;
  delete updateDoc._id;

  db.collection(COMPETE).updateOne({_id: new ObjectID(req.params.id)}, updateDoc, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to update contact");
    } else {
      updateDoc._id = req.params.id;
      res.status(200).json(updateDoc);
    }
  });
});

/*  "/api/contacts/:id"
 *    GET: find contact by id
 *    PUT: update contact by id
 *    DELETE: deletes contact by id
 */
app.get("/api/auth/:id", function(req, res) {
  db.collection(PASS_AUTH).findOne({ _id: new ObjectID(req.params.id) }, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to get contact");
      return;
    } else {
      res.status(200).json(doc);
    }
  });
});

app.get("/api/fight/:password", function(req, res) {
  db.collection(COMPETE).findOne({ password: req.params.password }, function(err, doc) {
    if (err) {
      handleError(res, err.message, "Failed to get contact");
      return;
    } else {
      res.status(200).json(doc);
    }
  });
});

app.delete("/api/active/:id", function(req, res) {
  db.collection(ACTIVE).deleteOne({_id: new ObjectID(req.params.id)}, function(err, result) {
    if (err) {
      handleError(res, err.message, "Failed to delete contact");
    } else {
      res.status(200).json(req.params.id);
    }
  });
});

app.delete("/api/donations/:id", function(req, res) {
  db.collection(DONATION).deleteOne({_id: new ObjectID(req.params.id)}, function(err, result) {
    if (err) {
      handleError(res, err.message, "Failed to delete contact");
    } else {
      res.status(200).json(req.params.id);
    }
  });
});

app.delete("/api/newsletters/:id", function(req, res) {
  db.collection(NEWS).deleteOne({_id: new ObjectID(req.params.id)}, function(err, result) {
    if (err) {
      handleError(res, err.message, "Failed to delete contact");
    } else {
      res.status(200).json(req.params.id);
    }
  });
});

app.delete("/api/caro_data/:id", function(req, res) {
  db.collection(LANDING).deleteOne({_id: new ObjectID(req.params.id)}, function(err, result) {
    if (err) {
      handleError(res, err.message, "Failed to delete contact");
    } else {
      res.status(200).json(req.params.id);
    }
  });
});

app.delete("/api/sweetheart/:id", function(req, res) {
  db.collection(LSROSTER).deleteOne({_id: new ObjectID(req.params.id)}, function(err, result) {
    if (err) {
      handleError(res, err.message, "Failed to delete contact");
    } else {
      res.status(200).json(req.params.id);
    }
  });
});

app.delete("/api/fight/:id", function(req, res) {
  db.collection(COMPETE).deleteOne({_id: new ObjectID(req.params.id)}, function(err, result) {
    if (err) {
      handleError(res, err.message, "Failed to delete contact");
    } else {
      res.status(200).json(req.params.id);
    }
  });
});
