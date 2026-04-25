# Alan OS — Persistent Brain
**Owner:** Alan Sercy · alansercy@gmail.com
**Last Updated:** April 22, 2026
**Status:** Active

---

## How to Load Context Into a Claude Session

Paste at the start of any session:
```
Load context: https://raw.githubusercontent.com/alansercy/alan-os/main/handoff/current.md
```

For strategy sessions, add the relevant domain file:
```
Load strategy: https://raw.githubusercontent.com/alansercy/alan-os/main/strategy/veritas_strategy.md
```

---

## Repo Structure

```
alan-os/
├── handoff/
│   └── current.md              ← Always the latest session handoff
├── strategy/
│   ├── veritas_strategy.md     ← $1.2M → $100M exit plan
│   ├── mmm_trucking.md         ← BD playbook, lane focus, shippers
│   ├── job_search.md           ← targets, comp floor, positioning
│   ├── lollie_brand.md         ← book series, merch, publishing path
│   └── family_governance.md    ← Norman/Marsha, Charles, estate
├── sops/
│   ├── lux_stack.md            ← Lux architecture, accounts, scripts
│   ├── norman_inbox_guard.md   ← how it works, whitelist governance
│   └── printful_shop.md        ← Lollie merch setup SOP
├── vault/
│   ├── templates/              ← reusable email/pitch/doc templates
│   ├── scripts/                ← key Python scripts backed up
│   └── prompts/                ← master prompt library
└── README.md                   ← This file — master index
```

---

## Active Workstreams

| Workstream | Status | Load File |
|---|---|---|
| Veritas AI Partners | Active — positioning blocker | strategy/veritas_strategy.md |
| MMM Trucking BD | Active — Hood May 1 deadline | strategy/mmm_trucking.md |
| Job Search | Active — remote CRO/EVP BD | strategy/job_search.md |
| Lollie & Lovie Lou | Website live — shop next | strategy/lollie_brand.md |
| Family Governance | Active — Norman/Charles/Estate | strategy/family_governance.md |
| Lux Stack | Live — 5 accounts running | sops/lux_stack.md |

---

## Key People

| Person | Role | Contact |
|---|---|---|
| Loretta Sercy | Wife · eXp Realty · Lollie author | lorettasercy@gmail.com / lsercy@mmmtrucks.com |
| Norman Sercy | Father — primary steward | sercypete@aol.com |
| Marsha Sercy | Mother — primary steward | sercymarsha@aol.com |
| Charles Sercy | Brother — estate planning | csercy@outlook.com |
| Nimrat Samra | MMM Trucking CEO | — |
| Matthew Bauer | HP Hood — May 1 deadline | — |
| Gordy Schulze | Stemilt — warm intro via Brendan | — |

---

## Environment

| System | Purpose |
|---|---|
| Host machine | Personal + Veritas work only |
| VM: SecureAI-W11 | AgentOS + n8n development only |
| `C:\Users\aserc\.lux\` | Lux runtime — scripts, logs, launcher |
| alansercy/agentos | n8n automation code repo |
| alansercy/alan-os | This repo — persistent brain |
