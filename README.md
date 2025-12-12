# wikidata-qcode-resolver
This repository contains a Python script that retrieves Wikidata Q-codes based on external identifiers from any Wikidata property. The script reads external URLs from a CSV, extracts their identifiers, and queries the Wikidata SPARQL endpoint in rate-limited batches. For each match, it outputs the Q-code, label, and description to a results CSV.
