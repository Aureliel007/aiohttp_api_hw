import json

from aiohttp import web
from pydantic import ValidationError

from models import engine, init_orm


async def orm_context(request: web.Application):
    await init_orm()
    yield
    await engine.dispose()

def validate(json_data, schema_cls):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as e:
        errors = e.errors()
        for error in errors:
            error.pop("ctx", None)
        raise get_error(errors, web.HTTPBadRequest)

def get_error(message: dict | list | str, err_cls):
    return err_cls(text=json.dumps({"error": message}), content_type="application/json")
