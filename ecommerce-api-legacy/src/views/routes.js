const checkoutController = require('../controllers/checkoutController');
const reportController = require('../controllers/reportController');
const userController = require('../controllers/userController');

function registerRoutes(app, db) {
  app.post('/api/checkout', async (req, res, next) => {
    try {
      const result = await checkoutController.checkout(db, req.body);
      res.status(200).json(result);
    } catch (err) {
      next(err);
    }
  });

  app.get('/api/admin/financial-report', async (req, res, next) => {
    try {
      const report = await reportController.financialReport(db);
      res.json(report);
    } catch (err) {
      next(err);
    }
  });

  app.delete('/api/users/:id', async (req, res, next) => {
    try {
      const result = await userController.deleteUser(db, req.params.id);
      res.send(result.msg);
    } catch (err) {
      next(err);
    }
  });
}

module.exports = { registerRoutes };
