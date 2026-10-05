const paymentModel = require('../models/paymentModel');

async function financialReport(db) {
  return paymentModel.getFinancialReport(db);
}

module.exports = { financialReport };
