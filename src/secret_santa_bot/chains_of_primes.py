from __future__ import annotations

import itertools
import math
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from secret_santa_bot.santa import Santa


def generate_coprime(n: int) -> int:
    # coprime of 0 gives a step size of 1 in santa.connect_graph
    if n < 3:
        return 0
    coprime = 3
    while math.gcd(n, coprime) != 1:
        coprime += 1
    return coprime


def is_prime(n: int) -> bool:
    """Calculates if a number is prime by calculating divisibility by squares."""
    # try except handles the case where n == n // 6 * 6
    try:
        for divisor in range(2, math.floor(math.sqrt(n)) + 1):
            if not n % divisor:
                return False
        return True
    except ValueError:
        return False


def check_compliment(candidate: int, sum: int):
    compliment = sum - candidate
    if is_prime(candidate) and is_prime(compliment):
        return candidate, compliment
    return False


def even_decomposition(n: int) -> tuple[int, int]:
    """Decomposes an even number into two primes using Goldbach's conjecture,
    and that all primes p > 5 can be expressed as p = 6q ± 1."""
    if n < 6:
        raise ValueError('The number to be decomposed must be greater than 6.')
    start = n // 6 * 6
    for candidate_median in range(start, 0, -6):
        if decomposition := check_compliment(candidate_median + 1, n):
            return decomposition
        if decomposition := check_compliment(candidate_median - 1, n):
            return decomposition
    raise RuntimeWarning('Mr. Gold is going to be real mad.')


def odd_decomposition(n: int) -> tuple[int, int, int]:
    """Decomposition based on Goldbach's weak conjecture. See
    santa.even_decomposition for further detail."""
    even_number = n - 3
    decomposition, compliment = prime_decomposition(even_number)
    return decomposition, compliment, 3


def prime_decomposition(n: int) -> Iterable[int]:
    if is_prime(n):
        return (n,)
    elif n in [4, 6]:
        return n // 2, n // 2
    if n % 2 == 0:
        return even_decomposition(n)
    else:
        return odd_decomposition(n)


def adjust_index(decomposition: Iterable[int]):
    adjusted_index = []
    current_sum = 0
    for entry in decomposition:
        current_sum += entry
        adjusted_index.append(current_sum)
    return adjusted_index


def make_prime_sets(santas: Sequence[Santa]):
    """Makes sets A for which |A| is a prime number."""
    decomposition = prime_decomposition(len(santas))
    decomposition = adjust_index(decomposition)
    mappings = []
    lower_boundary = 0
    for upper_boundary in decomposition:
        prime_mapping = santas[lower_boundary:upper_boundary]
        mappings.append(prime_mapping)
        lower_boundary = upper_boundary
    return mappings


def connect_graph(santas: Sequence[Santa]):
    n = len(santas)
    k = generate_coprime(n)
    current_santa = santas[0]
    for index in range(n + 1):
        target_index = ((k + 1) * index) % n
        current_santa.target = santas[target_index].member
        current_santa = santas[target_index]


def verify_interconnectivity(mappings: Sequence[Sequence[Santa]]):
    """Checks that every number is present in and that the mapping is circular."""
    flattened_mapping = list(itertools.chain.from_iterable(mappings))
    member_sum = 0
    target_sum = 0
    for entry in flattened_mapping:
        member_sum += entry.member or 0
        target_sum += entry.target or 0
    if not member_sum == target_sum:
        print(mappings)
    sentinel = flattened_mapping[0]
    current_entry = flattened_mapping[0]
    joins = 0
    first = True
    while first or current_entry is not sentinel:
        if first:
            first = False
        target_index = current_entry.target
        current_entry = flattened_mapping[target_index]
        joins += 1
    if joins != len(flattened_mapping):
        print(mappings)


def connect_disjoint_graphs(mappings):
    for left_mapping, right_mapping in itertools.pairwise(mappings):
        left_mapping[-1].target, right_mapping[0].target = (
            right_mapping[0].target,
            left_mapping[-1].target,
        )
    return mappings


def assign_santas(santas: Sequence[Santa]):
    mappings = make_prime_sets(santas)
    for mapping in mappings:
        connect_graph(mapping)
    mappings = connect_disjoint_graphs(mappings)
    return itertools.chain.from_iterable(mappings)
    # verify_interconnectivity(mappings)
