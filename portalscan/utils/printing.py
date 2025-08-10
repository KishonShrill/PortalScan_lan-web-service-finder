from colorama import Fore, Style

def print_line(text, color=Fore.YELLOW, symbol="*"):
    print(f"{color}[{symbol}] {Style.RESET_ALL}{text}")


def print_boxed(text, color=Fore.CYAN, padding_inline=0, padding_left=0):
    lines = text.split('\n')
    width = max(len(line) for line in lines) + padding_inline
    print(color + (" " * padding_left) + "╔" + "═" * (width + 2) + "╗")
    for line in lines:
        print(color + (" " * padding_left) + f"║ {line.ljust(width)} ║")
    print(color + (" " * padding_left) + "╚" + "═" * (width + 2) + "╝" + Style.RESET_ALL)


def print_columns(items, columns=4, color=Fore.GREEN):
    col_width = max(len(str(item)) for item in items) + 16
    for i in range(0, len(items), columns):
        row_items = []
        for j in range(columns):
            if i + j < len(items):
                idx = i + j + 1
                row_items.append(f"{color}[{idx}]{Style.RESET_ALL} {items[i+j]}".ljust(col_width))
        print("".join(row_items))