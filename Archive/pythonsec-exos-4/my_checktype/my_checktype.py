import functools
import inspect

def checktypes(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        
        bound_args = sig.bind(*args, **kwargs)
        for param_name, value in bound_args.arguments.items():
            param = sig.parameters[param_name]
            if param.annotation != inspect.Parameter.empty:
                expected_type = param.annotation
                if not isinstance(value, expected_type):
                    raise Exception(
                        f"f: wrong type of '{param_name}' argument, "
                        f"'{expected_type.__name__}' expected, "
                        f"got '{type(value).__name__}'"
                    )
        
        result = func(*args, **kwargs)
        
        return_annotation = sig.return_annotation
        if return_annotation != inspect.Parameter.empty:
            if not isinstance(result, return_annotation):
                raise Exception(
                    f"f: wrong return type, '{return_annotation.__name__}' expected, "
                    f"got '{type(result).__name__}'"
                )
        
        return result
    
    return wrapper
