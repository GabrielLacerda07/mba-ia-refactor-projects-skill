const sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');

function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.scryptSync(password, salt, 64).toString('hex');
  return `${salt}:${hash}`;
}

function verifyPassword(password, stored) {
  if (!stored || !stored.includes(':')) {
    return stored === password;
  }
  const [salt, hash] = stored.split(':');
  const verify = crypto.scryptSync(password, salt, 64).toString('hex');
  if (hash.length !== verify.length) return false;
  return crypto.timingSafeEqual(Buffer.from(hash, 'hex'), Buffer.from(verify, 'hex'));
}

function createDatabase() {
  const db = new sqlite3.Database(':memory:');

  return new Promise((resolve, reject) => {
    db.serialize(() => {
      db.run('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, pass TEXT)');
      db.run('CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)');
      db.run('CREATE TABLE enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)');
      db.run('CREATE TABLE payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)');
      db.run('CREATE TABLE audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)');

      const adminPass = hashPassword('123');
      db.run(
        'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
        ['Leonan', 'leonan@fullcycle.com.br', adminPass]
      );
      db.run(
        'INSERT INTO courses (title, price, active) VALUES (?, ?, ?), (?, ?, ?)',
        ['Clean Architecture', 997.0, 1, 'Docker', 497.0, 1]
      );
      db.run('INSERT INTO enrollments (user_id, course_id) VALUES (1, 1)');
      db.run(
        "INSERT INTO payments (enrollment_id, amount, status) VALUES (1, 997.00, 'PAID')",
        (err) => {
          if (err) reject(err);
          else resolve(db);
        }
      );
    });
  });
}

module.exports = { createDatabase, hashPassword, verifyPassword };
