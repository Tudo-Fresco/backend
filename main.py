from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.api_router_builder import ApiRouterBuilder
from api.shared.env_variable_manager import EnvVariableManager
from api.shared.logger import Logger
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.exception_handlers import http_exception_handler


logger = Logger('Tudo Fresco API')

def create_app() -> FastAPI:
    logger.log_info('Starting FastAPI application')
    env = EnvVariableManager()
    allowed_methods = env.load('ALLOWED_METHODS', '*').string().split(',')
    allowed_origins = env.load('ALLOWED_ORIGINS', 'http://localhost:5173').string().split(',')
    allow_credentials = env.load('ALLOW_CREDENTALS', True).boolean()
    allow_headers = env.load('ALLOW_CREDENTALS_HEADERS', '*').string().split(',')
    app = FastAPI(
        title='Tudo Fresco API',
        version='1.0.0'
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=allow_credentials,
        allow_methods=allowed_methods,
        allow_headers=allow_headers,
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
    env = EnvVariableManager()
    app_ip = env.load('APP_IP', '0.0.0.0').string()
    app_port = env.load('APP_PORT', 8080).integer()
    app = create_app()
    uvicorn.run(app, host=app_ip, port=app_port)