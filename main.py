from fastapi import FastAPI
from api.api_router_builder import ApiRouterBuilder
from api.shared.logger import Logger
import uvicorn

logger = Logger('Tudo Fresco API')

def create_app() -> FastAPI:
    logger.log_info('Starting FastAPI application')
    app = FastAPI(
        title='Tudo Fresco API',
        version='1.0.0'
    )
    router_builder = ApiRouterBuilder()
    routers = router_builder.build()
    for router in routers:
        logger.log_debug(f'Including router: {router.prefix}')
        app.include_router(router)
    logger.log_info('All routers included. App is ready.')
    return app

if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host='0.0.0.0', port=8777)