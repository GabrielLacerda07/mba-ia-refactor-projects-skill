function getActiveById(db, courseId) {
  return new Promise((resolve, reject) => {
    db.get(
      'SELECT * FROM courses WHERE id = ? AND active = 1',
      [courseId],
      (err, row) => {
        if (err) reject(err);
        else resolve(row || null);
      }
    );
  });
}

function getAll(db) {
  return new Promise((resolve, reject) => {
    db.all('SELECT * FROM courses', [], (err, rows) => {
      if (err) reject(err);
      else resolve(rows || []);
    });
  });
}

module.exports = { getActiveById, getAll };
