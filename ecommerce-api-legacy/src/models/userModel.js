function getByEmail(db, email) {
  return new Promise((resolve, reject) => {
    db.get('SELECT id, name, email, pass FROM users WHERE email = ?', [email], (err, row) => {
      if (err) reject(err);
      else resolve(row || null);
    });
  });
}

function getById(db, id) {
  return new Promise((resolve, reject) => {
    db.get('SELECT id, name, email FROM users WHERE id = ?', [id], (err, row) => {
      if (err) reject(err);
      else resolve(row || null);
    });
  });
}

function create(db, { name, email, passwordHash }) {
  return new Promise((resolve, reject) => {
    db.run(
      'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
      [name, email, passwordHash],
      function onInsert(err) {
        if (err) reject(err);
        else resolve(this.lastID);
      }
    );
  });
}

function remove(db, id) {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      db.run(
        `DELETE FROM payments WHERE enrollment_id IN (
          SELECT id FROM enrollments WHERE user_id = ?
        )`,
        [id]
      );
      db.run('DELETE FROM enrollments WHERE user_id = ?', [id]);
      db.run('DELETE FROM users WHERE id = ?', [id], function onDelete(err) {
        if (err) reject(err);
        else resolve(this.changes);
      });
    });
  });
}

module.exports = { getByEmail, getById, create, remove };
