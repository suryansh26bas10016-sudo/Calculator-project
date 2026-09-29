import addition
import subtraction
import multiplication
import division
import reset
import cmath
import calculator_gui

# Initializing global calculation states
first_number = 0.0 + 0j
current_operator = None  # Stores the operator until '=' is pressed
start = True

def get_current_result():
    global first_number
    return first_number

def process_operation(operator, screen_value):
    """
    Exposes the existing calculation backend to the GUI layout module.
    Correctly follows: Input 1 -> Operator -> Input 2 -> Equal (=) -> Result.
    """
    global first_number, current_operator, start
    
    # 1. Clear Operation
    if operator == "CLEAR":
        try:
            reset.clear_screen()
        except AttributeError:
            pass  # Fallback if reset module doesn't have clear_screen
        first_number = 0.0 + 0j
        current_operator = None
        start = True
        return format_clean_output(first_number)
    
    # 2. Exit Operation
    elif operator == "EXIT":
        print("------- Closing the calculator -------")
        return None

    # Convert the structural string on screen layout to standard processing values safely
    try:
        y = complex(screen_value)
    except (ValueError, TypeError):
        y = 0.0 + 0j

    # 3. Basic Arithmetic Operators (+, -, *, /)
    if operator in ["+", "-", "*", "/"]:
        first_number = y             # Save the first number entered
        current_operator = operator  # Store the active operator
        start = True                 # Signal GUI to receive the second number input
        return None                  # Tells the GUI to hold current screen until typing begins

    # 4. Advanced Math Logic Routes (sin, cos, tan, log, exp)
    elif operator in ["sin", "cos", "tan", "log", "exp"]:
        try:
            if operator == "sin": res = cmath.sin(y)
            elif operator == "cos": res = cmath.cos(y)
            elif operator == "tan": res = cmath.tan(y)
            elif operator == "log": res = cmath.log(y)
            elif operator == "exp": res = cmath.exp(y)
        except Exception:
            res = 0.0 + 0j
        
        if res is None:
            res = 0.0 + 0j
            
        first_number = res
        start = True
        return format_clean_output(res)

    # 5. Equal Button Evaluation Route
    elif operator == "=":
        if current_operator:
            # Calculate using the stored first number and the current screen input
            final_result = calculate_basic(first_number, y, current_operator)
            current_operator = None  # Clear operator chain after execution
        else:
            final_result = y
        
        first_number = final_result
        start = True  # Ready for a brand new sequence loop
        
        # Format the result clearly for terminal visualization
        clean_out = format_clean_output(final_result)
        print(f"Answer printed in terminal: {clean_out}")
        return clean_out

    return format_clean_output(first_number)

def calculate_basic(val1, val2, op):
    """Helper function to route arithmetic calculations safely without runtime exceptions."""
    try:
        if op == "+": return addition.add(val1, val2)
        elif op == "-": return subtraction.subt(val1, val2)
        elif op == "*": return multiplication.multiply(val1, val2)
        elif op == "/": 
            if val2 == 0:
                print("Runtime Warning: Division by zero avoided.")
                return 0.0 + 0j
            return division.divide(val1, val2)
    except Exception as e:
        print(f"Calculation error handled: {e}")
    return val2

def format_clean_output(val):
    """Formats complex numbers to drop decimal points or imaginary tails if flat zero."""
    if isinstance(val, complex):
        if val.imag == 0:
            return int(val.real) if val.real.is_integer() else val.real
        return val
    return val

if __name__ == "__main__":
    print("============== MY CALCULATOR (GUI BACKEND) ==============")
    calculator_gui.start_gui(process_operation, None, get_current_result)
