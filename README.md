# Wikidata Q-code Resolver

This script resolves Wikidata Q-codes for external identifiers (e.g., RKD, ULAN, CERL) provided in a CSV file. It processes the identifiers in batches to avoid overloading the Wikidata SPARQL endpoint and writes the results to a CSV file while printing them to the terminal. It is designed for batch processing and is particularly useful for collection management, data enrichment, and authority control workflows.

## What does this script do?

* Reads a CSV file named `source.csv` with columns `recordnumber` and `external_uri`.
* Extracts numeric IDs from the external URIs (e.g., RKD, ULAN, CERL).
* Queries the Wikidata SPARQL endpoint to retrieve the corresponding Q-codes.
* Processes the identifiers in configurable batch sizes.
* Writes the results to an output CSV file `results.csv` with columns `recordnumber`, `external_uri`, `qcode`, and `full_q_link`.
* Prints each result to the terminal.

## Features

* Handles large batches of external identifiers.
* Avoids overloading Wikidata with a configurable pause between batches.
* Supports any Wikidata property (P-code) by including the `P` prefix.
* Clearly indicates if a Q-code is found or missing.
* Outputs results in CSV format ready for further processing.

## Input format

The input CSV must be named `source.csv` and have the following columns:

* **Column A (`recordnumber`)**: your internal record number or identifier.
* **Column B (`external_uri`)**: the URL of the external authority identifier.

Example:

```csv
recordnumber,external_uri
32569,https://rkd.nl/artists/440559
32570,http://vocab.getty.edu/ulan/500115588
3604,cnp01905094
```
> The script automatically extracts the last segment of `external_uri` as the identifier to query Wikidata.
## Supported Properties (P-codes)

| Property | Authority   | Notes |
|----------|------------|----------|
| P650     | RKD Artists | Default property |
| P245     | ULAN        | Use `-p P245` to query |
| P1871    | CERL        | Use `-p P1871` to query |

If no Q-code is found for a given external ID, both `qcode` and `full_q_link` will be empty.

Other Wikidata P-codes can also be used by specifying them with the `-p` argument.

## Requirements

- Python 3.9 or higher
- Python packages:

```bash
pip install requests
```

> **Note:** An active internet connection is required, as the script queries the Wikidata SPARQL endpoint.

## Usage

Run the script via the command line:

```bash
python wikidata-qcode-resolver.py -p P650
```

`-p`, `--property`: the Wikidata property ID to query. Always include the `P` prefix.  
If no property is specified, it defaults to P650 (RKD Artists).

To retrieve other identifiers, simply change the P-code:

- ULAN: `-p P245`
- CERL: `-p P1871`

## Output

The output CSV `results.csv` contains:

```csv
recordnumber,external_uri,qcode,full_q_link
32569,https://rkd.nl/artists/440559,Q12345,http://www.wikidata.org/entity/Q12345
32570,http://vocab.getty.edu/ulan/500115588,Q67890,http://www.wikidata.org/entity/Q67890
```

If no match is found, the `qcode` and `full_q_link` columns will be empty.

All results are also printed in the terminal.

## Typical workflow

1. Prepare `source.csv` with your external identifiers and record numbers.  
2. Run the script with the desired Wikidata property using the `-p` argument.  
3. Review the `results.csv` file for found or missing Q-codes.

## Recommended project structure
```
wikidata-qcode-resolver/
│
├── wikidata-qcode-resolver.py
├── source.csv
├── results.csv
└── README.md
```

## Contributing

Contributions, improvements, and bug fixes are welcome. Please provide clear commit messages and usage examples.

## License

This project is released under the **CC0 1.0 Universal (CC0 1.0) Public Domain Dedication**.  
You are free to copy, modify, distribute, and use this work, even for commercial purposes, without asking for permission. No attribution is required.

**Author:** Jeroen De Meester  
**Repository:** [https://github.com/Jeroen-DeMeester/wikidata-qcode-resolver](https://github.com/Jeroen-DeMeester/wikidata-qcode-resolver)