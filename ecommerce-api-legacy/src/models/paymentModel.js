function create(db, enrollmentId, amount, status) {
  return new Promise((resolve, reject) => {
    db.run(
      'INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)',
      [enrollmentId, amount, status],
      function onInsert(err) {
        if (err) reject(err);
        else resolve(this.lastID);
      }
    );
  });
}

function writeAudit(db, action) {
  return new Promise((resolve, reject) => {
    db.run(
      "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
      [action],
      (err) => {
        if (err) reject(err);
        else resolve();
      }
    );
  });
}

function getFinancialReport(db) {
  return new Promise((resolve, reject) => {
    const sql = `
      SELECT
        c.id AS course_id,
        c.title AS course,
        u.name AS student,
        COALESCE(p.amount, 0) AS paid,
        p.status AS payment_status
      FROM courses c
      LEFT JOIN enrollments e ON e.course_id = c.id
      LEFT JOIN users u ON u.id = e.user_id
      LEFT JOIN payments p ON p.enrollment_id = e.id
      ORDER BY c.id, e.id
    `;

    db.all(sql, [], (err, rows) => {
      if (err) return reject(err);

      const byCourse = new Map();
      for (const row of rows) {
        if (!byCourse.has(row.course_id)) {
          byCourse.set(row.course_id, {
            course: row.course,
            revenue: 0,
            students: [],
          });
        }
        const courseData = byCourse.get(row.course_id);
        if (row.student) {
          courseData.students.push({
            student: row.student,
            paid: row.paid,
          });
          if (row.payment_status === 'PAID') {
            courseData.revenue += row.paid;
          }
        }
      }

      resolve(Array.from(byCourse.values()));
    });
  });
}

module.exports = { create, writeAudit, getFinancialReport };
