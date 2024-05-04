const mongoose = require('mongoose');

const ministrySchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  description: {
    type: String,
  },
  leader: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User', // Reference to your User model
  },
  contactEmail: {
    type: String,
  },
  website: {
    type: String,
  },
  meetingTime: {
    type: String, // Optional: Specify meeting day and time (e.g., " Tuesdays at 7pm")
  },
  meetingLocation: {
    type: String, // Optional: Physical or virtual location of meetings
  },
  vision: {
    type: String, // Optional: Describe the ministry's vision or goals
  },
  areasOfFocus: {
    type: [String], // Optional: List areas the ministry focuses on (e.g., "Youth", "Missions")
  },
  targetAudience: {
    type: String,
    enum: ['Children', 'Youth', 'Young Adults', 'Families', 'Adults', 'Seniors', 'Other'], // Include "Youth" and "Other"
  },
  isSundaySchool: {
    type: Boolean,
    default: false,
  },
  // Additional fields specific to Sunday School (optional)
  ageGroups: {
    type: [String], //  e.g., ["Toddlers", "Preschool", "Elementary"]
  },
  curriculum: {
    type: String, // Reference or description of the curriculum used
  },
  volunteerOpportunities: [
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'VolunteerOpportunity', // Reference to your VolunteerOpportunity model
    },
  ],
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
  },
});

module.exports = mongoose

