const mongoose = require('mongoose');

const forumPostSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
  },
  content: {
    type: String,
    required: true,
  },
  author: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
  },
  category: {
    type: String,
    required: true,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
  updatedAt: {
    type: Date,
  },
  parentPost: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'ForumPost',
  },
  upvotes: {
    type: Number,
    default: 0,
  },
  downvotes: {
    type: Number,
    default: 0,
  },
  comments: [
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Comment',
    },
  ],
  isApproved: {
    type: Boolean,
    default: true,
  },
  isDeleted: {
    type: Boolean,
    default: false,
  },
});

// Method to upvote a post
forumPostSchema.methods.upvote = function() {
  this.upvotes++;
  return this.save();
};

// Method to downvote a post
forumPostSchema.methods.downvote = function() {
  this.downvotes++;
  return this.save();
};

// Method to check if a user is authorized to edit the post
forumPostSchema.methods.isAuthorizedToEdit = function(currentUser, isAdminOrModerator) {
  // If the current user is the author, allow edit
  if (currentUser && currentUser._id.equals(this.author)) {
    return true;
  }

  // If the current user is an admin or moderator, allow edit
  if (isAdminOrModerator) {
    return true;
  }

  // Otherwise, not authorized to edit
  return false;
};

const ForumPost = mongoose.model('ForumPost', forumPostSchema);

module.exports = ForumPost;

