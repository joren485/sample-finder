# Sample Finder

Sample Finder is a modular tool to search for and download malware samples from public malware sources.

### Supported sources
* [Malpedia](https://malpedia.caad.fkie.fraunhofer.de/)
* [MalShare](https://malshare.com/)
* [Malware Bazaar](https://bazaar.abuse.ch/)
* [VirusShare](https://virusshare.com/)
* [VirusTotal](https://www.virustotal.com)

### Installation
```bash
$ git clone git@github.com:joren485/sample-finder.git
$ cd sample-finder
$ poetry install
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
