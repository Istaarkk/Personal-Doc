import traceback

def format_table(headers, rows):
    """Formate un tableau avec des colonnes alignées."""
    column_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(cell)))
    
    row_format = " | ".join(f"{{:<{width}}}" for width in column_widths)
    
    header_line = row_format.format(*headers)
    separator = "-+-".join("-" * width for width in column_widths)
    data_lines = "\n".join(row_format.format(*[str(cell) for cell in row]) for row in rows)
    
    return f"{header_line}\n{separator}\n{data_lines}"

def debug_info_as_table():
    """Capture et affiche les détails d'une exception sous forme de tableaux alignés."""
    try:
        exc_type, exc_value, exc_traceback = traceback.sys.exc_info()
        stack_summary = traceback.extract_tb(exc_traceback)
        
        error_details = [
            [call.filename, call.lineno, call.name, call.line.strip()]
            for call in stack_summary
        ]
        error_table = format_table(
            headers=["File", "Line", "Function", "Code"],
            rows=error_details
        )
        
        frame = exc_traceback.tb_frame
        locals_data = [[k, repr(v)] for k, v in frame.f_locals.items()]
        locals_table = format_table(
            headers=["Variable", "Value"],
            rows=locals_data
        )
        
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