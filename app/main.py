from aiohttp import web

# from app import create_app

from middlewares import session_middleware, jwt_middleware
from tools import orm_context
from views import AdsView, UserView, login


app = web.Application(middlewares=[session_middleware, jwt_middleware])
app.cleanup_ctx.append(orm_context)

app.add_routes(
    [
        web.post("/login", login),
        web.get("/user/{user_id:\d+}", UserView),
        web.post("/user", UserView),
        web.get("/ads/{ads_id:\d+}", AdsView),
        web.post("/ads", AdsView),
        web.patch("/ads/{ads_id:\d+}", AdsView),
        web.delete("/ads/{ads_id:\d+}", AdsView),
    ]
)


if __name__ == "__main__":
    web.run_app(app)
