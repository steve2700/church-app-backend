// models/Donation.js

const mongoose = require('mongoose');
const nodemailer = require('nodemailer');

const donationSchema = new mongoose.Schema({
  donor: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  amount: { type: Number, required: true },
  currency: String,
  donationDate: { type: Date, default: Date.now },
  paymentMethod: String,
  designation: String,
  transactionFee: Number,
  memo: String,
  status: { type: String, default: 'Pending' },
  receiptSent: { type: Boolean, default: false },
  receipt: String // Store receipt content in database
});

// Method to generate a donation receipt document
donationSchema.methods.generateReceipt = function() {
  // Retrieve donation details
  const { donor, amount, currency, donationDate, paymentMethod, designation, transactionFee, memo, status, receiptSent } = this;

  // Construct receipt content
  const receiptContent = `
    Donation Receipt
    ----------------

    Donor: ${donor}
    Amount: ${amount} ${currency}
    Donation Date: ${donationDate.toDateString()}
    Payment Method: ${paymentMethod}
    Designation: ${designation || 'Not specified'}
    Transaction Fee: ${transactionFee || 'Not specified'}
    Memo: ${memo || 'None'}

    Status: ${status}
    Receipt Sent: ${receiptSent ? 'Yes' : 'No'}
  `;

  // Return receipt content
  return receiptContent;
};

// Method to send donation receipt via email
donationSchema.methods.sendReceiptByEmail = async function() {
  // Configure transporter
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: 'your_email@gmail.com',
      pass: 'your_email_password'
    }
  });

  // Generate receipt content
  const receiptContent = this.generateReceipt();

  // Send email
  await transporter.sendMail({
    from: 'your_email@gmail.com',
    to: this.donor.email, // Assuming donor has an 'email' field
    subject: 'Donation Receipt',
    text: receiptContent
  });

  console.log('Receipt sent successfully to ' + this.donor.email);

  // Update receiptSent flag
  this.receiptSent = true;
  await this.save();
};

const Donation = mongoose.model('Donation', donationSchema);

module.exports = Donation;

