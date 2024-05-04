// models/Event.js

const mongoose = require('mongoose');

const eventSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  description: String,
  startDate: {
    type: Date,
    required: true
  },
  endDate: Date,
  location: String,
  category: String,
  speaker: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  imageUrl: String,
  registrationLink: String,
  cost: Number,
  isPublic: {
    type: Boolean,
    default: true
  },
  organizers: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

const Event = mongoose.model('Event', eventSchema);

module.exports = Event;

