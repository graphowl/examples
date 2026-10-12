"""Ask GraphOWL a SPARQL question from Python, using only the standard library.

    export GRAPHOWL_URL=https://your-graphowl-host
    export GRAPHOWL_TOKEN=...
    python query.py                      # counts instances per class, now
    python query.py --as-of 2026-10-01T00:00:00Z

Imported facts live in named graphs, so patterns over them sit inside GRAPH ?g { ... }.
The request body is {"query": "...", "asOf": "<RFC 3339 timestamp>"}; leave asOf out for the present.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_QUERY = """
SELECT ?class (COUNT(?s) AS ?instances)
WHERE { GRAPH ?g { ?s a ?class } }
GROUP BY ?class
ORDER BY DESC(?instances)
LIMIT 20
"""


def ask(base_url, token, query, as_of):
    body = {"query": query, **({"asOf": as_of} if as_of else {})}
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/sparql",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        sys.exit(f"{error.code}: {error.read().decode()[:500]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--as-of")
    args = parser.parse_args()
    print(json.dumps(ask(os.environ["GRAPHOWL_URL"], os.environ["GRAPHOWL_TOKEN"], args.query, args.as_of), indent=2))


main()
