from fastapi.responses import JSONResponse

def success_response(data=None, message="Operation successful", status_code=200):
    """
    Generates a standardized success response.

    :param data: The response data (default: None)
    :param message: A custom success message (default: "Operation successful")
    :param status_code: The HTTP status code (default: 200)
    :return: JSONResponse with the standardized format
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "data": data,
        },
    )

def error_response(message="An error occurred", status_code=400, details=None):
    """
    Generates a standardized error response.

    :param message: A custom error message (default: "An error occurred")
    :param status_code: The HTTP status code (default: 400)
    :param details: Optional detailed error information (default: None)
    :return: JSONResponse with the standardized error format
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "data": details,
        },
    )