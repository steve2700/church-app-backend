// models/User.js

const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true
  },
  email: {
    type: String,
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  },
  fullName: String,
  phoneNumber: {
    type: String,
    validate: {
      validator: function(v) {
        return /\d{4}/.test(v); // Validate format (4 digits)
      },
      message: props => `${props.value} is not a valid phone number!`
    },
    required: true,
    unique: true
  },
  profilePicUrl: String,
  shortBio: String,
  membershipStatus: String,
  ministryInvolvement: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Ministry' }], 
});

// Hash the password before saving it to the database
userSchema.pre('save', async function(next) {
  const user = this;
  if (user.isModified('password')) {
    user.password = await bcrypt.hash(user.password, 10);
  }
  next();
});

// Method to compare provided password with hashed password
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

const User = mongoose.model('User', userSchema);

module.exports = User;

