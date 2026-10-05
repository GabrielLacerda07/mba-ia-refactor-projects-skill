function errorHandler(err, req, res, next) {
  const status = err.status || 500;
  const message = err.message || 'Erro interno';
  if (status >= 500) {
    console.error(err);
  }
  if (req.accepts('json') && req.path.startsWith('/api/')) {
    return res.status(status).json({ erro: message });
  }
  return res.status(status).send(message);
}

module.exports = { errorHandler };
