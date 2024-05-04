const mongoose = require('mongoose');

const sermonSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
  },
  speaker: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  series: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Sermon', // Reference to another Sermon model if part of a series
  },
  preachingDate: {
    type: Date,
    required: true,
  },
  content: {
    type: String, // Content of the sermon (text, HTML, or reference to uploaded media)
    required: true,
  },
  description: {
    type: String,
  },
  bibleReference: {
    type: String,
  },
  audioFile: {
    type: String, // Reference to the uploaded audio file of the sermon (optional)
  },
  videoFile: {
    type: String, // Reference to the uploaded video file of the sermon (optional)
  },
  transcript: {
    type: String, // Text transcript of the sermon audio/video (optional)
  },
  slides: {
    type: String, // Reference to uploaded sermon slides (optional)
  },
  tags: {
    type: [String],
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
  },
});

const Sermon = mongoose.model('Sermon', sermonSchema);

module.exports = Sermon;

