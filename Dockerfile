# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking
ENV UV_LINK_MODE=copy

# Install dependencies first (better caching)
# TODO: remove group ci and use uvx instead
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=app/uv.lock,target=uv.lock \
    --mount=type=bind,source=app/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --group ci --all-extras

# Copy the application code
COPY app/ /app/

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --group ci --all-extras

# Place /app/.venv/bin at the beginning of PATH
ENV PATH="/app/.venv/bin:$PATH"

# Default command: run bruin
ENTRYPOINT ["bruin"]
CMD ["run", "."]
