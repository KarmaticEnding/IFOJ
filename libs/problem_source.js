'use strict';
const fs = require('fs-extra');
const path = require('path');
const yaml = require('js-yaml');

async function getProject(id) {
  const database = path.resolve(__dirname, '../problem-database');
  try {
    const index = await fs.readJson(path.join(database, 'problem-index.json'));
    const folder = index[String(id)];
    let relative;
    let allowedRoot;
    if (typeof folder === 'string' && /^[a-zA-Z0-9_-]+$/.test(folder)) {
      relative = path.join('problems', folder);
      allowedRoot = 'problems';
    } else if (folder && typeof folder.path === 'string' && /^contests\/(?:[a-zA-Z0-9_-]+\/)+[a-zA-Z0-9_-]+$/.test(folder.path)) {
      relative = folder.path;
      allowedRoot = 'contests';
    } else return null;
    const projects = await fs.realpath(path.join(database, allowedRoot));
    const directory = await fs.realpath(path.join(database, relative));
    if (!directory.startsWith(projects + path.sep)) return null;
    const configFile = await fs.realpath(path.join(directory, 'conf.yaml'));
    if (!configFile.startsWith(directory + path.sep)) return null;
    const config = yaml.load(await fs.readFile(configFile, 'utf8'));
    return { directory, config };
  } catch (err) {
    if (err.code !== 'ENOENT') syzoj.log(err);
    return null;
  }
}

async function getName(id) {
  const project = await getProject(id);
  return project && project.config && typeof project.config.name === 'string' ? project.config.name : null;
}

function getMarkdown(problem) {
  const parts = [];
  for (const [key, title] of [['description', '题目描述'], ['input_format', '输入格式'], ['output_format', '输出格式']]) {
    if (problem[key] && problem[key].trim()) parts.push('## ' + title + '\n\n' + problem[key].trim());
  }
  for (const key of ['example', 'limit_and_hint']) {
    if (problem[key] && problem[key].trim()) parts.push(problem[key].trim());
  }
  return parts.join('\n\n') + '\n';
}

module.exports = { getName, getMarkdown, getProject };
