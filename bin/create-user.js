#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const readline = require('readline');
const { Writable } = require('stream');
const mysql = require('mysql2/promise');

function loadConfig() {
  const defaults = require('../config-example.json');
  const file = path.resolve(__dirname, '../config.json');
  const custom = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : {};
  return {
    ...defaults,
    ...custom,
    db: { ...defaults.db, ...custom.db },
    default: { user: { ...defaults.default.user, ...(custom.default && custom.default.user) } }
  };
}

async function createUser({ username, password, email = null, isAdmin = false }) {
  const config = loadConfig();
  if (typeof username !== 'string' || username.length > 80 || !new RegExp(config.username_regex).test(username)) {
    throw new Error('用户名不合法，请使用字母、数字、下划线或连字符。');
  }
  if (typeof password !== 'string' || !password.length) throw new Error('密码不能为空。');
  if (email !== null && (typeof email !== 'string' || !email.trim() || email.length > 120)) {
    throw new Error('邮件地址不能为空，且不能超过 120 个字符。');
  }

  const host = config.db.host.split(':');
  const db = await mysql.createConnection({
    host: host[0], port: Number(host[1] || 3306),
    user: config.db.username, password: config.db.password, database: config.db.database
  });
  try {
    // This legacy SYZOJ login compares MD5(password + salt), never a plaintext password.
    const digest = crypto.createHash('md5').update(password + 'syzoj2_xxx').digest('hex');
    const [result] = await db.execute(
      'INSERT INTO `user` (username, password, email, is_admin, is_show, rating, register_time, ac_num, submit_num, public_email, prefer_formatted_code, information, nickname, nameplate, sex) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 0, 1, ?, ?, ?, 0)',
      [username, digest, email && email.trim(), isAdmin ? 1 : 0, config.default.user.show ? 1 : 0,
        config.default.user.rating, Math.floor(Date.now() / 1000), '', '', '']
    );
    return { id: result.insertId, username, isAdmin };
  } catch (err) {
    if (err.code === 'ER_DUP_ENTRY') throw new Error('用户名已存在，未修改现有账号。');
    throw err;
  } finally {
    await db.end();
  }
}

function askPassword(prompt) {
  return new Promise(resolve => {
    const muted = new Writable({ write(chunk, encoding, callback) { callback(); } });
    const rl = readline.createInterface({ input: process.stdin, output: muted, terminal: true });
    process.stdout.write(prompt);
    rl.question('', answer => {
      rl.close();
      process.stdout.write('\n');
      resolve(answer);
    });
    rl.on('SIGINT', () => { rl.close(); process.stdout.write('\n'); process.exit(130); });
  });
}

async function main() {
  const args = process.argv.slice(2);
  if (!args.length || args.includes('--help')) {
    console.log('用法：./bin/create-user 用户名 [--admin] [--email 邮件地址]');
    console.log('密码会在终端中隐藏输入；默认创建普通账号，--admin 创建管理员。');
    return;
  }
  const username = args.shift();
  let isAdmin = false, email = null;
  while (args.length) {
    const arg = args.shift();
    if (arg === '--admin') isAdmin = true;
    else if (arg === '--email' && args.length) email = args.shift();
    else throw new Error('未知或不完整的参数：' + arg);
  }
  if (!process.stdin.isTTY) throw new Error('请在交互式终端运行，以隐藏输入密码。');
  const password = await askPassword('输入新账号密码（不显示）：');
  const confirmation = await askPassword('再次输入密码：');
  if (password !== confirmation) throw new Error('两次密码不一致，未创建账号。');
  const user = await createUser({ username, password, email, isAdmin });
  console.log(`已创建${isAdmin ? '管理员' : '普通'}账号：${user.username}（ID ${user.id}）`);
}

module.exports = { createUser };
if (require.main === module) main().catch(err => { console.error(err.message); process.exitCode = 1; });
