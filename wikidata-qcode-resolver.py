#!/usr/bin/env python3
"""
Resolve Wikidata Q-ids for external identifiers (e.g. RKD, ULAN, CERL) using SPARQL.
"""

import csv  # CSV module to read and write CSV files.
import time # Used for inserting delays between batches (helps avoid rate limiting).
from argparse import ArgumentParser # Parses command-line arguments such as --property.
import requests # Used to send HTTP requests to the Wikidata SPARQL endpoint.

def extract_id_from_uri(uri: str) -> str:   # Removes trailing slash → splits URL by "/" → returns last segment (usually the numeric ID).
    return uri.rstrip('/').split('/')[-1]

def get_qcodes_from_external_uris(property_id: str, batch_size: int = 50, pause_sec: float = 0.5):  # Main function that performs SPARQL lookups.
    endpoint = "https://query.wikidata.org/sparql"
    csv_file = "source.csv"
    output_csv = "results.csv"

    # Read the input CSV and store all rows in a list.
    entries = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append({'recordnumber': row['recordnumber'], 'external_uri': row['external_uri']})

    # Open output CSV and write header.
    with open(output_csv, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['recordnumber', 'external_uri', 'qcode', 'full_q_link'])

        # Process entries in batches to avoid overloading the SPARQL endpoint.
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i+batch_size]

            # Extract IDs from the external URLs.
            ids = [extract_id_from_uri(e['external_uri']) for e in batch]
            values_str = " ".join(f'"{id_}"' for id_ in ids)

            # Build the SPARQL query for this batch.
            query = f"""
            SELECT ?item ?prop_value
            WHERE {{
                ?item wdt:{property_id} ?prop_value .
                VALUES ?prop_value {{ {values_str} }}
            }}
            """

            try:
                # Execute the SPARQL query via HTTP GET
                resp = requests.get(endpoint, params={"query": query, "format": "json"})
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"ERROR in batch {i}-{i+len(batch)}: {e}")
                continue

            # Map external IDs to Q-codes
            qcode_map = {}
            for r in data["results"]["bindings"]:
                uri_value = r["prop_value"]["value"]
                qcode = r["item"]["value"].split("/")[-1]
                qcode_map[uri_value] = qcode

            # Write results to CSV
            for e in batch:
                id_ = extract_id_from_uri(e['external_uri'])
                if id_ in qcode_map:
                    q = qcode_map[id_]
                    full_q_link = f"http://www.wikidata.org/entity/{q}"
                    print(f"{e['recordnumber']} | {e['external_uri']} → {q} ({full_q_link})")
                    writer.writerow([e['recordnumber'], e['external_uri'], q, full_q_link])
                else:
                    # No match found
                    print(f"{e['recordnumber']} | {e['external_uri']} → No Q-code found")
                    writer.writerow([e['recordnumber'], e['external_uri'], '', ''])


            # Sleep between batches to avoid being throttled.
            time.sleep(pause_sec)


# ----- CLI -----
if __name__ == "__main__":
    parser = ArgumentParser(description="Resolve Wikidata Q-ids for external identifiers (e.g. RKD, ULAN, ...)")
    # Creates the command-line argument parser.
    parser.add_argument(
        '-p', '--property',
        type=str,
        default="P650",  # Default is RKD Artists.
        help='Wikidata property ID (P245 for ULAN, P650 for RKD artists, P1871 for cerl).'
        # For other codes, run: python3 wikidata-qcode-resolver.py -p P1871
    )

    args = parser.parse_args()
    property_id = args.property

    # Start processing.
    get_qcodes_from_external_uris(property_id=property_id)