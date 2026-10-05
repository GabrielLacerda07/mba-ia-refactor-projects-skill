const config = require('../config/settings');
const { hashPassword } = require('../database');
const userModel = require('../models/userModel');
const courseModel = require('../models/courseModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');

function maskCard(cardNumber) {
  if (!cardNumber || cardNumber.length < 4) return '****';
  return `****${cardNumber.slice(-4)}`;
}

function processPayment(cardNumber) {
  console.log(
    `Processando cartão ${maskCard(cardNumber)} na chave ${config.paymentGatewayKey}`
  );
  return cardNumber.startsWith('4') ? 'PAID' : 'DENIED';
}

async function checkout(db, body) {
  const userName = body.usr;
  const email = body.eml;
  const password = body.pwd;
  const courseId = body.c_id;
  const cardNumber = body.card;

  if (!userName || !email || !courseId || !cardNumber) {
    const error = new Error('Bad Request');
    error.status = 400;
    throw error;
  }

  const course = await courseModel.getActiveById(db, courseId);
  if (!course) {
    const error = new Error('Curso não encontrado');
    error.status = 404;
    throw error;
  }

  let user = await userModel.getByEmail(db, email);
  let userId;

  if (!user) {
    const passwordHash = hashPassword(password || '123456');
    userId = await userModel.create(db, {
      name: userName,
      email,
      passwordHash,
    });
  } else {
    userId = user.id;
  }

  const status = processPayment(cardNumber);
  if (status === 'DENIED') {
    const error = new Error('Pagamento recusado');
    error.status = 400;
    throw error;
  }

  const enrollmentId = await enrollmentModel.create(db, userId, courseId);
  await paymentModel.create(db, enrollmentId, course.price, status);
  await paymentModel.writeAudit(db, `Checkout curso ${courseId} por ${userId}`);

  return { msg: 'Sucesso', enrollment_id: enrollmentId };
}

module.exports = { checkout };
