# Common response method
def res(data=None, message='Ok', success=True, code=200):
    """
    Generate a common response dictionary.

    Parameters:
    - data: The data to include in the response.
    - message: A message describing the response.
    - success: A boolean indicating whether the operation was successful.
    - code: The HTTP status code.

    Returns:
    A dictionary containing the response information.
    """
    return {
        'success': success,
        'message': message,
        'data': data,
    }, code

# datetime 转换格式
def format_datetime_to_json(datetime, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strftime(format)

def res2(data=None, message='Ok', success=True, code=200):
    """
    Generate a common response dictionary with a less nested structure.

    Parameters:
    - data: The data to include in the response. Expected to be a dictionary.
    - message: A message describing the response.
    - success: A boolean indicating whether the operation was successful.
    - code: The HTTP status code.

    Returns:
    A dictionary containing the response information.
    """
    response = {
        'success': success,
        'message': message
    }
    if data is not None:
        response.update(data)  # Merge data into the response

    return response, code