# data-eng-zoomcamp-2026-project
Data engineering zoomcamp project - MMA stats

## NB 
- iac should be an external repository; for the sake of simplicity, I've included it in this project


## Set-up
- install uv
`pip install uv`

- install bruin
```
curl -LsSf https://getbruin.com/install/cli | sh
source ~/.bashrc
```
- install dependencies
`uv sync --dev`

- install bruin mcp (e.g on workspace)
```
{
  "servers": {
    "bruin": {
      "type": "stdio",
      "command": "bruin",
      "args": [
        "mcp"
      ]
    }
  },
  "inputs": []
}
```

## Useful devEx commands
typing
```
uv run ty check
```

linting and formating
```
uv run ruff check --fix # lint
uv run ruff format # formating
```

bruin format sql & assets def
```
uv run bruin format app/ --sqlfluff
```

bruin validate
```
bruin validate app/
```

install pre-commit
```
uv --directory app run prek install
```
