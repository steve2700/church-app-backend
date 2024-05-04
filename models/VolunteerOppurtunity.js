const mongoose = require('mongoose');

const volunteerOpportunitySchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  ministry: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Ministry', // Reference to a model representing the ministry associated with the opportunity
  },
  startDate: {
    type: Date,
    required: true,
  },
  endDate: {
    type: Date,
  },
  timeCommitment: {
    type: String,
    required: true,
  },
  skillsNeeded: {
    type: [String],
  },
  location: {
    type: String,
  },
  ageRequirement: {
    type: Number,
  },
  contactPerson: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User', // Reference to a User model representing the contact person for the opportunity
  },
  signupDeadline: {
    type: Date,
  },
  maximumVolunteers: {
    type: Number,
  },
  isActive: {
    type: Boolean,
    default: true,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
  },
});

const VolunteerOpportunity = mongoose.model('VolunteerOpportunity', volunteerOpportunitySchema);

module.exports = VolunteerOpportunity;

