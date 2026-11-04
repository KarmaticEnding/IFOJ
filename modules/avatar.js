const fs = require('fs');
const avatar = require('../libs/avatars');
const User = syzoj.model('user');
const upload = require('multer')({
  storage: require('multer').memoryStorage(),
  limits: { fileSize: 2 * 1024 * 1024, files: 1, fields: 0, parts: 1 }
}).single('avatar');

app.get('/user/:id/avatar', async (req, res) => {
  try {
    const file = avatar.filename(req.params.id);
    if (!await User.findById(Number(req.params.id))) return res.sendStatus(404);
    res.set('Cache-Control', 'private, no-store');
    res.set('X-Content-Type-Options', 'nosniff');
    try {
      const image = await fs.promises.readFile(file);
      return res.type('png').send(image);
    } catch (e) {
      if (e.code !== 'ENOENT') throw e;
      return res.sendFile(syzoj.rootDir + '/assets/default-avatar.svg');
    }
  } catch (e) {
    syzoj.log(e);
    return res.sendStatus(404);
  }
});

app.post('/user/:id/avatar', async (req, res) => {
  res.set('Cache-Control', 'no-store');
  try {
    avatar.filename(req.params.id);
    const user = await User.findById(Number(req.params.id));
    if (!user) return res.status(404).json({ message: '无此用户。' });
    if (!await user.isAllowedEditBy(res.locals.user)) return res.status(403).json({ message: '您没有权限修改此头像。' });
    if (!avatar.validToken(req)) return res.status(403).json({ message: '页面已过期，请刷新后重试。' });
    upload(req, res, async err => {
      if (err) return res.status(400).json({ message: '请选择一张不超过 2MB 的头像图片。' });
      if (!req.file || !req.file.buffer.length) return res.status(400).json({ message: '请选择头像图片。' });
      try {
        await avatar.save(user.id, req.file.buffer);
        return res.json({ success: true, message: '头像已更新。', url: syzoj.utils.makeUrl(['user', user.id, 'avatar'], { v: Date.now() }) });
      } catch (e) {
        return res.status(400).json({ message: '上传失败：请使用有效的 JPG、PNG 或 WebP 图片，每边不超过 4096 像素；也可稍后重试。' });
      }
    });
  } catch (e) {
    syzoj.log(e);
    return res.status(400).json({ message: '无法更新头像，请刷新后重试。' });
  }
});
