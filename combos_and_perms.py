"""
    File: 'combos.py'

    Combination and permutation theory.

    This describes the logic behind calculating combinations and permutations,
    with a choice count, from a set of items.  This also includes recursive 
    implementations of each algorithm.
"""

"""
    Combinations:

    [] => [] # Base case.

    [a] => [ # Base case.
             []
             [a] # Base case.
           ]
    
    # Every combination of [a],
    # plus every combination of [a] with 'b' added [anywhere] to it, 
    # plus [b].
    [a b] => [ 
               []
               [a]

               [a b]
               [b]
             ]

    # Every combination of [a b],
    # plus every combination of [a b] with 'c' added [anywhere] to it, 
    # plus [c].
    [a b c] => [ 
                 []
                 [a]
                 [a b]
                 [b]

                 [a c]
                 [a b c]
                 [b c]

                 [c]
               ]

    [a b c] DECISION tree for COMBINATIONS:

    Pick 'a' or '-':               [-]                             [a]
                               /         \                     /         \
    Pick 'b' or '-':      [- -]           [- b]           [a -]           [a b]
                         /     \         /     \         /     \         /     \
    Pick 'c' or '-': [- - -] [- - c] [- b -] [- b c] [a - -] [a - c] [a b -] [a b c]

    Either a value from the set of values or nothing is selected at each level of the tree,
    i.e. at the beginning of each recursive call.  Each recursive call steps one level deeper
    along the tree branch (towards the leaf).
    Values are accumulated as each branch of the tree is traversed.
    The set of values accumulated when the leaf is reached is the combination represented by that branch.

    COMBINATIONS are produced by recursively iterating over all REMAINING elements that FOLLOW the 
    element [currently] being visited by the outer loop (if any; the base cases have no outer loop).

    PERMUTATIONS differ from combinations in that, for permutations, each inner loop visits 
    ALL elements EXCEPT those currently being visited by all outer loops.

    Note that both combination and permutation inner loops visit one less element than their outer loops
    will visit, so both will visit (n*k)/2 elements (due to the triangular iteration shape).

    The following unwound COMBINATION algorithm visits all REMAINING values with each recursion.
    Choice is implemented by limiting the number of levels of recursion to the number of choices.
    For example: [a b c] choose 2:
    - values = [a b c]
    - choice = 2
    - result = []
    - combo = []
    for a in [a b c]: # Primary function call (choice = 2).
        combo = [a]
        for b in [b c]: # First recursive function call (choice = 1).
            combo = [a b]
            for c in [c]: # Second recursive function call (choice = 0).
                0 == choice:
                    result = [ [a b] ] # Recursion would cause choice = 0.
            combo = [a]
        (loop)
        for c in [b c]: # First recursive function call (choice = 1).
            combo = [a c]
            for [] in []: # Second recursive function call (choice = 0).
                0 == choice:
                    result = [ [a b] [a c] ] # Recursion would cause choice = 0.
            combo = [a]
        (loop done)
        combo = []
    (loop)
    for b in [a b c]: # Primary function call (choice = 2).
        combo = [b]
        for c in [c]: # First recursive function call (choice = 1).
            combo = [b c]
            for [] in []: # Second recursive function call (choice = 0).
                0 == choice:
                    result = [ [a b] [a c] [b c] ] # Recursion would cause choice = 0.
            combo = [b]
        (loop done)
        combo = []
    (loop done)
    for c in [a b c]: # Prmary function call (choice = 2).
        remaining array size (from 'c') is less than choice.
        break
    return result

    Complexity:

    Time = O((n*k)/2) => O(n*k)
           n = number of values
           k = choice count ('k' in nCk).

    Space = O(k)
            k = choice count ('k' in nCk).
            There will be 'k' recursive calls.
            There will be k values per terminated recursion (base case reached).
"""
def chooseCombos(values, choice, result = None, combo = None, firstVal = None):
    if None == result: result = []
    if None == combo: combo = []
    if None == firstVal: firstVal = 0
    if 0 == choice:
        result.append(combo[:])
    else:
        for valIdx in range(firstVal, len(values)):
            if len(values) - valIdx < choice:
                break
            combo.append(values[valIdx])
            chooseCombos(values, choice - 1, result, combo, valIdx + 1)
            combo.pop()
    return result

"""
    Permutations:

    [] => [] # Base case.

    [a] => [a] # Base case.

    # Every permutation of [a] with 'b' added to it in every position.
    # NOTE: permutations of only [a] are NOT included, unlike in combinations.
    [a b] => [
               [a b]
               [b a]
             ]

    # Every permutation of [a b] with 'c' added to it in every position.
    # NOTE: permutations of only [a b] are NOT included, unlike in combinations.
    [a b c] => [
                 [c a b]
                 [a c b]
                 [a b c]

                 [c b a]
                 [b c a]
                 [b a c]
               ]

    # Every permutation of [a b c] with 'd' added to it in every position.
    # NOTE: permutations of only [a b c] are NOT included, unlike in combinations.
    [a b c d] => [
                   [d c a b]
                   [c d a b]
                   [c a d b]
                   [c a b d]
                   [d a c b]
                   [a d c b]
                   [a c d b]
                   [a c b d]
                   [d a b c]
                   [a d b c]
                   [a b d c]
                   [a b c d]

                   [d c b a]
                   [c d b a]
                   [c b d a]
                   [c b a d]
                   [d b c a]
                   [b d c a]
                   [b c d a]
                   [b c a d]
                   [d b a c]
                   [b d a c]
                   [b a d c]
                   [b a c d]
                 ]

    [a b c] DECISION tree for PERMUTATIONS:

           *
      /    |    \
     a     b     c    First, choose a or b or c
    / \   / \   / \
    b  c  a  c  a  b  Second, choose one of the remainders.
    |  |  |  |  |  |
    c  b  c  a  b  a  Third, choose the only remainder.

    Each value in the set of REMAINING values is selected at each level of the tree,
    i.e. at the beginning of each recursive call.  Each recursive call steps one level deeper
    along the tree branch (towards the leaf).
    Values are accumulated as each branch of the tree is traversed.
    The set of values accumulated when the leaf is reached is the permutation represented by that branch.

    PERMUTATIONS are produced by recursively iterating over all REMAINING elements that EXCLUDE the 
    element [currently] being visited by the outer loop (if any; the base cases have no outer loop),
    i.e. by recursively iterating over all REMAINING elements that EXCLUDE all elements being visisted
    by all outer loops.

    PERMUTATIONS are produced by recursively iterating over all REMAINING elements, which exludes elements
    being visited by the outer loop (if any; the base cases have no outer loop).  Remaining elements include
    all elements EXCEPT those being visited by ALL outer loops.  There is one outer loop for each tree level.

    COMBINATONS differ from permutatons in that, for combinations, each inner loop iterates over 
    all REMAINING elements, i.e. those that follow the element being visited by the outer loop.

    Note that both combination and permutation inner loops visit one less element than their outer loops
    will visit, so both will visit (n*k)/2 elements (due to the triangular iteration shape).

    The following unwound PERMUTATION algorithm visits all REMAINING values with each recursion.
    Choice is implemented by limiting the number of levels of recursion to the number of choices.
    For example: [a b c] permute 2:
    - values = [a b c]
    - choice = 2
    - result = []
    - perm = []
    for a in [a b c]: # Primary function call (choice = 2).
        perm = [a]
        for b in [b c]: # First recursive function call (choice = 1).
            perm = [a b]
            for c in [c]: # Second recursive function call (choice = 0).
                0 == choice:
                    result = [ [a b] ] # Recursion would cause choice = 0.
            perm = [a]
        (loop)
        for c in [b c]: # First recursive function call (choice = 1).
            perm = [a c]
            for [b] in [b]: # Second recursive function call (choice = 0).
                0 == choice:
                    result = [ [a b] [a c] ] # Recursion would cause choice = 0.
            perm = [a]
        (loop done)
        perm = []
    (loop)
    for b in [a b c]: # Primary function call (choice = 2).
        perm = [b]
        for a in [a c]: # First recursive function call (choice = 1).
            perm = [b a]
            for c in [c]: # Second recursive function call (choice = 0).
                0 == choice:
                    result = [ [a b] [a c] [b a] ] # Recursion would cause choice = 0.
            perm = [b]
        (loop)
        for c in [a c]: # First recursive function call (choice = 1).
            perm = [b c]
            for [a] in [a]: # Second recursive function call (choice = 0).
                0 == choice:
                    result = [ [a b] [a c] [b a] [b c] ] # Recursion would cause choice = 0.
            perm = [b]
        (loop done)
        perm = []
    (loop)
    for c in [a b c]: # Primary function call (choice = 2).
        perm = [c]
        for a in [a b]: # First recursive function call (choice = 1).
            perm = [c a]
            for b in [b]: # Second recursive function call (choice = 0).
                0 == choice:
                    result = [ [a b] [a c] [b a] [b c] [c a] ] # Recursion would cause choice = 0.
            perm = [b]
        (loop)
        for b in [a b]: # First recursive function call (choice = 1).
            perm = [c b]
            for [a] in [a]: # Second recursive function call (choice = 0).
                0 == choice:
                    result = [ [a b] [a c] [b a] [b c] [c a] [c b] ] # Recursion would cause choice = 0.
            perm = [b]
        (loop done)
        perm = []
    (loop done)
    return result

    Complexity:

    Time = O((n*k)/2) => O(n*k)
           n = number of values
           k = choice count ('k' in nPk).

    Space = O(k)
            k = choice count ('k' in nPk).
            There will be 'k' recursive calls.
            There will be k values per terminated recursion (base case reached).
"""
def permute(values, choice, perm = None, result = None, valuesSize = None):
    if None == perm: perm = []
    if None == result: result = []
    if None == valuesSize: valuesSize = len(values)
    if 0 == valuesSize or len(values) - valuesSize == choice:
        result.append(perm[:])
    else:
        for idx in range(valuesSize):
            if len(values) - valuesSize > choice:
                result.append(perm[:])
                break
            perm.append(values[idx])
            values[idx], values[valuesSize - 1] = values[valuesSize - 1], values[idx] # Remove value from values.
            permute(values, choice, perm, result, valuesSize - 1)
            values[idx], values[valuesSize - 1] = values[valuesSize - 1], values[idx] # Restore value in values.
            perm.pop()
    return result


if __name__ == '__main__':
    values = ['a', 'b', 'c'] 
    
    for choice in range(len(values) + 1):
        print("{} choose {}:".format(values, choice))
        print("[")
        for combo in chooseCombos(values, choice):
            print("  {}".format(combo))
        print("]")

    print("")

    for choice in range(len(values) + 1):
        print("{} perm {}:".format(values, choice))
        print("[")
        for perm in permute(values, choice):
            print("  {}".format(perm))
        print("]")

#
# End of 'combos.py'
#

