import tkinter as tk
import re

def evaluate_expression(expr):
    try:
        # Remove leading zeros from numbers and commas
        expr = re.sub(r'\b0+(\d)', r'\1', expr.replace(',', ''))
        # Replace custom operators with Python operators
        expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**').replace('√', 'sqrt')
        # Evaluate the expression using eval with safe scope
        result = eval(expr, {"__builtins__": None, "sqrt": lambda x: x**0.5})
        return result
    except Exception:
        return "Error"

def format_output(result):
    try:
        if isinstance(result, (int, float)):
            result_str = f"{result:,}"
            return result_str.rstrip('0').rstrip('.') if '.' in result_str else result_str
        return str(result)
    except Exception:
        return "Error"

def format_input(equation):
    try:
        # Insert commas every three digits in numbers
        parts = re.split(r'(\D)', equation)  # Split by non-digit characters
        for i, part in enumerate(parts):
            if part.isdigit():
                parts[i] = f"{int(part):,}"
        return ''.join(parts)
    except Exception:
        return equation

def update_display():
    global equation
    formatted_equation = format_input(equation)
    display_input.config(text=formatted_equation.replace('**', '^').replace('sqrt', '√'))
    result = evaluate_expression(equation + ')' * (equation.count('(') - equation.count(')')))
    if result != "Error":
        display_output.config(text=format_output(result))
    else:
        display_output.config(text="")

def button_press(value):
    global equation
    if value in '0123456789.+-×÷':
        equation += value
    elif value in '+-×÷':
        if equation and equation[-1] in '+-×÷':
            equation = equation[:-1] + value
        elif equation:
            equation += value
    elif value == 'x²':
        if equation and equation[-1] in '0123456789':
            equation += '**2'
    elif value == '√':
        if equation and (equation[-1] in '0123456789'):
            equation += '*sqrt('
        elif equation and equation[-1] in '+-×÷':
            equation += 'sqrt('
        elif not equation or equation[-1] in '()+-×÷':
            equation += 'sqrt('
    elif value == '(':
        if equation and equation[-1] in '0123456789':
            equation += '*('
        else:
            equation += '('
    elif value == ')':
        if equation and equation[-1] in '0123456789)':
            equation += ')'
    elif value == 'AC':
        equation = ""
    elif value == '←':
        if equation.endswith('sqrt('):
            equation = equation[:-5]
        elif equation.endswith('**2'):
            equation = equation[:-3]
        else:
            equation = equation[:-1]
    update_display()

def calculate():
    global equation
    if validate_start():
        result = evaluate_expression(equation + ')' * (equation.count('(') - equation.count(')')))
        if result != "Error":
            equation = format_output(result)
            display_input.config(text=equation, font=("Arial", 20))
            display_output.config(text="")
        else:
            display_output.config(text=result)

def validate_start():
    global equation
    if equation and (equation[0] in '^×÷'):
        display_output.config(text="Error")
        return False
    return True

root = tk.Tk()
root.title("Simple Calculator")
root.geometry("400x600")
root.resizable(False, False)
root.configure(bg="#17161b")

equation = ""

display_input = tk.Label(root, width=24, height=2, text="", font=("Arial", 20), bg="#17161b", fg="#ffffff", anchor='e')
display_input.pack(pady=(20, 0), padx=10, fill='x')

display_output = tk.Label(root, width=24, height=2, text="", font=("Arial", 16), bg="#17161b", fg="#ffffff", anchor='e')
display_output.pack(pady=(0, 10), padx=10, fill='x')

button_frame = tk.Frame(root, bg="#17161b")
button_frame.pack(fill='both', expand=True)

button_styles = {
    'number': {'bg': '#333333', 'fg': '#ffffff'},
    'operator': {'bg': '#c2d1f0', 'fg': '#3366cc'},
    'equals': {'bg': '#0088cc', 'fg': '#ffffff'},
    'special': {'bg': '#333333', 'fg': '#ffffff'}
}

buttons = [
    ('AC', 0, 0, lambda: button_press('AC'), 'operator', 2),
    ('←', 2, 0, lambda: button_press('←'), 'operator', 1),
    ('x²', 3, 0, lambda: button_press('x²'), 'operator', 1),
    ('7', 0, 1, lambda: button_press('7'), 'number', 1),
    ('8', 1, 1, lambda: button_press('8'), 'number', 1),
    ('9', 2, 1, lambda: button_press('9'), 'number', 1),
    ('÷', 3, 1, lambda: button_press('÷'), 'operator', 1),
    ('4', 0, 2, lambda: button_press('4'), 'number', 1),
    ('5', 1, 2, lambda: button_press('5'), 'number', 1),
    ('6', 2, 2, lambda: button_press('6'), 'number', 1),
    ('×', 3, 2, lambda: button_press('×'), 'operator', 1),
    ('1', 0, 3, lambda: button_press('1'), 'number', 1),
    ('2', 1, 3, lambda: button_press('2'), 'number', 1),
    ('3', 2, 3, lambda: button_press('3'), 'number', 1),
    ('+', 3, 3, lambda: button_press('+'), 'operator', 1),
    ('√', 0, 4, lambda: button_press('√'), 'special', 1),
    ('0', 1, 4, lambda: button_press('0'), 'number', 1),
    ('.', 2, 4, lambda: button_press('.'), 'number', 1),
    ('-', 3, 4, lambda: button_press('-'), 'operator', 1),
    ('(', 0, 5, lambda: button_press('('), 'operator', 1),
    (')', 1, 5, lambda: button_press(')'), 'operator', 1),
    ('=', 2, 5, lambda: calculate(), 'equals', 2)
]

button_width = 300 // 4
button_height = 2

for (text, col, row, command, style, col_span) in buttons:
    tk.Button(button_frame, text=text, width=button_width * col_span, height=button_height, font=("Arial", 14, "bold"), bd=1,
              fg=button_styles[style]['fg'], bg=button_styles[style]['bg'],
              command=command).grid(row=row, column=col, columnspan=col_span, sticky="nsew")

for i in range(6):
    button_frame.grid_rowconfigure(i, weight=1)
for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)

root.mainloop()
