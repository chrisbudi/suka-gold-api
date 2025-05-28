def round_up_to_100(n):
    return n if n % 100 == 0 else n + (100 - n % 100)
