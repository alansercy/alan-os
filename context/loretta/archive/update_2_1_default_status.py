"""
Workflow 2.1 — Add 'Default Status to Idea' code node between
'Read Content Calendar' and 'Filter Episodes'.

Purpose: defaults blank/missing Status to 'Idea' so Loretta only has to
fill Episode Title and Film Date for the brief generator to fire.

Run from the PowerShell session where $env:N8N_API_KEY is set:
    python C:\\loretta-os\\scripts\\update_2_1_default_status.py
"""
import json, os, re, sys
import urllib.request, urllib.error

WF_ID       = '69lXVUnqWMr2yF1q'
BASE        = 'http://localhost:5678/api/v1'
EXPORT_PATH = r'C:\loretta-os\workflows\69lXVUnqWMr2yF1q.json'
NEW_NODE    = 'Default Status to Idea'

ALLOWED_SETTINGS = {
    'executionOrder', 'saveDataErrorExecution', 'saveDataSuccessExecution',
    'saveManualExecutions', 'callerPolicy', 'errorWorkflow',
}

NEW_NODE_JS = """return $input.all().map(item => {
  const status = (item.json['Status'] || '').toString().trim();
  return { json: { ...item.json, Status: status || 'Idea' } };
});"""

api_key = os.environ.get('N8N_API_KEY')
if not api_key:
    print('ERROR: N8N_API_KEY not set in environment', file=sys.stderr)
    sys.exit(1)


def call(method, path, body=None):
    url = BASE + path
    data = json.dumps(body).encode('utf-8') if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={
            'X-N8N-API-KEY': api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode('utf-8')
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body_resp = e.read().decode('utf-8', errors='replace')
        print(f'HTTP {e.code} on {method} {path}', file=sys.stderr)
        print(f'  Body: {body_resp[:600]}', file=sys.stderr)
        raise


# 1. GET current workflow
wf = call('GET', f'/workflows/{WF_ID}')
print(f'Loaded: {wf["name"]}  ({len(wf["nodes"])} nodes)')

# 2. Idempotent check
if any(n['name'] == NEW_NODE for n in wf['nodes']):
    print(f'Node "{NEW_NODE}" already exists -- nothing to do.')
    sys.exit(0)

# 3. Sanity-check the existing Read Content Calendar -> Filter Episodes wiring
read_main = (wf['connections'].get('Read Content Calendar') or {}).get('main') or [[]]
if not (read_main and read_main[0] and read_main[0][0].get('node') == 'Filter Episodes'):
    print(f'ERROR: unexpected wiring on Read Content Calendar: {read_main}', file=sys.stderr)
    sys.exit(2)

# 4. Build the new node
new_node = {
    'parameters': {'jsCode': NEW_NODE_JS},
    'id':          'code-default-status-1',
    'name':        NEW_NODE,
    'type':        'n8n-nodes-base.code',
    'typeVersion': 2,
    'position':    [424, 304],  # midpoint between Read (288,304) and Filter (560,304)
}
wf['nodes'].append(new_node)

# 5. Rewire: Read Content Calendar -> Default Status to Idea -> Filter Episodes
wf['connections']['Read Content Calendar'] = {
    'main': [[{'node': NEW_NODE, 'type': 'main', 'index': 0}]],
}
wf['connections'][NEW_NODE] = {
    'main': [[{'node': 'Filter Episodes', 'type': 'main', 'index': 0}]],
}

# 6. Build strict PUT body
clean_settings = {
    k: v for k, v in (wf.get('settings') or {}).items() if k in ALLOWED_SETTINGS
}
put_body = {
    'name':        wf['name'],
    'nodes':       wf['nodes'],
    'connections': wf['connections'],
    'settings':    clean_settings,
}

# 7. PUT
print('PUTting updated workflow...')
call('PUT', f'/workflows/{WF_ID}', put_body)
print('PUT OK.')

# 8. Verify via GET
verify = call('GET', f'/workflows/{WF_ID}')
node_names = [n['name'] for n in verify['nodes']]
chain_ok = (
    (verify['connections'].get('Read Content Calendar') or {}).get('main', [[]])[0][0].get('node') == NEW_NODE
    and (verify['connections'].get(NEW_NODE) or {}).get('main', [[]])[0][0].get('node') == 'Filter Episodes'
)
print(f'Nodes ({len(verify["nodes"])}): {", ".join(node_names)}')
print(f'Chain Read -> {NEW_NODE} -> Filter Episodes verified: {chain_ok}')
if not chain_ok:
    sys.exit(3)

# 9. Save scrubbed JSON to disk for the loretta-os repo
text = json.dumps(verify, indent=2, ensure_ascii=False)
text = re.sub(r'sk-ant-api\d+-[A-Za-z0-9_-]+', '{{ANTHROPIC_API_KEY}}', text)
os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)
with open(EXPORT_PATH, 'w', encoding='utf-8', newline='') as h:
    h.write(text)
print(f'Saved scrubbed JSON: {EXPORT_PATH}')
