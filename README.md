# Dobrani by Ania - Polish Matchmaker

Static bilingual site (Polish at `/`, English at `/en/`) for polishmatchmaker.com, hosted on GitHub Pages.

- `build.py` generates every page and `sitemap.xml`. Edit copy there, then run `python3 build.py`.
- `assets/` holds CSS, JS, logos and favicons.
- Before going live, replace `REG_ADDR` in `build.py` with the registered office address.

## DNS (at your domain provider / Cloudflare)
Apex `polishmatchmaker.com`, four A records: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
`www`: CNAME to `anianka1983.github.io`
Set Cloudflare proxy to "DNS only" until GitHub issues the HTTPS certificate.
