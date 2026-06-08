const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'web')));
app.use('/i18n', express.static(path.join(__dirname, 'i18n')));

app.get('/codes.json', (req, res) => {
  res.sendFile(path.join(__dirname, 'codes.json'));
});

app.listen(PORT, () => {
  console.log(`HTTP Status Codes server running at http://localhost:${PORT}`);
});
