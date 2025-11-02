from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from fastapi import status


def get_exception_status_code(exception) -> int:
    exception_type = type(exception).__name__

    match exception_type:
        case "ValueError":
            error_msg = str(exception).lower()
            if "invalid" in error_msg or "password" in error_msg or "username" in error_msg:
                return status.HTTP_401_UNAUTHORIZED
            return status.HTTP_404_NOT_FOUND
        case "NoResultFound":
            return status.HTTP_404_NOT_FOUND
        case "IntegrityError" | "ForeignKeyViolationError" | "UniqueViolationError":
            return status.HTTP_409_CONFLICT
        case _:
            return status.HTTP_500_INTERNAL_SERVER_ERROR


def get_db_error_message(exception, model_name: str = "This record") -> str:
    exception_type = type(exception).__name__

    match exception_type:
        case "ForeignKeyViolationError":
            return "Cannot delete, record is being used by other data"

        case "UniqueViolationError":
            return f"{model_name} already exists with this value"

        case "IntegrityError":
            if hasattr(exception, 'orig') and hasattr(exception.orig, 'pgcode'):
                pgcode = exception.orig.pgcode
                if pgcode == "23503":
                    return "Cannot delete or update, record is linked to other data"
                elif pgcode == "23505":
                    return f"{model_name} already exists"
                elif pgcode == "23502":
                    return "Required field cannot be empty"
                return "Database constraint violation"
            return "Database constraint violation"

        case "ValueError":
            return f"{model_name} not found"

        case "NoResultFound":
            return f"{model_name} not found"

        case _:
            error_msg = str(exception)
            return error_msg if error_msg else "Database error"
