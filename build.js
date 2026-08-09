const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const DIST = path.join(ROOT, 'dist');
const WEB = path.join(ROOT, 'web');
const I18N = path.join(ROOT, 'i18n');

function copyDir(source, target) {
  fs.mkdirSync(target, {recursive: true});
  for (const entry of fs.readdirSync(source, {withFileTypes: true})) {
    const from = path.join(source, entry.name); const to = path.join(target, entry.name);
    if (entry.isDirectory()) copyDir(from, to); else fs.copyFileSync(from, to);
  }
}

function translationManifest(codes) {
  const standard = codes.filter((item) => item.type === 'standard');
  const standardIds = new Set(standard.map((item) => item.id));
  const standardCodes = new Set(standard.map((item) => String(item.code)));
  const allIds = new Set(codes.map((item) => item.id));
  return fs.readdirSync(I18N).filter((file) => file.endsWith('.json') && file !== 'manifest.json').sort().map((file) => {
    const data = JSON.parse(fs.readFileSync(path.join(I18N, file), 'utf8')); const keys = Object.keys(data);
    const translatedStandard = keys.filter((key) => standardIds.has(key) || standardCodes.has(key)).length;
    const translatedOverall = keys.filter((key) => allIds.has(key) || standardCodes.has(key)).length;
    return {lang: path.basename(file, '.json'), translated_standard: translatedStandard, standard_total: standard.length, standard_percent: Number(((translatedStandard / standard.length) * 100).toFixed(1)), translated_overall: translatedOverall, overall_total: codes.length, overall_percent: Number(((translatedOverall / codes.length) * 100).toFixed(1))};
  });
}

fs.rmSync(DIST, {recursive: true, force: true}); fs.mkdirSync(DIST, {recursive: true});
copyDir(WEB, DIST); fs.copyFileSync(path.join(ROOT, 'codes.json'), path.join(DIST, 'codes.json')); copyDir(I18N, path.join(DIST, 'i18n'));
const codes = JSON.parse(fs.readFileSync(path.join(ROOT, 'codes.json'), 'utf8'));
fs.writeFileSync(path.join(DIST, 'i18n', 'manifest.json'), `${JSON.stringify(translationManifest(codes), null, 2)}\n`);
const indexHtml = fs.readFileSync(path.join(WEB, 'index.html'), 'utf8');
function writeRoute(parts) { const dir = path.join(DIST, ...parts); fs.mkdirSync(dir, {recursive: true}); fs.writeFileSync(path.join(dir, 'index.html'), indexHtml); }
for (const item of codes) { if (item.type === 'standard') writeRoute(['status', String(item.code)]); else writeRoute(['status', item.provider, String(item.code)]); }
console.log(`Build complete: ${codes.length} status entries and static permalinks generated in dist/.`);
