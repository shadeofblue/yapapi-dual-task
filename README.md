# yapapi-dual-task

Just a test app to verify feasibility of launching golem tasks from a HTTP server (in this case, django)

Assumes you know how to install Golem (yagna), et al blah blah blah... 
if not, consult http://handbook.golem.network ... 

## Installation

First, create and activate some virtual environment...

### Install the requirements

Ensure you have python>=3.8 and poetry, then:

`poetry install`

### Provide your `YAGNA_APPKEY` and django's `SECRET_KEY`

#### Generate your yagna appkey

`yagna app-key create requestor`

or, if you already have one

`yagna app-key list`

and copy the value from the `key` column.

#### Generate your django secret

`python -c "import secrets; print(secrets.token_urlsafe())"`

#### Add `settings_local.py`

Inside `yapapi_dual_task`, beside the usual `settings.py`,
create a `settings_local.py` with:

```python
SECRET_KEY = "your-django-secret"
YAGNA_APPKEY = "your-yagna-appkey"
```

## Running

From project's root:

`gunicorn yapapi_dual_task.asgi:application -k uvicorn.workers.UvicornWorker`
