# use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# set the working directory
WORKDIR /app

# install system dependencies for Bruin
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

# install Bruin CLI
RUN curl -LsSf https://getbruin.com/install/cli | sh && \
    mv /root/.local/bin/bruin /usr/local/bin/bruin && \
    chmod +x /usr/local/bin/bruin

# enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# copy from the cache instead of linking
ENV UV_LINK_MODE=copy

# install dependencies first (better caching)
# TODO: remove group ci and use uvx instead
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=app/uv.lock,target=uv.lock \
    --mount=type=bind,source=app/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --group ci --all-extras

# copy the application code
COPY app/ /app/

# sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --group ci --all-extras

# place /app/.venv/bin at the beginning of PATH
ENV PATH="/app/.venv/bin:$PATH"

# default command: run bruin
ENTRYPOINT ["bruin"]
CMD ["run", "."]
