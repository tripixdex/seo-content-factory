"""UI page HTML for the local demo app."""

from __future__ import annotations


def build_ui_html(default_output_dir: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SEO Factory Demo UI</title>
  <style>
    :root {{
      --bg:#f7f9fc; --card:#fff; --ink:#111827; --line:#d1d5db;
      --ok:#065f46; --err:#991b1b;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--ink);
    }}
    .wrap {{ max-width: 900px; margin: 24px auto; padding: 0 16px; }}
    .card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 14px;
    }}
    h1, h2 {{ margin: 0 0 10px; }}
    p {{ margin: 8px 0; }}
    .tabs {{ display: flex; gap: 8px; margin-bottom: 12px; }}
    .tab {{
      border: 1px solid var(--line);
      background: #fff;
      padding: 8px 10px;
      border-radius: 8px;
      cursor: pointer;
    }}
    .tab.active {{ border-color: #2563eb; color: #2563eb; }}
    .mode {{ display: none; }}
    .mode.active {{ display: block; }}
    label {{ display: block; font-weight: 600; margin: 10px 0 6px; }}
    input {{ width: 100%; padding: 8px; border: 1px solid var(--line); border-radius: 8px; }}
    .row {{
      display: grid;
      gap: 10px;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    }}
    button {{
      margin-top: 12px;
      padding: 10px 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      cursor: pointer;
    }}
    .error {{
      display: none;
      white-space: pre-wrap;
      background: #fee2e2;
      color: var(--err);
      border: 1px solid #fca5a5;
      border-radius: 8px;
      padding: 10px;
      margin-top: 10px;
    }}
    .result {{
      display: none;
      border: 1px solid #93c5fd;
      background: #eff6ff;
      border-radius: 8px;
      padding: 10px;
      margin-top: 10px;
    }}
    .ok {{ color: var(--ok); font-weight: 700; }}
    pre {{
      margin: 8px 0;
      background: #111827;
      color: #f9fafb;
      padding: 10px;
      border-radius: 8px;
      overflow-x: auto;
    }}
    ol {{ margin: 6px 0 0 18px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>SEO Content Factory</h1>
      <h2>Quick demo steps</h2>
      <ol>
        <li>Select a mode (single HTML or batch CSV).</li>
        <li>Fill `keyword`, `job_id`, and `run_id` (single) or `run_id` (batch).</li>
        <li>Click run and share the generated output paths.</li>
      </ol>
      <p><strong>Accepted inputs:</strong> `.html/.htm` for single mode, `.csv` for batch mode.</p>
      <p><strong>Offline mode:</strong> all processing is local-only. No network fetches.</p>
      <p>
        <strong>Write location:</strong> defaults to
        <code>{default_output_dir}</code>. Any override must stay inside <code>outputs/</code>.
      </p>
    </div>

    <div class="card">
      <div class="tabs">
        <button class="tab active" id="tab-single" type="button">Single Run</button>
        <button class="tab" id="tab-batch" type="button">Batch CSV</button>
      </div>

      <div class="mode active" id="mode-single">
        <form id="single-form">
          <label for="single_file">HTML file</label>
          <input id="single_file" type="file" accept=".html,.htm" required />
          <div class="row">
            <div>
              <label for="keyword">Keyword</label>
              <input id="keyword" value="product analytics automation" required />
            </div>
            <div>
              <label for="job_id">Job ID</label>
              <input id="job_id" value="ui-item-001" required />
            </div>
            <div>
              <label for="single_run_id">Run ID</label>
              <input id="single_run_id" value="ui-run-001" required />
            </div>
          </div>
          <label for="single_output_dir">Output directory in outputs/ (optional)</label>
          <input id="single_output_dir" placeholder="{default_output_dir}" />
          <button type="submit">Run Single</button>
        </form>
      </div>

      <div class="mode" id="mode-batch">
        <form id="batch-form">
          <label for="batch_file">CSV file</label>
          <input id="batch_file" type="file" accept=".csv" required />
          <div class="row">
            <div>
              <label for="batch_run_id">Run ID</label>
              <input id="batch_run_id" value="ui-batch-001" required />
            </div>
            <div>
              <label for="batch_output_dir">Output directory in outputs/ (optional)</label>
              <input id="batch_output_dir" placeholder="{default_output_dir}" />
            </div>
          </div>
          <button type="submit">Run Batch</button>
        </form>
      </div>

      <div id="error-box" class="error"></div>
      <div id="result-box" class="result"></div>
    </div>
  </div>

  <script>
    const tabs = {{
      single: document.getElementById('tab-single'),
      batch: document.getElementById('tab-batch')
    }};
    const modes = {{
      single: document.getElementById('mode-single'),
      batch: document.getElementById('mode-batch')
    }};
    const errorBox = document.getElementById('error-box');
    const resultBox = document.getElementById('result-box');

    function setMode(mode) {{
      const isSingle = mode === 'single';
      tabs.single.classList.toggle('active', isSingle);
      tabs.batch.classList.toggle('active', !isSingle);
      modes.single.classList.toggle('active', isSingle);
      modes.batch.classList.toggle('active', !isSingle);
      errorBox.style.display = 'none';
      resultBox.style.display = 'none';
    }}

    tabs.single.addEventListener('click', () => setMode('single'));
    tabs.batch.addEventListener('click', () => setMode('batch'));

    function renderResult(payload) {{
      const paths = payload.output_paths || {{}};
      const pathLines = Object.entries(paths).map(([k, v]) => `${{k}}: ${{v}}`).join('\\n');
      const firstPath = Object.values(paths)[0] || '';
      resultBox.innerHTML = `
        <p><strong>Status:</strong> <span class="ok">${{payload.status}}</span></p>
        <p>
          <strong>Quality:</strong> ${{payload.quality_score}}
          | <strong>Passed:</strong> ${{payload.passed}}
        </p>
        <p><strong>Output paths</strong></p>
        <pre id="paths-block">${{pathLines || 'No output paths returned.'}}</pre>
        <button id="copy-path" type="button">Copy output path</button>
      `;
      resultBox.style.display = 'block';
      const copyBtn = document.getElementById('copy-path');
      copyBtn.addEventListener('click', async () => {{
        if (!firstPath) return;
        await navigator.clipboard.writeText(String(firstPath));
      }});
    }}

    function renderError(message) {{
      errorBox.textContent = message;
      errorBox.style.display = 'block';
      resultBox.style.display = 'none';
    }}

    async function postJson(url, payload) {{
      const response = await fetch(url, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(payload)
      }});
      const data = await response.json();
      if (!response.ok) {{
        throw new Error(data.detail || JSON.stringify(data));
      }}
      return data;
    }}

    document.getElementById('single-form').addEventListener('submit', async (event) => {{
      event.preventDefault();
      try {{
        const sourceFile = document.getElementById('single_file').files[0];
        if (!sourceFile) throw new Error('Select an HTML file.');
        const payload = {{
          source_filename: sourceFile.name,
          html_content: await sourceFile.text(),
          keyword: document.getElementById('keyword').value,
          job_id: document.getElementById('job_id').value,
          run_id: document.getElementById('single_run_id').value,
          output_dir: document.getElementById('single_output_dir').value || null
        }};
        renderResult(await postJson('/run-one', payload));
      }} catch (error) {{
        renderError(String(error));
      }}
    }});

    document.getElementById('batch-form').addEventListener('submit', async (event) => {{
      event.preventDefault();
      try {{
        const csvFile = document.getElementById('batch_file').files[0];
        if (!csvFile) throw new Error('Select a CSV file.');
        const payload = {{
          csv_filename: csvFile.name,
          csv_content: await csvFile.text(),
          run_id: document.getElementById('batch_run_id').value,
          output_dir: document.getElementById('batch_output_dir').value || null
        }};
        renderResult(await postJson('/run-batch', payload));
      }} catch (error) {{
        renderError(String(error));
      }}
    }});
  </script>
</body>
</html>
"""
