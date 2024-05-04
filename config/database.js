const mongoose = require('mongoose');
require('dotenv').config();

const connectionString = process.env.MONGODB_URI;

mongoose.connect(connectionString)
  .then(() => {
    console.log('Connected to the MongoDB database');
  })
  .catch((error) => {
    console.error('Database connection error:', error);
  });

