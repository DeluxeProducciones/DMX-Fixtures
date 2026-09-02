// Decrypt every .ssl2 in the Daslight 5 ScanLibrary into one JSON line per profile.
//
// Daslight (Nicolaudie) ships 25,610 fixture profiles as AraCrypt-encrypted XML
// under /Applications/Daslight 5/ScanLibrary. The npm package ssl2-tools
// (github.com/ecopoesis/ssl2-tools, cipher reversed by HakanL) decrypts them.
//
//   cd tools/daslight && npm install ssl2-tools && node bulk_decrypt.mjs
//
// writes library.jsonl beside it; scan_fingerprints.py reads that. 2026-09-02:
// this is how six 7R profiles in the show's exact channel order were found.

import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join } from 'path';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { decrypt } = require('./node_modules/ssl2-tools/dist/index.js');
const ROOT = '/Applications/Daslight 5/ScanLibrary';
const out = [];
let n = 0, bad = 0;
function walk(dir) {
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    if (statSync(p).isDirectory()) { walk(p); continue; }
    if (!e.toLowerCase().endsWith('.ssl2')) continue;
    try {
      const xml = decrypt(readFileSync(p)).toString('utf-8');
      const name = (xml.match(/SSLLIBRARY SSLNAME="([^"]*)"/) || [])[1] || '';
      const brand = (xml.match(/SSLBRAND="([^"]*)"/) || [])[1] || '';
      const modes = [];
      const modeRe = /<SSLMODE [^>]*SSLNBCHANNEL="(\d+)"[^>]*>([\s\S]*?)<\/SSLMODE>/g;
      let m;
      while ((m = modeRe.exec(xml))) {
        const channels = [];
        const chRe = /<SSLCHANNEL ([^>]*)>([\s\S]*?)<\/SSLCHANNEL>/g;
        let c;
        while ((c = chRe.exec(m[2]))) {
          const cname = (c[1].match(/SSLCHANNELNAME="([^"]*)"/) || [])[1] || '';
          const ctype = (c[1].match(/SSLCHANNELTYPE="([^"]*)"/) || [])[1] || '';
          const presets = [];
          const pRe = /<SSLPRESET [^>]*SSLPRESETNAME="([^"]*)"[^>]*SSLPRESETDMXSTART="(\d+)"[^>]*SSLPRESETDMXEND="(\d+)"/g;
          let pm;
          while ((pm = pRe.exec(c[2]))) presets.push([+pm[2], +pm[3], pm[1]]);
          channels.push({ name: cname, type: ctype, presets });
        }
        modes.push({ n: +m[1], channels });
      }
      out.push(JSON.stringify({ file: p.slice(ROOT.length + 1), name, brand, modes }));
      n++;
    } catch (err) { bad++; }
  }
}
walk(ROOT);
writeFileSync('library.jsonl', out.join('\n') + '\n');
console.log(`decoded ${n}, failed ${bad}`);
