// models/Admin.js

const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const adminSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  firstName: String,
  lastName: String,
  phoneNumber: { type: String, required: true },
  phoneVerificationCode: String, // Store verification code
  isPhoneVerified: { type: Boolean, default: false }, // Flag to indicate phone verification status
});

// Middleware to hash the password before saving
adminSchema.pre('save', async function(next) {
  const admin = this;
  if (!admin.isModified('password')) {
    return next();
  }
  try {
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(admin.password, salt);
    admin.password = hashedPassword;
    next();
  } catch (error) {
    next(error);
  }
});

// Method to compare passwords
adminSchema.methods.comparePassword = async function(candidatePassword) {
  try {
    return await bcrypt.compare(candidatePassword, this.password);
  } catch (error) {
    throw new Error(error);
  }
};

const Admin = mongoose.model('Admin', adminSchema);

module.exports = Admin;

