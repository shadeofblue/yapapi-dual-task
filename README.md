# yapapi-dual-task

Just a test app to verify feasibility of launching golem tasks from a HTTP server (in this case, django)

## Installation

First, create and activate some virtual environment...

### Install the requirements

Ensure you have python>=3.8 and poetry, then:

`poetry install`

### Provide your `YAGNA_APPKEY`

Inside `yapapi_dual_task`, beside the usual `settings.py`,
create a `settings_local.py` with a single entry of:

```python
YAGNA_APPKEY = "your-yagna-appkey"
```

## Running

From project's root:

`gunicorn yapapi_dual_task.asgi:application -k uvicorn.workers.UvicornWorker`
