'use strict';

// Discussion, posting and comment endpoints are not part of IFOJ.
app.all(['/discussion', '/discussion/*', '/article', '/article/*'], (req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    return res.status(404).json({ error: 'NOT_FOUND' });
  }
  return res.status(404).render('error', { err: new ErrorMessage('无此页面。') });
});
