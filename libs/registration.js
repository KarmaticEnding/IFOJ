'use strict';

// Keep all account creation routes, including old verification links, under one policy.
module.exports = function requireRegistration(req, res, next) {
  if (syzoj.config.allow_registration === true) return next();

  const message = '本站不开放注册，请联系管理员获取账号。';
  res.status(403);
  if (req.path.startsWith('/api/')) {
    return res.json({ error_code: 2011, message });
  }
  return res.render('error', { err: new ErrorMessage(message) });
};
