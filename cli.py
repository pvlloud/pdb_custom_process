# cli.py
import click
from celery import chain
from environs import Env

from tasks import extract_chains_from_pdb, run_model_on_chains

env = Env()


@click.group()
def cli():
    pass


@click.command()
@click.argument("input_file_name")
@click.argument("chains_lookup_list", nargs=-1)
def extract_chain(input_file_name, chains_lookup_list):
    """Extract chains from a PDB file."""
    extract_chains_from_pdb.delay(input_file_name, list(chains_lookup_list))


@click.command()
@click.argument("chains_file_name")
def run_model(chains_file_name):
    """Run the model."""
    # Implement the logic to run the model here
    run_model_on_chains.delay(chains_file_name)


@click.command()
@click.argument("input_file_name")
@click.argument("chains_lookup_list", nargs=-1)
def run_pipeline(input_file_name, chains_lookup_list):
    """Run the pipeline."""
    workflow = chain(
        extract_chains_from_pdb.s(input_file_name, list(chains_lookup_list)),
        run_model_on_chains.s(),
    )
    workflow()


cli.add_command(extract_chain)
cli.add_command(run_model)
cli.add_command(run_pipeline)

if __name__ == "__main__":
    cli()
