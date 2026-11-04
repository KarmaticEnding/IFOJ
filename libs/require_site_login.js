// Only the home page and login page are public dynamic pages.
// Static assets are served before session middleware in app.js.
module.exports = function requireSiteLogin(req, res, next) {
  if (res.locals.user ||
      ((req.method === 'GET' || req.method === 'HEAD') && (req.path === '/' || req.path === '/login')) ||
      (req.method === 'POST' && req.path === '/api/login')) return next();

  res.set('Cache-Control', 'no-store');
  if (req.path.startsWith('/api/') || (req.method !== 'GET' && req.method !== 'HEAD')) {
    return res.status(401).json({ success: false, error: 'LOGIN_REQUIRED', message: '请登录后继续。' });
  }
  return res.status(403).render('error', {
    err: new ErrorMessage('请登录后继续。', {
      '登录': syzoj.utils.makeUrl(['login'], { url: req.originalUrl })
    })
  });
};
