const fs = require('fs');
const path = require('path');

const distDir = path.join(__dirname, 'dist');

// Create dist directory if it doesn't exist
if (!fs.existsSync(distDir)) {
    fs.mkdirSync(distDir, { recursive: true });
}

// Copy web files to dist
const webDir = path.join(__dirname, 'web');
const files = fs.readdirSync(webDir);
files.forEach(file => {
    fs.copyFileSync(path.join(webDir, file), path.join(distDir, file));
});

// Copy codes.json and i18n to dist
fs.copyFileSync(path.join(__dirname, 'codes.json'), path.join(distDir, 'codes.json'));

const i18nDistDir = path.join(distDir, 'i18n');
if (!fs.existsSync(i18nDistDir)) {
    fs.mkdirSync(i18nDistDir, { recursive: true });
}
const i18nFiles = fs.readdirSync(path.join(__dirname, 'i18n')).filter(f => f.endsWith('.json'));
i18nFiles.forEach(file => {
    fs.copyFileSync(path.join(__dirname, 'i18n', file), path.join(i18nDistDir, file));
});

console.log('Build completed successfully! Output in dist/');
