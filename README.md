## Installation

There is docker used to set up project environment. To set up project perform next steps:

1. Install [docker](https://docs.docker.com/engine/installation/) and
   [docker compose](https://docs.docker.com/compose/install/)

2. To run the application execute:
```bash
$ docker compose up --build
```
## Invocation

The `cli` service in the compose file is used to run the pipeline. The command to run the pipeline is as follows:

```bash
$ docker compose run cli run-pipeline <PDB_FILE> <CHAIN1> <CHAIN2> ...
```

The file `<PDB_FILE>` should be located in the `input_files` directory, and the output will be saved in the `output_files` directory.
Command Example:
```bash
$ docker compose run cli uv run cli.py run-pipeline 1bey.pdb H L
```

The command to only extract chains is as follows:
```bash
$ docker compose run cli extract-chain <PDB_FILE> <CHAIN1> <CHAIN2> ...
```

The command to only run model is as follows:
```bash
$ docker compose run cli run-model <CHAIN_FILE>
```
The file `<CHAIN_FILE>` should be located in the `output_files` directory, and the output will be saved in the `output_files` directory.

## Workflow Overview

Schema of the workflow from a PDB file to the model prediction, reflecting that `extract_chains_from_pdb` accepts a PDB file as input:

1. **Input PDB File**: The process starts with an input PDB file containing protein structure data.

2. **CLI Command**: The user triggers the workflow using the `run_pipeline` command in the CLI, providing the PDB file name and a list of chains to extract.

3. **Celery Task - `extract_chains_from_pdb`**:
   - **File Provider**: Reads the PDB file from the input directory.
   - **PDB Processor**: Extracts the specified chains from the PDB file.
   - **File Exporter**: Writes the extracted chains data to an output file.

4. **Output Chains File**: The result of the `extract_chains_from_pdb` task is an output file containing the extracted chains.

5. **Celery Task - `run_model_on_chains`**:
   - **Chain Provider**: Reads the chains data from the output file.
   - **Model Executor**: Processes each chain using the T5 model to generate predictions.
   - **Prediction Exporter**: Writes the prediction results to an output file.

6. **Output Prediction File**: The final result is an output file containing the model predictions for each chain.

Here is a visual representation of the workflow:

```
Full Pipeline Workflow     Model Prediction Workflow   Chain Extraction Workflow
 +------------------+        +------------------+        +------------------+
 |  Input PDB File  |        |  Output Chains   |        |  Input PDB File  |
 |                  |        |      File        |        |                  |
 +--------+---------+        +--------+---------+        +--------+---------+
          |                           |                           |
          v                           v                           v
 +--------+---------+        +--------+---------+        +--------+---------+
 |  CLI Command     |        |  Celery Task     |        |  Celery Task     |
 |  run_pipeline    |        |  run_model_on_   |        |  extract_chains_ |
 |                  |        |  chains          |        |  from_pdb        |
 +--------+---------+        +--------+---------+        +--------+---------+
          |                           |                           |
          v                           v                           v
 +--------+---------+        +--------+---------+        +--------+---------+
 |  Celery Task     |        |  Chain Provider  |        |  File Provider   |
 |  extract_chains_ |        |                  |        |                  |
 |  from_pdb        |        +--------+---------+        +--------+---------+
 +--------+---------+                 |                           |
          |                           v                           v
          v                  +--------+---------+        +--------+---------+
 +--------+---------+        |  Model Executor  |        |  PDB Processor   |
 |  PDB Processor   |        |                  |        |                  |
 |                  |        +--------+---------+        +--------+---------+
 +--------+---------+                 |                           |
          |                           v                           v
          v                  +--------+---------+        +--------+---------+
 +--------+---------+        |  Prediction      |        |  File Exporter   |
 |  File Exporter   |        |  Exporter        |        |                  |
 |                  |        +--------+---------+        +--------+---------+
 +--------+---------+                 |                           |
          |                           v                           v
          v                +----------+----------+       +--------+---------+
 +--------+---------+      |  Output Prediction  |       |  Output Chains   |
 |  Output Chains   |      |  File               |       |  File            |
 |  File            |      +---------------------+       +------------------+
 +------------------+
          |
          v
 +--------+---------+
 |  Celery Task     |
 |  run_model_on_   |
 |  chains          |
 +--------+---------+
          |
          v
 +--------+---------+
 |  Chain Provider  |
 |                  |
 +--------+---------+
          |
          v
 +--------+---------+
 |  Model Executor  |
 |                  |
 +--------+---------+
          |
          v
 +--------+---------+
 |  Prediction      |
 |  Exporter        |
 +--------+---------+
          |
          v
 +--------+------------+
 |  Output Prediction  |
 |  File               |
 +---------------------+
```