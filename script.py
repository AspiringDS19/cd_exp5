import sys

def compute_first(grammar):
    first = {nt: set() for nt in grammar}
    
    def get_first(symbol):
        # If it's a terminal, FIRST is itself
        if symbol not in grammar:
            return {symbol}
        
        # If already computed, return it
        if first[symbol]:
            return first[symbol]
        
        for production in grammar[symbol]:
            if production == 'ε':
                first[symbol].add('ε')
            else:
                for char in production:
                    char_first = get_first(char)
                    if 'ε' in char_first:
                        first[symbol].update(char_first - {'ε'})
                        # Continue to next char if epsilon is present
                    else:
                        first[symbol].update(char_first)
                        break
                else:
                    # If all chars in production had epsilon
                    first[symbol].add('ε')
        return first[symbol]

    for nt in grammar:
        get_first(nt)
    return first

def compute_follow(grammar, first, start_symbol):
    follow = {nt: set() for nt in grammar}
    follow[start_symbol].add('$') # End of input marker
    
    changed = True
    while changed:
        changed = False
        for nt, productions in grammar.items():
            for prod in productions:
                for i in range(len(prod)):
                    char = prod[i]
                    if char in grammar: # If it's a non-terminal
                        before_count = len(follow[char])
                        
                        # Rule: If A -> αBβ, everything in FIRST(β) (except ε) is in FOLLOW(B)
                        if i + 1 < len(prod):
                            next_part = prod[i+1:]
                            # Find FIRST of the remaining string β
                            res_first = set()
                            for next_char in next_part:
                                if next_char not in grammar:
                                    res_first.add(next_char)
                                    break
                                res_first.update(first[next_char] - {'ε'})
                                if 'ε' not in first[next_char]:
                                    break
                            else:
                                res_first.add('ε')
                            
                            follow[char].update(res_first - {'ε'})
                            
                            # Rule: If ε is in FIRST(β), everything in FOLLOW(A) is in FOLLOW(B)
                            if 'ε' in res_first:
                                follow[char].update(follow[nt])
                        else:
                            # Rule: If A -> αB, everything in FOLLOW(A) is in FOLLOW(B)
                            follow[char].update(follow[nt])
                        
                        if len(follow[char]) > before_count:
                            changed = True
    return follow
