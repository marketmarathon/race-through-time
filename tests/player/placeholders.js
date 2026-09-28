/* Placeholder pictures for the overlay boxes (DEC-035): Luke's logo and the car picture are private
 * media and are never committed (DEC-006), so the tests and the phone check draw plain rectangles in
 * their place, written at run time into tests/output/ (gitignored). Standard library only. */
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

/* A plain-rectangle PNG (placeholder for the private logo and car pictures; written at test
   time into tests/output/, never committed). */
function placeholderPNG(file, w, h, rgb) {
  const crcT = []; for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; crcT[n] = c >>> 0; }
  const crc = b => { let c = 0xffffffff; for (const x of b) c = crcT[(c ^ x) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
  const chunk = (t, d) => { const l = Buffer.alloc(4); l.writeUInt32BE(d.length); const td = Buffer.concat([Buffer.from(t), d]); const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l, td, c]); };
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 2;
  const raw = Buffer.alloc((w * 3 + 1) * h); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) raw.set(rgb, y * (w * 3 + 1) + 1 + x * 3);
  fs.writeFileSync(file, Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw)), chunk('IEND', Buffer.alloc(0))]));
}
function placeholders(cfg, dir) {
  fs.mkdirSync(dir, { recursive: true });
  // IQ-05d (DEC-045): the shapes of the real files - Luke's full logo with its wordmark is
  // 1983 x 793 (2.5 : 1), the car photo 3435 x 936 (about 3.67 : 1)
  const shape = { logo: [1983, 793, [212, 175, 55]], car: [3435, 936, [200, 200, 200]] };
  for (const b of cfg.overlays || []) { const [w, h, c] = shape[b.name] || [b.w, b.h, [128, 128, 128]]; placeholderPNG(path.join(dir, b.file), w, h, c); }
  return dir;
}

module.exports = { placeholderPNG, placeholders };
