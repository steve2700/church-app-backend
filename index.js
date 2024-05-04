// index.js

const express = require('express');
const mongoose = require('mongoose');

// Require database configuration
require('./config/database');

const app = express();

// Other setup and middleware configurations

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

