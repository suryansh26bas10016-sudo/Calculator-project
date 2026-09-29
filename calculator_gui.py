import tkinter as tk

# Tracks whether the screen needs to reset when the next number button is clicked
clear_on_next_input = False

def start_gui(process_op_callback, placeholder, get_result_callback):
    """
    Builds the visual interface and handles operational sequential logic flows.
    """
    root = tk.Tk()
    root.title("Sequential Complex Calculator")
    root.geometry("380x500")
    root.configure(bg="#202020")

    screen_var = tk.StringVar(value="0")
    screen = tk.Entry(
        root, 
        textvariable=screen_var, 
        font=("Arial", 24), 
        bd=0, 
        width=14, 
        justify="right",
        bg="#202020",
        fg="#ffffff"
    )
    # Fixed the stickiness error here by changing "all" to "nsew"
    screen.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipady=15, sticky="nsew")

    def handle_click(char):
        global clear_on_next_input
        current = screen_var.get()
        
        # If an operator or evaluation was just selected, clear screen for the new input
        if clear_on_next_input:
            current = ""
            clear_on_next_input = False
            
        if current == "0" or current == "0.0":
            screen_var.set(char)
        else:
            screen_var.set(current + char)

    def handle_action(operator):
        global clear_on_next_input
        
        # Send current display value to the backend along with the selected action
        backend_result = process_op_callback(operator, screen_var.get())
        
        if operator in ["+", "-", "*", "/"]:
            # Basic operator clicked: keep current display, but clear it when user starts typing number 2
            clear_on_next_input = True
        elif backend_result is not None:
            # Equals (=), Clear, or scientific operations update the interface display directly
            screen_var.set(str(backend_result))
            clear_on_next_input = True
        else:
            root.destroy()  # Exit selected

    # Grid Button Configuration
    buttons = [
        ('CLEAR', 1, 0, '#d32f2f'), ('EXIT', 1, 1, '#f57c00'), ('log', 1, 2, '#555555'), ('exp', 1, 3, '#555555'),
        ('sin', 2, 0, '#555555'), ('cos', 2, 1, '#555555'), ('tan', 2, 2, '#555555'), ('/', 2, 3, '#ff9800'),
        ('7', 3, 0, '#333333'), ('8', 3, 1, '#333333'), ('9', 3, 2, '#333333'), ('*', 3, 3, '#ff9800'),
        ('4', 4, 0, '#333333'), ('5', 4, 1, '#333333'), ('6', 4, 2, '#333333'), ('-', 4, 3, '#ff9800'),
        ('1', 5, 0, '#333333'), ('2', 5, 1, '#333333'), ('3', 5, 2, '#333333'), ('+', 5, 3, '#ff9800'),
        ('0', 6, 0, '#333333'), ('.', 6, 1, '#333333'), ('j', 6, 2, '#333333'), ('=', 6, 3, '#4caf50')
    ]

    for (text, row, col, color) in buttons:
        if text in ['CLEAR', 'EXIT', '=', '+', '-', '*', '/', 'sin', 'cos', 'tan', 'log', 'exp']:
            action = lambda t=text: handle_action(t)
        else:
            action = lambda t=text: handle_click(t)

        btn = tk.Button(
            root, 
            text=text, 
            font=("Arial", 14, "bold"), 
            bg=color, 
            fg="#ffffff", 
            bd=0, 
            command=action
        )
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    for i in range(7):
        root.rowconfigure(i, weight=1)
    for j in range(4):
        root.columnconfigure(j, weight=1)

    root.mainloop()
