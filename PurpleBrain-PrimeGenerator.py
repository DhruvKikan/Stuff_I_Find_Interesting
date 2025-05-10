# First and foremost, credits
# This is the code I "borrowed" from PurpleBrain's video - https://www.youtube.com/watch?v=tBzaMfV94uA
# It has some additions in regards to the confidence level calculations based on https://www.youtube.com/@symmetricpositivedefinite's comment
# Do suggest changes or point out my mistakes if you find them

"""

Your confidence level needs to be adjusted for the fact that you're running the test on a lot of composite numbers. Ex: let's say the chance of a number being prime wasn't 1/2281ln(10), but rather 1/10^12. Even if your program says that it's 99.9999% confident, since you're expecting to run the test around 10^12 times until you find a prime number, you're almost guaranteed to hit the 0.0001% at some point in that process. Of course, this is exaggerated, but still.

If you want the confidence level to be more accurate, you can use Bayes's theorem: P(prime given test success) = P(test success given prime) * P(prime)/P(test success) = 1 * P(prime)/(P(prime) + P(composite)*P(false positive)) = (1/ln(n))/(1/ln(n) + 1 * (1 - your current output)) = 1/(1 + ln(n) * (1 - your current output)), where n is the number you're generating up to (so 10^2281). (I used P(composite) = 1 because the answer is the same). 

This gives a confidence level of 1/(1 + ln(10^2281) * (0.000000954)) = 99.5%. Which is, you know, good, but unlike 99.9999%, I wouldn't use it for a bank account.

"""

import random
import numpy as np
import argparse

def generate_random_odd(size):
    min_val = 10**(size - 1)
    max_val = 10**size - 1
    while True:
        num = random.randint(min_val, max_val)
        if num % 2 == 1:
            return num

def is_prime(value):
    """Check if a number is prime."""
    if value < 2:
        return False
    for i in range(2, int(value**0.5) + 1):
        if value % i == 0:
            return False
    return True

# list of prime numbers less then 1100
small_primes = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 
    79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 
    167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 
    257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 
    353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 
    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 
    563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 
    653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 
    761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 
    877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 
    991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069
]

def is_multiple_of_small_prime(number):
    """Check if n is a multiple of any small prime."""
    for prime in small_primes:
        if number % prime == 0:
            return True
    return False

def Miller_Rabin_Iteration_Test(number) -> bool:
    """
    Does the Miller-Rabin test.
    The whole iteration is done in this function.
    """
    # first check if number is in the list of small primes
    if is_multiple_of_small_prime(number) and number > small_primes[-1]:
        return False
    
    base = random.randint(2, number - 1)
    exponent = number - 1
    
    # this is Fermat's little theorem
    # if number is prime, then base^(number-1) mod number = 1
    if pow(base, exponent, number) != 1:
        return False
    
    # Miller-Rabin test (this can still fail though)
    # keep dividing exponent by 2 until it is odd
    # and re-check the base^(exponent) mod number
    # if it is not equal to number-1 or 1, then number is composite
    is_previous_base_1 = True
    while exponent % 2 == 0:
        exponent //= 2
        new_base = pow(base, exponent, number)
        if is_previous_base_1:
            if new_base == number - 1:
                is_previous_base_1 = False
            elif new_base != 1:
                return False
    return True

def Miller_Rabin_Test(number, iterations = 25) -> bool:
    """Perform the Miller-Rabin primality test for 'iteration' counts."""
    for _ in range(iterations):
        if not Miller_Rabin_Iteration_Test(number):
            return False
    return True

def generate_prime(size, iterations = 25):
    """Generate a prime number of the given size."""
    i = 0
    while True:
        i += 1
        print(f"Iteration {i} (expected {int(2.3 * size)} total)")
        random_odd = generate_random_odd(size)
        if Miller_Rabin_Test(random_odd, iterations):
            return random_odd

def basic_confidence(iterations):
    """Calculate the confidence level of the Miller-Rabin test."""
    return 1 - (0.25 ** iterations)

def bayesian_confidence(size, iterations):
    """Calculate the Bayesian confidence level of the Miller-Rabin test."""
    basic = basic_confidence(iterations)
    ln_n = size * np.log(10)
    # Bayesian confidence level is calculated using the formula:
    # P(prime|pass) = P(pass|prime) * P(prime) / P(pass)
    # P(prime|pass) ≈ 1 / [1 + ln(n) * (1 - basic_confidence)]
    return 1.0 / (1.0 + ln_n * (1.0 - basic))


parser = argparse.ArgumentParser()
parser.add_argument('-n', type = int, required = True, help = "Size of required number (must be greater than 0)")
args = parser.parse_args()
number_size = args.n
print(generate_prime(size = number_size, iterations = 20))
print(f"Confidence level: {basic_confidence(20) * 100:.20f}%")
print(f"Bayesian confidence level: {bayesian_confidence(number_size, 20) * 100:.20f}%")
