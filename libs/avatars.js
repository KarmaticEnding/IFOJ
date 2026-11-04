const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFile } = require('child_process');
const { promisify } = require('util');
const run = promisify(execFile);
const lock = new (require('async-lock'))();

function directory() {
  return syzoj.utils.resolvePath(syzoj.config.upload_dir, 'avatars');
}
function filename(id) {
  if (!/^[1-9]\d*$/.test(String(id)) || !Number.isSafeInteger(Number(id))) throw new Error('无效的用户编号。');
  return path.join(directory(), `${id}.png`);
}
exports.filename = filename;
exports.token = function (req) {
  if (!req.session.avatarToken) req.session.avatarToken = crypto.randomBytes(32).toString('hex');
  return req.session.avatarToken;
};
exports.validToken = function (req) {
  const token = req.get('X-Avatar-CSRF');
  return typeof token === 'string' && /^[a-f0-9]{64}$/.test(token) && typeof req.session.avatarToken === 'string' &&
    token.length === req.session.avatarToken.length &&
    crypto.timingSafeEqual(Buffer.from(token), Buffer.from(req.session.avatarToken));
};
exports.save = async function (id, buffer) {
  return lock.acquire('image-conversion', async () => {
    const target = filename(id);
    await fs.promises.mkdir(directory(), { recursive: true });
    const nonce = crypto.randomBytes(16).toString('hex');
    const input = path.join(directory(), `.input-${nonce}`);
    const output = path.join(directory(), `.output-${nonce}`);
    try {
      await fs.promises.writeFile(input, buffer, { flag: 'wx', mode: 0o600 });
      await run('python3', [path.join(__dirname, '../bin/normalize-avatar.py'), input, output],
        { timeout: 10000, maxBuffer: 4096 });
      await fs.promises.chmod(output, 0o600);
      await fs.promises.rename(output, target);
    } finally {
      for (const file of [input, output]) await fs.promises.unlink(file).catch(e => { if (e.code !== 'ENOENT') throw e; });
    }
  }, { maxPending: 4 });
};
