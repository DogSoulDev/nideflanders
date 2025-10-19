"""Fetch Tor relays from Onionoo (Tor Project) and update `config/nodes.yml`.

This uses Onionoo's summary endpoint to obtain relays ordered by consensus
weight and writes a compact set of entries into `config/nodes.yml` under
`tor_relays:`. This is best-effort and intended to help initial configuration.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from typing import List, Dict

ONIONOO_SUMMARY = 'https://onionoo.torproject.org/summary?limit={limit}&order=consensus_weight'
NODES_YML = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'nodes.yml')


def fetch_top_relays(_limit: int = 50) -> List[Dict]:
    url = ONIONOO_SUMMARY.format(limit=_limit)
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            data = json.load(r)
    except (urllib.error.URLError, ValueError, TimeoutError, OSError) as e:  # best-effort fetch
        print('Error fetching Onionoo:', e)
        return []

    relays = []
    for r in data.get('relays', [])[:_limit]:
        fp = r.get('fingerprint')
        nick = r.get('nickname') or ''
        country = r.get('country') or ''
        or_addresses = r.get('or_addresses', [])
        ip = ''
        if or_addresses:
            # first OR address looks like '1.2.3.4:9001'
            ip = or_addresses[0].split(':', 1)[0]
        relays.append({'nickname': nick, 'fingerprint': fp, 'ip': ip, 'country': country, 'source': 'onionoo'})
    return relays


def update_nodes_yaml(relays: List[Dict]) -> None:
    if not os.path.isfile(NODES_YML):
        print('No se encontró', NODES_YML)
        sys.exit(1)
    with open(NODES_YML, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find where to insert under 'tor_relays:' (before 'bridges:' section)
    try:
        bridges_idx = next(i for i, l in enumerate(lines) if l.strip().startswith('bridges:'))
    except StopIteration:
        bridges_idx = len(lines)

    body: list[str] = []
    for r in relays:
        if not r.get('fingerprint'):
            continue
        nickname = r.get('nickname') or 'unknown'
        fp = r.get('fingerprint')
        ip = r.get('ip') or ''
        country = r.get('country') or ''
        entry = f"  - nickname: \"{nickname}\"\n    fingerprint: \"{fp}\"\n    ip: \"{ip}\"\n    country: \"{country}\"\n    source: \"onionoo\"\n"
        body.append(entry)

    new_lines = []
    inserted = False
    for idx, line in enumerate(lines):
        if idx == 0:
            new_lines.append(line)
            continue
        if idx == bridges_idx and not inserted:
            # ensure tor_relays header exists
            new_lines.append('tor_relays:\n')
            for e in body:
                new_lines.append(e)
            inserted = True
        new_lines.append(line)

    if not inserted:
        # append at end
        new_lines.append('\n')
        new_lines.append('tor_relays:\n')
        for e in body:
            new_lines.append(e)

    with open(NODES_YML, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print('Updated', NODES_YML, 'with', len(body), 'relays')


def main() -> int:
    relays = fetch_top_relays()
    update_nodes_yaml(relays)
    return 0


if __name__ == '__main__':
    sys.exit(main())
