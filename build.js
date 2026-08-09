const fs = require('fs');
const path = require('path');
const ROOT = __dirname;
const DIST = path.join(ROOT, 'dist');
const WEB = path.join(ROOT, 'web');
const I18N = path.join(ROOT, 'i18n');
const rawBase = (process.env.BASE_PATH || '').trim();
const BASE_PATH = rawBase && rawBase !== '/' ? `/${rawBase.replace(/^\/+|\/+$/g, '')}` : '';
const SITE_URL = (process.env.SITE_URL || '').replace(/\/+$/, '');

function copyDir(source, target) {
  fs.mkdirSync(target, {recursive: true});
  for (const entry of fs.readdirSync(source, {withFileTypes: true})) {
    const from = path.join(source, entry.name);
    const to = path.join(target, entry.name);
    if (entry.isDirectory()) copyDir(from, to);
    else fs.copyFileSync(from, to);
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'})[char]);
}

function translationManifest(codes) {
  const standard = codes.filter((item) => item.type === 'standard');
  const standardIds = new Set(standard.map((item) => item.id));
  const standardCodes = new Set(standard.map((item) => String(item.code)));
  const allIds = new Set(codes.map((item) => item.id));
  return fs.readdirSync(I18N).filter((file) => file.endsWith('.json') && file !== 'manifest.json').sort().map((file) => {
    const data = JSON.parse(fs.readFileSync(path.join(I18N, file), 'utf8'));
    const keys = Object.keys(data);
    const translatedStandard = keys.filter((key) => standardIds.has(key) || standardCodes.has(key)).length;
    const translatedOverall = keys.filter((key) => allIds.has(key) || standardCodes.has(key)).length;
    return {lang:path.basename(file,'.json'),translated_standard:translatedStandard,standard_total:standard.length,standard_percent:Number(((translatedStandard/standard.length)*100).toFixed(1)),translated_overall:translatedOverall,overall_total:codes.length,overall_percent:Number(((translatedOverall/codes.length)*100).toFixed(1))};
  });
}

function routePath(item) {return item.type === 'standard' ? `/status/${item.code}/` : `/status/${encodeURIComponent(item.provider)}/${item.code}/`;}

function pageHtml(source, item = null) {
  let html = source
    .replace('<meta name="app-base" content="">', `<meta name="app-base" content="${BASE_PATH}">`)
    .replaceAll('href="/favicon.svg"', `href="${BASE_PATH}/favicon.svg"`)
    .replaceAll('href="/manifest.webmanifest"', `href="${BASE_PATH}/manifest.webmanifest"`)
    .replaceAll('href="/style.css"', `href="${BASE_PATH}/style.css"`)
    .replaceAll('src="/script.js"', `src="${BASE_PATH}/script.js"`);
  if (!item || !SITE_URL) return html;
  const pageUrl = `${SITE_URL}${routePath(item)}`;
  const title = `HTTP ${item.code} ${item.phrase} — httpCode`;
  const provider = item.type === 'standard' ? 'IANA/RFC' : item.provider;
  const description = `HTTP ${item.code} ${item.phrase} — ${item.description} ${provider} status-code reference with source and lifecycle metadata.`;
  return html
    .replace(/<title>.*?<\/title>/, `<title>${escapeHtml(title)}</title>`)
    .replace(/<meta name="description" content=".*?">/, `<meta name="description" content="${escapeHtml(description)}">`)
    .replace(/<meta property="og:title" content=".*?">/, `<meta property="og:title" content="${escapeHtml(title)}">`)
    .replace(/<meta property="og:description" content=".*?">/, `<meta property="og:description" content="${escapeHtml(description)}">`)
    .replace(/<meta property="og:url" content=".*?">/, `<meta property="og:url" content="${escapeHtml(pageUrl)}">`)
    .replace(/<link rel="canonical" href=".*?">/, `<link rel="canonical" href="${escapeHtml(pageUrl)}">`);
}

fs.rmSync(DIST,{recursive:true,force:true}); fs.mkdirSync(DIST,{recursive:true}); copyDir(WEB,DIST); fs.copyFileSync(path.join(ROOT,'codes.json'),path.join(DIST,'codes.json')); copyDir(I18N,path.join(DIST,'i18n'));
const codes=JSON.parse(fs.readFileSync(path.join(ROOT,'codes.json'),'utf8'));
fs.writeFileSync(path.join(DIST,'i18n','manifest.json'),`${JSON.stringify(translationManifest(codes),null,2)}\n`);
const sourceIndex=fs.readFileSync(path.join(WEB,'index.html'),'utf8'); fs.writeFileSync(path.join(DIST,'index.html'),pageHtml(sourceIndex));
function writeRoute(item){const parts=item.type==='standard'?['status',String(item.code)]:['status',item.provider,String(item.code)]; const dir=path.join(DIST,...parts); fs.mkdirSync(dir,{recursive:true}); fs.writeFileSync(path.join(dir,'index.html'),pageHtml(sourceIndex,item));}
for(const item of codes)writeRoute(item);
if(SITE_URL){const urls=[`${SITE_URL}/`,...codes.map((item)=>`${SITE_URL}${routePath(item)}`)]; const sitemap=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',...urls.map((url)=>`  <url><loc>${escapeHtml(url)}</loc></url>`),'</urlset>',''].join('\n'); fs.writeFileSync(path.join(DIST,'sitemap.xml'),sitemap); fs.writeFileSync(path.join(DIST,'robots.txt'),`User-agent: *\nAllow: /\nSitemap: ${SITE_URL}/sitemap.xml\n`);}
console.log(`Build complete: ${codes.length} status entries and static permalinks generated in dist/. Base path: ${BASE_PATH||'/'}${SITE_URL?` · Site: ${SITE_URL}`:''}`);
