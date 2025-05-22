# clojure.walk implementation in Python
# https://gist.github.com/SegFaultAX/10941721
# https://clojuredocs.org/clojure.walk

# Note: this can probably be made lazy
# Are list comprehensions lazy in python?


from functools import partial

def identity(e):
    return e

def walk(inner, outer, coll):
    if isinstance(coll, list):
        return outer([inner(e) for e in coll])
    elif isinstance(coll, dict):
        return outer(dict([inner(e) for e in coll.items()]))
    elif isinstance(coll, tuple):
        return outer([inner(e) for e in coll])
    else:
        return outer(coll)

def prewalk(fn, coll):
    return walk(partial(prewalk, fn), identity, fn(coll))

def postwalk(fn, coll):
    return walk(partial(postwalk, fn), fn, coll)

def prewalk_demo(coll):
    def prn(e):
        print("Walked:", e)
        return e
    return prewalk(prn, coll)

def postwalk_demo(coll):
    def prn(e):
        print("Walked:", e)
        return e
    return postwalk(prn, coll)


def postwalk_traverse(coll):
    """Traverse the tree and return a post-order list of all the nodes."""
    # Note: I would've liked to have done this without mutable state,
    # but this is way simpler, and any mutable state is kept local to this fn.
    out = []
    def _helper(e): out.append(e); return e
    postwalk(_helper, coll)
    return out


## Test this file
if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    b = {'a': 1, 'b': 2, 'c': 3}
    c = {'a': 1, 'b': 2, 'c': {'d': 3, 'e': 4, 'f': {'g': 5, 'h': 6}}}

    postwalk_demo(c)
    traversal = postwalk_traverse(c)
    print(traversal)
