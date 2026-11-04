'use strict';
const fs = require('fs-extra');
const path = require('path');
const { spawn } = require('child_process');
const { getProject } = require('./problem_source');

async function validateDirectory(directory) {
  for (const entry of await fs.readdir(directory)) {
    const file = path.join(directory, entry);
    const stat = await fs.lstat(file);
    if (stat.isSymbolicLink() || (!stat.isFile() && !stat.isDirectory())) {
      throw new ErrorMessage('相关文件目录包含不支持的文件类型。');
    }
    if (stat.isDirectory()) await validateDirectory(file);
    else await fs.access(file, fs.constants.R_OK);
  }
}

const zipProgram = `
import os, sys, zipfile
root = os.path.realpath(sys.argv[1])
with zipfile.ZipFile(sys.stdout.buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
    for parent, directories, files in os.walk(root, followlinks=False):
        directories.sort()
        files.sort()
        for name in directories + files:
            if os.path.islink(os.path.join(parent, name)):
                raise RuntimeError('Symbolic links are not allowed')
        if parent != root and not directories and not files:
            archive.writestr(os.path.relpath(parent, root).replace(os.sep, '/') + '/', b'')
        for name in files:
            filename = os.path.join(parent, name)
            archive.write(filename, os.path.relpath(filename, root))
`;

async function download(problem, res) {
  const project = await getProject(problem.id);
  if (!project) return res.status(404).render('error', { err: new ErrorMessage('无此题目的相关文件。') });
  const directory = path.join(project.directory, 'down');
  let stat;
  try { stat = await fs.lstat(directory); }
  catch (err) { if (err.code !== 'ENOENT') throw err; }
  if (!stat || !stat.isDirectory() || stat.isSymbolicLink()) {
    return res.status(404).render('error', { err: new ErrorMessage('无此题目的相关文件。') });
  }
  await validateDirectory(directory);
  const zipper = spawn('python3', ['-B', '-c', zipProgram, directory], { stdio: ['ignore', 'pipe', 'pipe'] });
  res.attachment(String(problem.id) + '.zip');
  res.set('Cache-Control', 'no-store');
  let errorText = '', failed = false;
  function fail(err) {
    if (failed) return;
    failed = true;
    syzoj.log(err);
    zipper.stdout.unpipe(res);
    if (res.headersSent) res.destroy();
    else {
      res.removeHeader('Content-Disposition');
      res.status(500).type('text/plain').end('相关文件打包失败。');
    }
  }
  zipper.stderr.on('data', chunk => { errorText = (errorText + chunk).slice(0, 4096); });
  zipper.on('error', fail);
  zipper.stdout.on('error', fail);
  zipper.stdout.pipe(res, { end: false });
  zipper.on('close', code => {
    if (failed) return;
    if (code === 0) res.end();
    else fail(new Error('Related files ZIP failed: ' + errorText));
  });
  res.on('close', () => { if (!res.writableEnded && zipper.exitCode === null) zipper.kill(); });
}

module.exports = { download, validateDirectory };
