"""
Recon113 - HTML Report Generator
Author: Megh
Generates a hacker-themed, self-contained HTML report with charts and animations.
"""

import html
import json
from datetime import datetime


class HTMLReportGenerator:
    """Generates a stunning hacker-themed HTML security report."""

    def __init__(self, results, output_path):
        self.results = results
        self.output_path = output_path

    def generate(self):
        """Generate the full HTML report."""
        meta = self.results.get("meta", {})
        target = self.results.get("target", {})
        recon = self.results.get("recon", {})
        crawler = self.results.get("crawler", {})
        vulns = self.results.get("vulnerabilities", [])
        stats = self.results.get("statistics", {})

        # Severity counts
        sev_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for v in vulns:
            s = v.get("severity", "INFO").upper()
            if s in sev_counts:
                sev_counts[s] += 1

        report_html = self._build_html(meta, target, recon, crawler, vulns, stats, sev_counts)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(report_html)

    def _build_html(self, meta, target, recon, crawler, vulns, stats, sev_counts):
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Recon113 Report - {self._esc(target.get('domain',''))}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{self._css()}</style>
</head>
<body>
<div class="container">
  {self._header_section(meta, target)}
  {self._nav_section()}
  {self._stats_section(stats, sev_counts)}
  {self._vuln_chart_section(sev_counts)}
  {self._target_section(target)}
  {self._recon_section(recon)}
  {self._crawler_section(crawler)}
  {self._vuln_section(vulns)}
  {self._footer_section(meta)}
</div>
<script>{self._js(sev_counts)}</script>
</body>
</html>"""

    def _css(self):
        return """
:root {
  --bg: #ffffff;
  --surface: #f8f9fa;
  --surface2: #e9ecef;
  --border: #dee2e6;
  --primary: #2563eb;
  --primary-light: #dbeafe;
  --red: #dc2626;
  --amber: #d97706;
  --green: #16a34a;
  --cyan: #0891b2;
  --text: #1f2937;
  --text-secondary: #6b7280;
  --dim: #9ca3af;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 14px;
  line-height: 1.6;
}
.container { max-width: 1100px; margin: 0 auto; padding: 24px; }

/* Header */
.header {
  text-align: center;
  padding: 36px 0 24px;
  border-bottom: 2px solid var(--border);
  margin-bottom: 24px;
}
.header h1 {
  font-size: 1.8em;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 6px;
}
.header .subtitle { color: var(--text-secondary); font-size: 0.9em; }
.header .target-badge {
  display: inline-block;
  background: var(--primary-light);
  border: 1px solid var(--primary);
  padding: 6px 20px;
  border-radius: 6px;
  margin-top: 12px;
  color: var(--primary);
  font-weight: 600;
  font-size: 0.95em;
}

/* Navigation */
nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}
nav a {
  color: var(--text-secondary);
  text-decoration: none;
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 0.8em;
  font-weight: 500;
  transition: all .2s;
}
nav a:hover {
  color: var(--primary);
  border-color: var(--primary);
  background: var(--primary-light);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  transition: box-shadow .2s;
}
.stat-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.stat-card .value {
  font-size: 1.6em;
  font-weight: 700;
  color: var(--primary);
}
.stat-card .label {
  font-size: 0.75em;
  color: var(--text-secondary);
  margin-top: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Sections */
.section { margin-bottom: 28px; }
.section-title {
  font-size: 1.05em;
  font-weight: 600;
  color: var(--text);
  padding: 10px 0;
  border-bottom: 2px solid var(--border);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
  font-size: 0.85em;
}
th {
  background: var(--surface);
  color: var(--text);
  padding: 10px 12px;
  text-align: left;
  border: 1px solid var(--border);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75em;
  letter-spacing: 0.5px;
}
td {
  padding: 8px 12px;
  border: 1px solid var(--border);
  vertical-align: top;
  word-break: break-word;
}
tr:nth-child(even) { background: var(--surface); }
tr:hover { background: #f0f4ff; }
tr.vuln-row { background: #fef2f2; border-left: 3px solid var(--red); }
tr.warn-row { background: #fffbeb; border-left: 3px solid var(--amber); }

/* Badges */
.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 0.72em;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.badge-critical { background: #fef2f2; color: #991b1b; border: 1px solid #fca5a5; }
.badge-high { background: #fff7ed; color: #9a3412; border: 1px solid #fdba74; }
.badge-medium { background: #fffbeb; color: #92400e; border: 1px solid #fcd34d; }
.badge-low { background: #ecfdf5; color: #065f46; border: 1px solid #6ee7b7; }
.badge-info { background: #f3f4f6; color: #4b5563; border: 1px solid #d1d5db; }

/* Vulnerability Cards */
.vuln-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 10px;
  overflow: hidden;
}
.vuln-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: background .2s;
}
.vuln-header:hover { background: var(--surface2); }
.vuln-header .title { font-weight: 500; }
.vuln-body {
  padding: 12px 16px;
  border-top: 1px solid var(--border);
  display: none;
  font-size: 0.85em;
  background: #fff;
}
.vuln-body.open { display: block; }
.vuln-body p { margin-bottom: 6px; }
.vuln-body .label { color: var(--text-secondary); font-size: 0.8em; }

/* Chart */
.chart-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  flex-wrap: wrap;
}
.donut-chart { position: relative; width: 200px; height: 200px; }
.donut-chart canvas { width: 200px; height: 200px; }
.chart-legend { display: flex; flex-direction: column; gap: 8px; }
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 0.8em; }
.legend-dot { width: 12px; height: 12px; border-radius: 3px; }

/* Info Cards */
.info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; }
.info-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px;
}
.info-card h4 {
  color: var(--primary);
  font-size: 0.8em;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.info-card p, .info-card li { font-size: 0.85em; margin-bottom: 4px; }
.info-card ul { list-style: none; padding: 0; }
.info-card ul li::before { content: "› "; color: var(--primary); font-weight: 700; }

.tag {
  display: inline-block;
  background: var(--surface2);
  border: 1px solid var(--border);
  padding: 1px 8px;
  border-radius: 4px;
  font-size: 0.75em;
  margin: 2px;
}

/* Footer */
.footer {
  text-align: center;
  padding: 30px 0;
  border-top: 2px solid var(--border);
  color: var(--text-secondary);
  font-size: 0.8em;
}

/* Collapsible */
.collapsible { cursor: pointer; user-select: none; }
.collapsible::after { content: " ▸"; color: var(--primary); }
.collapsible.active::after { content: " ▾"; }

/* Buttons */
.btn {
  display: inline-block;
  padding: 8px 18px;
  border: 1px solid var(--primary);
  border-radius: 6px;
  color: var(--primary);
  background: var(--primary-light);
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-size: 0.8em;
  font-weight: 500;
  transition: all .2s;
  text-decoration: none;
}
.btn:hover { background: var(--primary); color: #fff; }
.btn-red { border-color: var(--red); color: var(--red); background: #fef2f2; }
.btn-red:hover { background: var(--red); color: #fff; }

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .info-grid { grid-template-columns: 1fr; }
  .chart-container { flex-direction: column; }
}
@media print {
  .no-print { display: none !important; }
  body { font-size: 11px; }
  .container { max-width: 100%; }
  .badge { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .vuln-body { display: block !important; }
  .collapsible-content { display: block !important; }
  nav { display: none; }
}
"""

    def _header_section(self, meta, target):
        return f"""
<div class="header">
  <h1>Recon113</h1>
  <p class="subtitle">Automated Reconnaissance & Vulnerability Assessment Report</p>
  <div class="target-badge">{self._esc(target.get('domain','N/A'))}</div>
  <p class="subtitle" style="margin-top:10px">
    {self._esc(meta.get('scan_date',''))} &middot; v{self._esc(meta.get('version','1.0.0'))} &middot; Author: {self._esc(meta.get('author','Megh'))}
  </p>
</div>"""

    def _nav_section(self):
        return """
<nav>
  <a href="#stats">Dashboard</a>
  <a href="#target">Target</a>
  <a href="#recon">Reconnaissance</a>
  <a href="#crawler">Crawler</a>
  <a href="#vulns">Vulnerabilities</a>
  <a href="#" class="btn no-print" onclick="expandAll();return false">Expand All</a>
  <a href="#" class="btn btn-red no-print" onclick="downloadPDF();return false">Download PDF</a>
</nav>"""

    def _stats_section(self, stats, sev_counts):
        total_vulns = stats.get('total_vulnerabilities', 0)
        cards = f"""
<div id="stats" class="section">
  <h2 class="section-title">📊 Dashboard</h2>
  <div class="stats-grid">
    <div class="stat-card"><div class="value">{stats.get('total_subdomains',0)}</div><div class="label">Subdomains</div></div>
    <div class="stat-card"><div class="value">{stats.get('total_open_ports',0)}</div><div class="label">Open Ports</div></div>
    <div class="stat-card"><div class="value">{stats.get('total_technologies',0)}</div><div class="label">Technologies</div></div>
    <div class="stat-card"><div class="value">{stats.get('total_urls_crawled',0)}</div><div class="label">URLs Crawled</div></div>
    <div class="stat-card"><div class="value">{stats.get('total_directories',0)}</div><div class="label">Directories</div></div>
    <div class="stat-card"><div class="value" style="color:{'var(--red)' if total_vulns > 0 else 'var(--green)'}">{total_vulns}</div><div class="label">Vulnerabilities</div></div>
    <div class="stat-card"><div class="value">{stats.get('total_parameters',0)}</div><div class="label">Parameters</div></div>
    <div class="stat-card"><div class="value">{stats.get('scan_duration','N/A')}</div><div class="label">Duration</div></div>
  </div>
</div>"""
        return cards

    def _vuln_chart_section(self, sev_counts):
        total = sum(sev_counts.values())
        if total == 0:
            return ""
        colors = {"CRITICAL":"#dc2626","HIGH":"#ea580c","MEDIUM":"#d97706","LOW":"#16a34a","INFO":"#6b7280"}
        legend = ""
        for sev in ["CRITICAL","HIGH","MEDIUM","LOW","INFO"]:
            if sev_counts[sev] > 0:
                legend += f'<div class="legend-item"><div class="legend-dot" style="background:{colors[sev]}"></div>{sev}: {sev_counts[sev]}</div>'
        return f"""
<div class="chart-container">
  <div class="donut-chart"><canvas id="vulnChart" width="200" height="200"></canvas></div>
  <div class="chart-legend">{legend}</div>
</div>"""

    def _target_section(self, target):
        rows = ""
        for k in ["domain","ip","url","target_type","scheme"]:
            v = target.get(k,"")
            if v:
                rows += f"<tr><td><strong>{self._esc(k.replace('_',' ').title())}</strong></td><td>{self._esc(str(v))}</td></tr>"
        return f"""
<div id="target" class="section">
  <h2 class="section-title">🎯 Target Information</h2>
  <table><thead><tr><th>Property</th><th>Value</th></tr></thead><tbody>{rows}</tbody></table>
</div>"""

    def _recon_section(self, recon):
        parts = []
        # Subdomains — sorted by hacker priority
        subs = recon.get("subdomains",[])
        if subs:
            subs_sorted = self._sort_subdomains(subs)
            rows = ""
            for s in subs_sorted:
                if isinstance(s, dict):
                    ip = s.get('ip','N/A') or 'N/A'
                    cls = self._subdomain_row_class(s)
                    rows += f"<tr class='{cls}'><td>{self._esc(s.get('subdomain',''))}</td><td>{self._esc(ip)}</td><td>{self._esc(s.get('status',''))}</td></tr>"
                else:
                    rows += f"<tr><td>{self._esc(str(s))}</td><td>-</td><td>-</td></tr>"
            parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">Subdomains ({len(subs)})</h3>
<div class="collapsible-content"><table><thead><tr><th>Subdomain</th><th>IP</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        # Ports
        ports = recon.get("ports",[])
        open_ports = [p for p in ports if isinstance(p, dict) and p.get("state")=="open"]
        if open_ports:
            rows = ""
            for p in open_ports:
                rows += f"<tr><td>{p.get('port','')}</td><td><span class='badge badge-high'>OPEN</span></td><td>{self._esc(p.get('service',''))}</td><td>{self._esc(p.get('banner','')[:60])}</td></tr>"
            parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">Open Ports ({len(open_ports)})</h3>
<div class="collapsible-content"><table><thead><tr><th>Port</th><th>State</th><th>Service</th><th>Banner</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        # Technologies
        techs = recon.get("technologies",[])
        if techs:
            rows = ""
            for t in techs:
                if isinstance(t, dict):
                    rows += f"<tr><td>{self._esc(t.get('name',''))}</td><td>{t.get('confidence','')}%</td><td>{self._esc(', '.join(t.get('evidence',[])))}</td></tr>"
            parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">Technologies ({len(techs)})</h3>
<div class="collapsible-content"><table><thead><tr><th>Technology</th><th>Confidence</th><th>Evidence</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        # DNS
        dns = recon.get("dns",{})
        if dns:
            rows = ""
            for rtype, records in dns.items():
                if isinstance(records, list):
                    for r in records:
                        val = str(r) if not isinstance(r, dict) else json.dumps(r)
                        rows += f"<tr><td>{self._esc(rtype)}</td><td>{self._esc(val[:100])}</td></tr>"
            if rows:
                parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">DNS Records</h3>
<div class="collapsible-content"><table><thead><tr><th>Type</th><th>Value</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        # WHOIS
        whois = recon.get("whois",{})
        if whois:
            rows = ""
            for k,v in whois.items():
                if v and str(v) != "None":
                    rows += f"<tr><td>{self._esc(k.replace('_',' ').title())}</td><td>{self._esc(str(v)[:100])}</td></tr>"
            if rows:
                parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">WHOIS Information</h3>
<div class="collapsible-content"><table><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        # Headers
        hdrs = recon.get("headers",{})
        missing = hdrs.get("missing",[])
        present = hdrs.get("present",[])
        if missing or present:
            rows = ""
            for h in present:
                if isinstance(h, dict):
                    rows += f"<tr><td>{self._esc(h.get('header',''))}</td><td><span class='badge badge-info'>PRESENT</span></td><td>{self._esc(str(h.get('value',''))[:60])}</td></tr>"
            for h in missing:
                if isinstance(h, dict):
                    rows += f"<tr><td>{self._esc(h.get('header',''))}</td><td><span class='badge badge-{h.get('severity','LOW').lower()}'>MISSING</span></td><td>{self._esc(h.get('recommendation',''))}</td></tr>"
            parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">Security Headers</h3>
<div class="collapsible-content"><table><thead><tr><th>Header</th><th>Status</th><th>Detail</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        content = "\n".join(parts) if parts else "<p style='color:var(--dim)'>No reconnaissance data collected.</p>"
        return f'<div id="recon" class="section"><h2 class="section-title">🔍 Reconnaissance</h2>{content}</div>'

    def _crawler_section(self, crawler):
        parts = []
        urls = crawler.get("urls",[])
        if urls:
            rows = "".join(f"<tr><td>{self._esc(u)}</td></tr>" for u in urls)
            parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">Crawled URLs ({len(urls)})</h3>
<div class="collapsible-content"><table><thead><tr><th>URL</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        dirs = crawler.get("directories",[])
        if dirs:
            dirs_sorted = self._sort_directories(dirs)
            rows = ""
            for d in dirs_sorted:
                if isinstance(d, dict):
                    sc = d.get('status_code',0)
                    cls = 'vuln-row' if sc == 200 else ('warn-row' if sc == 403 else '')
                    rows += f"<tr class='{cls}'><td>{self._esc(d.get('path',''))}</td><td>{sc}</td><td>{self._esc(d.get('content_type','')[:40])}</td></tr>"
            parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">Directories ({len(dirs)})</h3>
<div class="collapsible-content"><table><thead><tr><th>Path</th><th>Status</th><th>Type</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        js_files = crawler.get("js_files",[])
        if js_files:
            rows = "".join(f"<tr><td>{self._esc(j)}</td></tr>" for j in js_files)
            parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">JavaScript Files ({len(js_files)})</h3>
<div class="collapsible-content"><table><thead><tr><th>URL</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        secrets = crawler.get("js_secrets",[])
        if secrets:
            rows = ""
            for s in secrets:
                if isinstance(s, dict):
                    rows += f"<tr><td><span class='badge badge-high'>{self._esc(s.get('type',''))}</span></td><td>{self._esc(s.get('value',''))}</td><td>{self._esc(s.get('file','').split('/')[-1])}</td></tr>"
            parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">JS Secrets ({len(secrets)})</h3>
<div class="collapsible-content"><table><thead><tr><th>Type</th><th>Value</th><th>File</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        params = crawler.get("parameters",[])
        if params:
            rows = ""
            for p in params:
                if isinstance(p, dict):
                    rows += f"<tr><td>{self._esc(p.get('name',''))}</td><td>{self._esc(', '.join(p.get('sources',[])))}</td><td>{self._esc(', '.join(p.get('methods',[])))}</td></tr>"
            parts.append(f"""<h3 class="collapsible" onclick="toggle(this)">Parameters ({len(params)})</h3>
<div class="collapsible-content"><table><thead><tr><th>Name</th><th>Source</th><th>Methods</th></tr></thead><tbody>{rows}</tbody></table></div>""")

        content = "\n".join(parts) if parts else "<p style='color:var(--dim)'>No crawl data collected.</p>"
        return f'<div id="crawler" class="section"><h2 class="section-title">🕷️ Crawling & Discovery</h2>{content}</div>'

    def _vuln_section(self, vulns):
        if not vulns:
            return '<div id="vulns" class="section"><h2 class="section-title">⚡ Vulnerabilities</h2><p style="color:var(--dim)">No vulnerabilities found.</p></div>'
        # Sort by severity
        order = {"CRITICAL":0,"HIGH":1,"MEDIUM":2,"LOW":3,"INFO":4}
        vulns_sorted = sorted(vulns, key=lambda v: order.get(v.get("severity","INFO").upper(), 5))
        cards = ""
        for i, v in enumerate(vulns_sorted):
            sev = v.get("severity","INFO").upper()
            badge_cls = f"badge-{sev.lower()}"
            detail = ""
            if v.get("detail"):
                detail += f"<p><span class='label'>Detail:</span> {self._esc(str(v['detail']))}</p>"
            if v.get("url"):
                detail += f"<p><span class='label'>URL:</span> {self._esc(str(v['url']))}</p>"
            if v.get("recommendation"):
                detail += f"<p><span class='label'>Fix:</span> {self._esc(str(v['recommendation']))}</p>"
            if v.get("source"):
                detail += f"<p><span class='label'>Source:</span> {self._esc(str(v['source']))}</p>"
            cards += f"""
<div class="vuln-card">
  <div class="vuln-header" onclick="this.nextElementSibling.classList.toggle('open')">
    <span class="title">{self._esc(v.get('title','Unknown'))}</span>
    <span class="badge {badge_cls}">{sev}</span>
  </div>
  <div class="vuln-body">{detail}</div>
</div>"""
        return f'<div id="vulns" class="section"><h2 class="section-title">⚡ Vulnerabilities ({len(vulns)})</h2>{cards}</div>'

    def _footer_section(self, meta):
        return f"""
<div class="footer">
  <p>Generated by Recon113 v{self._esc(meta.get('version','1.0.0'))} &middot; Author: {self._esc(meta.get('author','Megh'))}</p>
  <p>Report generated: {self._esc(meta.get('scan_date',''))}</p>
  <p style="margin-top:8px">⚠ This report is for authorized security testing only.</p>
</div>"""

    def _js(self, sev_counts):
        return f"""
function toggle(el){{el.classList.toggle('active');var c=el.nextElementSibling;c.style.display=c.style.display==='none'?'block':'none'}}
function expandAll(){{document.querySelectorAll('.collapsible-content').forEach(function(e){{e.style.display='block'}});document.querySelectorAll('.collapsible').forEach(function(e){{e.classList.add('active')}});document.querySelectorAll('.vuln-body').forEach(function(e){{e.classList.add('open')}})}}
function downloadPDF(){{expandAll();setTimeout(function(){{window.print()}},400)}}
document.querySelectorAll('.collapsible-content').forEach(function(e){{e.style.display='none'}});
(function(){{
  var canvas=document.getElementById('vulnChart');
  if(!canvas)return;
  var ctx=canvas.getContext('2d');
  var data=[{sev_counts.get('CRITICAL',0)},{sev_counts.get('HIGH',0)},{sev_counts.get('MEDIUM',0)},{sev_counts.get('LOW',0)},{sev_counts.get('INFO',0)}];
  var colors=['#dc2626','#ea580c','#d97706','#16a34a','#6b7280'];
  var total=data.reduce(function(a,b){{return a+b}},0);
  if(total===0)return;
  var cx=100,cy=100,r=80,ir=50,start=-Math.PI/2;
  for(var i=0;i<data.length;i++){{
    if(data[i]===0)continue;
    var slice=2*Math.PI*data[i]/total;
    ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,r,start,start+slice);ctx.closePath();
    ctx.fillStyle=colors[i];ctx.fill();start+=slice;
  }}
  ctx.beginPath();ctx.arc(cx,cy,ir,0,2*Math.PI);ctx.fillStyle='#f8f9fa';ctx.fill();
  ctx.fillStyle='#2563eb';ctx.font="bold 20px 'Inter', sans-serif";ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.fillText(total,cx,cy);
}})();"""

    @staticmethod
    def _esc(text):
        return html.escape(str(text)) if text else ""

    @staticmethod
    def _sort_subdomains(subs):
        """Sort subdomains by hacker priority: internal IPs, dev/staging/admin first."""
        INTERESTING_KEYWORDS = [
            'admin', 'dev', 'staging', 'test', 'beta', 'internal', 'intranet',
            'vpn', 'remote', 'jenkins', 'git', 'ci', 'deploy', 'debug',
            'api', 'dashboard', 'portal', 'login', 'auth', 'sso', 'db',
            'database', 'mysql', 'mongo', 'redis', 'elastic', 'grafana',
            'backup', 'old', 'legacy', 'phpmyadmin', 'cpanel', 'ftp',
            'mail', 'smtp', 'webmail', 'ssh', 'shell', 'console', 'monitor',
        ]

        def score(s):
            if not isinstance(s, dict):
                return 99
            ip = s.get('ip', '') or ''
            name = s.get('subdomain', '').lower()
            status = s.get('status', '')

            # Unresolved = lowest priority
            if status != 'active':
                return 90

            priority = 50  # default active

            # Internal IPs are gold — highest priority
            if ip.startswith('10.') or ip.startswith('192.168.') or ip.startswith('172.'):
                priority = 0
            # Interesting names
            for kw in INTERESTING_KEYWORDS:
                if kw in name:
                    priority = min(priority, 10)
                    break
            return priority

        return sorted(subs, key=score)

    @staticmethod
    def _subdomain_row_class(s):
        """Return CSS class for highlighting interesting subdomains."""
        if not isinstance(s, dict):
            return ''
        ip = s.get('ip', '') or ''
        name = s.get('subdomain', '').lower()
        if ip.startswith('10.') or ip.startswith('192.168.') or ip.startswith('172.'):
            return 'vuln-row'
        interesting = ['admin', 'dev', 'staging', 'test', 'beta', 'internal',
                       'vpn', 'jenkins', 'git', 'api', 'dashboard', 'login',
                       'db', 'backup', 'ftp', 'ssh', 'console', 'debug']
        for kw in interesting:
            if kw in name:
                return 'warn-row'
        return ''

    @staticmethod
    def _sort_directories(dirs):
        """Sort directories: 200 first (accessible), then 403 (forbidden but exists), then 301."""
        STATUS_PRIORITY = {200: 0, 403: 1, 405: 2, 301: 3, 302: 4}
        INTERESTING_PATHS = [
            'admin', 'config', 'backup', '.env', '.git', 'database', 'debug',
            'phpmyadmin', 'console', 'shell', 'upload', 'api', 'private',
            'secret', 'log', 'password', 'token', 'key', 'credential',
        ]

        def score(d):
            if not isinstance(d, dict):
                return 99
            sc = d.get('status_code', 999)
            path = d.get('path', '').lower()

            base = STATUS_PRIORITY.get(sc, 5)
            # Bump interesting paths higher within their status group
            for kw in INTERESTING_PATHS:
                if kw in path:
                    return base * 10  # Keep status priority but sort interesting first
            return base * 10 + 1

        return sorted(dirs, key=score)
