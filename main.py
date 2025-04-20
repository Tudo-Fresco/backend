from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.api_router_builder import ApiRouterBuilder
from api.shared.logger import Logger
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.exception_handlers import http_exception_handler


logger = Logger('Tudo Fresco API')

def create_app() -> FastAPI:
    logger.log_info('Starting FastAPI application')
    app = FastAPI(
        title='Tudo Fresco API',
        version='1.0.0'
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    router_builder = ApiRouterBuilder()
    routers = router_builder.build()
    for router in routers:
        logger.log_debug(f'Including router: {router.prefix}')
        app.include_router(router)
    logger.log_info('All routers included. App is ready.')
    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: Request, exc: HTTPException):
        if isinstance(exc.detail, JSONResponse):
            return exc.detail
        return await http_exception_handler(request, exc)
    return app

if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host='0.0.0.0', port=8777)