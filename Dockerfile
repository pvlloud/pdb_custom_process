FROM python:3.13-slim

ENV PYTHONDONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/
WORKDIR /src
COPY . /src/
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  pkg-config \
  wait-for-it \
  git \
  cmake \
  libssl-dev \
  libffi-dev \
  libxml2-dev \
  libxslt1-dev \
  zlib1g-dev \
  wget \
  && rm -rf /var/lib/apt/lists/*

RUN uv sync --frozen --no-install-project --no-dev

# pre-load model ProtT5
RUN uv run python -c "\
from transformers import T5Tokenizer, T5EncoderModel; \
model_name = 'Rostlab/prot_t5_xl_uniref50'; \
T5Tokenizer.from_pretrained(model_name); \
T5EncoderModel.from_pretrained(model_name)"

# Start CLI script
CMD ["uv", "run", "python", "cli.py"]