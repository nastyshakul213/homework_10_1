from typing import Callable, TypeVar, Any, Optional, TextIO
from functools import wraps
import sys

T = TypeVar('T')


def log(filename: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Декоратор для логирования вызовов функций.
    - При успехе: "Имя функции и результат выполнения"
    - При ошибке: "Имя функции, тип ошибки и входные параметры"
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)

        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Формируем базовую информацию о вызове
            func_info = f"{func.__name__} called with args: {args}, kwargs: {kwargs}"

            try:
                result = func(*args, **kwargs)

                # Успешное выполнение (только имя и результат)
                success_message = f"{func.__name__} returned {result}\n"

                if filename:
                    with open(filename, 'a') as file:
                        file.write(success_message)
                else:
                    sys.stdout.write(success_message)

                return result

            except Exception as e:
                # Ошибка (имя, тип ошибки и параметры)
                error_message = (
                    f"{func.__name__} raised {type(e).__name__} "
                    f"with args: {args}, kwargs: {kwargs}\n"
                )

                if filename:
                    with open(filename, 'a') as file:
                        file.write(error_message)
                else:
                    sys.stderr.write(error_message)

                raise

        return wrapper

    return decorator
