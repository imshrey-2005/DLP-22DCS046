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
print("First(S) =", first['S'])
print("First(A) =", first['A'])
print("First(B) =", first['B'])
print("First(C) =", first['C'])
print("First(D) =", first['D'])
print("Follow(S) =", follow['S'])
print("Follow(A) =", follow['A'])
print("Follow(B) =", follow['B'])
print("Follow(C) =", follow['C'])
print("Follow(D) =", follow['D'])