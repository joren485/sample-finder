import sys
from pathlib import Path
from typing import Annotated

import typer
import yaml
from loguru import logger

from sample_finder.sources.source import Source

app = typer.Typer(name="Malware Sample Finder")


def read_hashes(input_file: Path) -> dict[str, bool]:
    """Read hashes from a file."""
    hashes = {}
    with input_file.open("r") as h_files:
        for line in h_files:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if not Source.supported_hash(line):
                logger.warning(f"Invalid hash: '{line}'")

            hashes[line] = False
    return hashes


@app.command()
def find_samples(
    input_file: Annotated[
        Path, typer.Option("--input", "-i", exists=True, dir_okay=False, file_okay=True, readable=True)
    ],
    output_dir: Annotated[
        Path, typer.Option("--output", "-o", exists=True, dir_okay=True, file_okay=False, writable=True)
    ],
    config_file: Annotated[
        Path, typer.Option("--config", "-c", exists=True, dir_okay=False, file_okay=True, readable=True)
    ] = Path("./config.yaml"),
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Download hashes from multiple sources."""
    with config_file.open("r") as h_file:
        config = yaml.safe_load(h_file)

    hashes = read_hashes(input_file)

    logger.remove()
    if verbose:
        logger.add(sys.stdout, level="DEBUG")
    else:
        logger.add(sys.stdout, level="INFO")

    for source_name, source_config in config["sources"].items():
        try:
            source = Source.get_source(source_name, source_config)
        except ValueError as e:
            logger.warning(f"Could not load source {source_name}: {e}")
            continue
        logger.info(f"Source: {source.NAME}")

        for h in hashes:
            if hashes[h]:
                logger.debug(f"Skipping previously downloaded sample: '{h}'")
                continue

            if not source.supported_hash(h):
                logger.debug(f"Skipping unsupported hash: '{h}'")
                continue

            logger.info(f"Searching for: '{h}'")

            output_path_sample = output_dir / f"{h}.bin"
            try:
                download_success = source.download_file(sample_hash=h, output_path=output_path_sample)
            except Exception as e:
                logger.warning(f"Error: {e}")
                continue

            if download_success:
                logger.success(f"Downloaded '{h}' to {output_path_sample}")
                hashes[h] = True
            else:
                logger.warning(f"Did not find '{h}'")


if __name__ == "__main__":
    app()
