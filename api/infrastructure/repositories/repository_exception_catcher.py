import traceback
from functools import wraps

class RepositoryExceptionCatcher:

    def __init__(self, repository_name: str) -> None:
        from api.shared.logger import Logger
        self.repository_name = repository_name
        self.logger = Logger(self.repository_name)

    def __call__(self, func):
        @wraps(func)
        async def wrapper(repo_self, *args, **kwargs):
            try:
                return await func(repo_self, *args, **kwargs)
            except Exception as e:
                self.logger.log_error(f'Error in {func.__name__}: {e}')
                self.logger.log_debug(f'Traceback: {traceback.format_exc()}')
                if hasattr(repo_self, 'session') and repo_self.session:
                    try:
                        await repo_self.session.rollback()
                        self.logger.log_debug('Session rollback successful')
                    except Exception as rollback_error:
                        self.logger.log_error(f'Rollback failed: {rollback_error}')
                raise
        return wrapper
