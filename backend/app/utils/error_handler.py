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
            return "Related record does not exist or is being referenced by other records"

        case "UniqueViolationError":
            return f"A {model_name.lower()} with this value already exists"

        case "IntegrityError":
            if hasattr(exception, 'orig') and hasattr(exception.orig, 'pgcode'):
                pgcode = exception.orig.pgcode
                match pgcode:
                    case "23503":
                        return "Foreign key constraint violation. The record may not exist or is being referenced"
                    case "23505":
                        return f"Duplicate entry. A {model_name.lower()} with this value already exists"
                    case "23502":
                        return "Required field is missing or null"
                    case _:
                        return "Database integrity constraint violation"
            return "Database integrity constraint violation"

        case "ValueError":
            return f"{model_name} not found"

        case "NoResultFound":
            return f"{model_name} not found"

        case _:
            error_msg = str(exception)
            return f"An error occurred: {error_msg}" if error_msg else "Unknown error occurred"
