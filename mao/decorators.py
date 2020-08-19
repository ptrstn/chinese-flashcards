import pandas


def non_null_call(function):
    """
    Calls the function only when the passed value is not null.
    Return the original value otherwise.
    """
    def wrapper_function(value):
        return function(value) if not pandas.isnull(value) else value
    return wrapper_function
