from tabulate import tabulate
import traceback

def debug_info_as_table():
    try:
        exc_type, exc_value, exc_traceback = traceback.sys.exc_info()
        stack_summary = traceback.extract_tb(exc_traceback)
        
        error_details = []
        for call in stack_summary:
            error_details.append(
                [call.filename, call.lineno, call.name, call.line]
            )
        
        error_table = tabulate(
            error_details, headers=["File", "Line", "Function", "Code"], tablefmt="grid"
        )
        
        frame = exc_traceback.tb_frame
        locals_data = frame.f_locals.items()
        variables_table = [["Variable", "Value"]] + [[k, repr(v)] for k, v in locals_data]
        locals_table = tabulate(variables_table, headers="firstrow", tablefmt="grid")
        
        return f"\n--- Stack Trace ---\n{error_table}\n\n--- Local Variables ---\n{locals_table}"
    except Exception as e:
        return f"Erreur dans debug_info_as_table : {e}"

def monitored_function(func):
    """Décorateur pour surveiller les exceptions dans les fonctions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            print(f"Erreur détectée dans {func.__name__}:")
            print(debug_info_as_table())
            raise 
    return wrapper

@monitored_function
def function_a():
    a = 10
    b = 0
    result = a / b  

@monitored_function
def function_b():
    x = [1, 2, 3]
    print(x[5])  

def main():
    try:
        function_a()
        function_b()
    except Exception as e:
        print("Erreur détectée dans le main:")
        print(debug_info_as_table())

main()
