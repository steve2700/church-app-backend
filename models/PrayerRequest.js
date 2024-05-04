const mongoose = require('mongoose');

const prayerRequestSchema = new mongoose.Schema({
  title: {
    type: String,
  },
  content: {
    type: String,
    required: true,
  },
  submitter: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  category: {
    type: String,
  },
  isAnonymous: {
    type: Boolean,
    default: false,
  },
  answered: {
    type: Boolean,
    default: false,
  },
  prayerPoints: {
    type: [String],
  },
  comments: [
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Comment',
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

// Optional method to mark request as answered
prayerRequestSchema.methods.markAnswered = function () {
  this.answered = true;
  return this.save(); // Save the updated prayer request
};

module.exports = mongoose.model('PrayerRequest', prayerRequestSchema);

