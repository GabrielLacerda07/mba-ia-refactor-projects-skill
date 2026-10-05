const userModel = require('../models/userModel');

async function deleteUser(db, userId) {
  await userModel.remove(db, userId);
  return {
    msg: 'Usuário deletado com matrículas e pagamentos associados removidos.',
  };
}

module.exports = { deleteUser };
