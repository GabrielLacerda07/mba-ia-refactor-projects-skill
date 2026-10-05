const path = require('path');

module.exports = {
  port: Number(process.env.PORT) || 3000,
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || 'dev-payment-key',
  smtpUser: process.env.SMTP_USER || 'no-reply@example.com',
  dbUser: process.env.DB_USER || 'dev',
  dbPass: process.env.DB_PASS || 'dev',
};
