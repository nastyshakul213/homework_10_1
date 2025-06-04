from typing import Callable, TypeVar, Any, Optional
import datetime
import sys

# Тип для возвращаемого значения декорируемой функции
T = TypeVar('T')


def log(filename: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Декоратор для логирования вызовов функций."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        func

        def wrapper(*args: Any, **kwargs: Any) -> T:
            start_time = datetime.datetime.now()
            log_message = f"{start_time} - {func.__name__} started with args: {args}, kwargs: {kwargs}\n"

            # Фиксируем в файл или в консоль
            if filename:
                with open(filename, 'a') as file:
                    file.write(log_message)
            else:
                sys.stdout.write(log_message)

            try:
                result = func(*args, **kwargs)
                end_time = datetime.datetime.now()
                duration = end_time - start_time
                success_message = (
                    f"{end_time} - {func.__name__} finished successfully. "
                    f"Result: {result}. Execution time: {duration}\n"
                )

                if filename:
                    with open(filename, 'a') as file:
                        file.write(success_message)
                else:
                    sys.stdout.write(success_message)

                return result

            except Exception as e:
                end_time = datetime.datetime.now()
                duration = end_time - start_time
                error_message = (
                    f"{end_time} - {func.__name__} failed with error: {type(e).__name__}: {str(e)}. "
                    f"Args: {args}, kwargs: {kwargs}. Execution time: {duration}\n"
                )

                if filename:
                    with open(filename, 'a') as file:
                        file.write(error_message)
                else:
                    sys.stderr.write(error_message)

                raise

        return wrapper

    return decorator
