# Sample Finder

Sample Finder is a modular tool to search for and download malware samples from public malware sources.

### Supported sources
* [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/)
* [MalShare](https://malshare.com/)
* [Malware Bazaar](https://bazaar.abuse.ch/)
* [MWDB](https://mwdb.cert.pl/)
* [Triage](https://tria.ge/)
* [VirusExchange](https://virus.exchange)
* [VirusShare](https://virusshare.com/)
* [VirusTotal](https://www.virustotal.com) (only checks if the sample is available on VirusTotal and does not support downloading)

### Installation
#### Pip
```bash
$ pip install sample-finder
```

#### Development
```bash
$ git clone git@github.com:joren485/sample-finder.git
$ cd sample-finder
$ uv sync
$ source .venv/bin/activate
$ sample-finder --help
```

### Config
You need a config file with API tokens for each supported source.
You can find an example in `example.confg.yaml`:
```yaml
---

sources:
  malshare:
    api_key: "API KEY"
  malpedia:
    api_key: "API KEY"
  malwarebazaar:
    api_key: "API KEY"
  virusshare:
    api_key: "API KEY"
  virustotal:
    api_key: "API KEY"
  triage:
    api_key: "API KEY"
  virusexchange:
    api_key: "API KEY"
```

### Usage
```bash
$ sample-finder --help
 Usage: sample-finder [OPTIONS]

 Download hashes from multiple sources.

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --input               -i      FILE       [default: None] [required]                                                                                                                                         │
│ *  --output              -o      DIRECTORY  [default: None] [required]                                                                                                                                         │
│    --config              -c      FILE       [default: config.yaml]                                                                                                                                             │
│    --verbose             -v                                                                                                                                                                                    │
│    --install-completion                     Install completion for the current shell.                                                                                                                          │
│    --show-completion                        Show completion for the current shell, to copy it or customize the installation.                                                                                   │
│    --help                                   Show this message and exit.                                                                                                                                        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
