def compute_first_follow(grammar):
    def compute_first(symbol):
        if symbol.islower() or symbol == 'ε':
            return {symbol}
        if symbol not in grammar:
            return {symbol}
        if symbol in first:
            return first[symbol]
        first[symbol] = set()
        for production in grammar[symbol]:
            for s in production:
                first[symbol].update(compute_first(s))
                if 'ε' not in compute_first(s):
                    break
                else:
                    if s == production[-1]:
                        first[symbol].add('ε')
        return first[symbol]

    def compute_follow(symbol):
        if symbol in follow:
            return follow[symbol]
        follow[symbol] = set()
        if symbol == start_symbol:
            follow[symbol].add('$')
        for non_terminal, productions in grammar.items():
            for production in productions:
                for i, s in enumerate(production):
                    if s == symbol:
                        if i == len(production) - 1:
                            if non_terminal != symbol:
                                follow[symbol].update(compute_follow(non_terminal))
                        else:
                            next_symbol = production[i + 1]
                            first_next = compute_first(next_symbol)
                            follow[symbol].update(first_next - {'ε'})
                            if 'ε' in first_next:
                                if non_terminal != symbol:
                                    follow[symbol].update(compute_follow(non_terminal))
        return follow[symbol]

    first = {}
    follow = {}
    start_symbol = list(grammar.keys())[0]
    for symbol in grammar:
        compute_first(symbol)
    for symbol in grammar:
        compute_follow(symbol)
    return first, follow

def construct_parsing_table(grammar, first, follow):
    table = {nt: {} for nt in grammar}
    for nt in grammar:
        for production in grammar[nt]:
            first_set = set()
            if production == 'ε':
                first_set = {'ε'}
            else:
                for symbol in production:
                    sym_first = first[symbol] if symbol in grammar else {symbol}
                    first_set.update(sym_first - {'ε'})
                    if 'ε' not in sym_first:
                        break
                else:
                    first_set.add('ε')

            for terminal in first_set:
                if terminal != 'ε':
                    if terminal in table[nt]:
                        return None
                    table[nt][terminal] = production
            if 'ε' in first_set:
                for terminal in follow[nt]:
                    if terminal in table[nt]:
                        return None
                    table[nt][terminal] = 'ε'
    return table

def is_ll1(table):
    return table is not None

def validate_string(grammar, table, input_string):
    stack = ['$', 'S']
    input_string += '$'
    index = 0

    while stack:
        top = stack.pop()
        current_input = input_string[index]

        if top == current_input == '$':
            return "Valid string"
        elif top == current_input:
            index += 1
        elif top.islower() or top in '()':
            return "Invalid string"
        elif top in grammar:
            if current_input in table[top]:
                production = table[top][current_input]
                for symbol in reversed(production):
                    if symbol != 'ε':
                        stack.append(symbol)
            else:
                return "Invalid string"
        else:
            return "Invalid string"
    return "Invalid string"

grammar = {
    'S': ['ABC', 'D'],
    'A': ['a', 'ε'],
    'B': ['b', 'ε'],
    'C': ['(S)', 'c'],
    'D': ['AC']
}

# grammar = {
#     'S': ['aBC', 'bC', 'cC', '(S)C'],
#     'B': ['b'],
#     'C': ['(S)', 'c']
# }

first, follow = compute_first_follow(grammar)

print("First Sets:")
for k in first:
    print(f"First({k}) = {first[k]}")
print("\nFollow Sets:")
for k in follow:
    print(f"Follow({k}) = {follow[k]}")

parsing_table = construct_parsing_table(grammar, first, follow)

if not is_ll1(parsing_table):
    print("\nGrammar is not LL(1)")
else:
    print("\nParsing Table:")
    for nt, rules in parsing_table.items():
        print(f"{nt}: {rules}")

    print("\nThe grammar is LL(1)")

    s = input("\nEnter string: ")

    print("\nString Validations:")
    result = validate_string(grammar, parsing_table, s)
    print(f"{s}: {result}")
