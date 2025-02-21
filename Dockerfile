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

# Start CLI script
CMD ["uv", "run", "python", "cli.py"]