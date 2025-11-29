def curry(func, arity):
    if not callable(func):
        raise TypeError("First argument must be callable")
    if not isinstance(arity, int):
        raise TypeError("Arity should be whole number")
    if arity < 0:
        raise ValueError("Arity should be non-negative")
    if arity == 0:
        try:
            return func()
        except TypeError:
            raise ValueError("Function requires more than 0 arguments")
    try:
        test_args = [0] * arity
        func(*test_args)
    except TypeError as e:
        error_msg = str(e).lower()
        if "missing" in error_msg or "required" in error_msg:
            raise ValueError(f"Arity {arity} is less than function requires")
        elif "takes" in error_msg and "but" in error_msg:
            raise ValueError(f"Arity {arity} is greater than function requires")

    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        else:

            def next_curried(*next_args):
                return curried(*(args + next_args))

            return next_curried

    return curried


def uncurry(curried_func, arity):
    if not callable(curried_func):
        raise TypeError("First argument must be callable")
    if not isinstance(arity, int):
        raise TypeError("Arity should be whole number")
    if arity < 0:
        raise ValueError("Arity should be non-negative")
    try:
        result = curried_func
        for i in range(arity):
            if not callable(result):
                raise ValueError(f"Arity {arity} is greater than function requires")
            result = result(i)
        if callable(result):
            raise ValueError(f"Arity {arity} is less than function requires")
    except Exception as e:
        raise e

    def uncurried(*args):
        if len(args) >= arity:
            result = curried_func
            for i in range(arity):
                result = result(args[i])
            return result
        elif len(args) < arity:

            def next_uncurried(*next_args):
                return uncurried(*(args + next_args))

            return next_uncurried
        else:
            raise TypeError(f"Too many arguments, expected {arity}")

    return uncurried


def sum3(x, y, z):
    return x + y + z


def greet(greeting, name):
    return f"{greeting}, {name}!"


def no_args():
    return "no args"


def main():
    sum3_curry = curry(sum3, 3)
    sum3_uncurry = uncurry(sum3_curry, 3)
    print("sum3_curry(1)(2)(3):", sum3_curry(1)(2)(3))
    print("sum3_uncurry(1, 2, 3):", sum3_uncurry(1, 2, 3))

    greet_curry = curry(greet, 2)
    print("greet_curry('Hello')('world'):", greet_curry("Hello")("world"))

    no_args_curry = curry(no_args, 0)
    print("no_args_curry:", no_args_curry)

    print("sum3_uncurry(1, 2, 3, 4):", sum3_uncurry(1, 2, 3, 4))

    try:
        curry("not a function", 2)
    except TypeError as e:
        print("Not a function error:", e)

    try:
        curry(sum3, -1)
    except ValueError as e:
        print("Negative arity error:", e)

    try:
        curry(sum3, 2)
    except ValueError as e:
        print("Wrong arity error:", e)


if __name__ == "__main__":
    main()

