const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = Number(process.env.PORT || 3000);
const ROOT = __dirname;
const WEB_DIR = path.join(ROOT, 'web');
const I18N_DIR = path.join(ROOT, 'i18n');
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const loadCodes = () => readJson(path.join(ROOT, 'codes.json'));

function loadLanguages() {
  const codes = loadCodes();
  const standard = codes.filter((item) => item.type === 'standard');
  const standardIds = new Set(standard.map((item) => item.id));
  const standardCodes = new Set(standard.map((item) => String(item.code)));
  const allIds = new Set(codes.map((item) => item.id));
  return fs.readdirSync(I18N_DIR).filter((file) => file.endsWith('.json') && file !== 'manifest.json').sort().map((file) => {
    const lang = path.basename(file, '.json');
    const translations = readJson(path.join(I18N_DIR, file));
    const keys = Object.keys(translations);
    const translatedStandard = keys.filter((key) => standardIds.has(key) || standardCodes.has(key)).length;
    const translatedOverall = keys.filter((key) => allIds.has(key) || standardCodes.has(key)).length;
    return {lang, translated_standard: translatedStandard, standard_total: standard.length, standard_percent: Number(((translatedStandard / standard.length) * 100).toFixed(1)), translated_overall: translatedOverall, overall_total: codes.length, overall_percent: Number(((translatedOverall / codes.length) * 100).toFixed(1))};
  });
}

app.disable('x-powered-by');
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  res.setHeader('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'");
  next();
});
app.use(express.static(WEB_DIR, {extensions: ['html'], maxAge: '1h'}));
app.use('/i18n', express.static(I18N_DIR, {maxAge: '1h'}));
app.get('/codes.json', (req, res) => res.sendFile(path.join(ROOT, 'codes.json')));
app.get('/api/languages', (req, res) => res.json(loadLanguages()));
app.get('/api/codes', (req, res) => {
  let codes = loadCodes(); const {type, provider, status} = req.query;
  if (type) codes = codes.filter((item) => item.type === type);
  if (provider) codes = codes.filter((item) => item.provider === provider);
  if (status) codes = codes.filter((item) => item.status === status);
  res.json(codes);
});
app.get('/api/status/:code(\\d+)', (req, res) => {
  const code = Number(req.params.code); const matches = loadCodes().filter((item) => item.code === code);
  if (!matches.length) return res.status(404).json({error: 'Status code not found'}); return res.json(matches);
});
app.get('/api/status/:provider/:code(\\d+)', (req, res) => {
  const code = Number(req.params.code); const match = loadCodes().find((item) => item.code === code && item.provider === req.params.provider);
  if (!match) return res.status(404).json({error: 'Status code not found'}); return res.json(match);
});
app.get(['/status/:code(\\d+)', '/status/:provider/:code(\\d+)'], (req, res) => res.sendFile(path.join(WEB_DIR, 'index.html')));
app.use((req, res) => res.status(404).sendFile(path.join(WEB_DIR, 'index.html')));
app.listen(PORT, () => console.log(`HTTP Status Codes server running at http://localhost:${PORT}`));
