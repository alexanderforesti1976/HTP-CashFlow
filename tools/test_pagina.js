// Prova della pagina nuova/index.html in un browser vero: nessun errore e tutte le sezioni piene. Uso: (cd nuova && python3 -m http.server 8790 &) ; NODE_PATH=$(npm root -g) node tools/test_pagina.js http://localhost:8790/index.html
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }), p = await b.newPage({ viewport: { width: 390, height: 900 } }), er = [];
  p.on('pageerror', e => er.push(e.message));
  await p.goto(process.argv[2] || 'http://localhost:8790/index.html'); await p.waitForTimeout(2000);
  const r = await p.evaluate(() => ({ err: (document.getElementById('err') || {}).textContent, vuote: ['kpis', 'ce26', 'tab', 'rating', 'indici', 'indici2'].filter(i => !document.getElementById(i) || document.getElementById(i).innerHTML.length < 50) }));
  const ok = !r.err && !er.length && !r.vuote.length; console.log(ok ? 'PAGINA OK' : 'PAGINA ROTTA', JSON.stringify(r), er); await b.close(); process.exit(ok ? 0 : 1);
})();
