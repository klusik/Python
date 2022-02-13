# Create a function with two arguments that will return a list of length (n) with multiples of (x).
# Assume both the given number and the number of times to count will be positive numbers greater than 0.
# Return the results as an array (or list in Python, Haskell or Elixir).

def count_by(x, n):
    """
    Return a sequence of numbers counting by `x` `n` times.
    """
    # nejdrive vygeneruji spravne seznam, tedy bez 0 a n+1
    seznam = range(n + 1)
    seznam = seznam[1:]
    # pak ho vynasobim
    nasobek = [(i*x) for i in seznam]
    return nasobek


count_by(2, 5)
