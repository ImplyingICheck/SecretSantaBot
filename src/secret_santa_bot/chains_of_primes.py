from __future__ import annotations

import itertools
import math
from collections.abc import Iterable, Sequence
from typing import Literal, TYPE_CHECKING


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


def check_compliment(
    candidate: int, sum: int
) -> tuple[int, int] | Literal[False]:
    """Verifies that two summands are prime.

    Args:
        candidate: A number to be tested. One of the two summands is sufficient
            to uniquely identify the pair.
        sum: The result to which the candidate and compliment sum to

    Returns:
        A tuple of (int, int) if the candidate and compliment are both prime.
        Otherwise, False.
    """
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


def adjust_index(decomposition: Iterable[int]) -> list[int]:
    adjusted_index: list[int] = []
    current_sum = 0
    for entry in decomposition:
        current_sum += entry
        adjusted_index.append(current_sum)
    return adjusted_index


def convert_to_prime_sized_sets(
    santas: Sequence[Santa],
) -> list[Sequence[Santa]]:
    """Makes sets A for which |A| is a prime number."""
    decomposition = prime_decomposition(len(santas))
    decomposition = adjust_index(decomposition)
    mappings: list[Sequence[Santa]] = []
    lower_boundary = 0
    for upper_boundary in decomposition:
        prime_mapping = santas[lower_boundary:upper_boundary]
        mappings.append(prime_mapping)
        lower_boundary = upper_boundary
    return mappings


def connect_graph(santas: Sequence[Santa]) -> None:
    """Updates Santa.target to be another Santa within the Sequence.

    Uses the cyclical nature of the modulo of prime number multiples."""
    n = len(santas)
    k = generate_coprime(n)
    current_santa = santas[0]
    for index in range(n + 1):
        target_index = ((k + 1) * index) % n
        current_santa.target = santas[target_index].member
        current_santa = santas[target_index]


def connect_disjoint_graphs(mappings: Sequence[Sequence[Santa]]) -> None:
    """Sets the last Santa of a subsequence to target the first santa of the
    following subsequence. Assuming each subsequence is cyclically connected, we
    can swap the targets of any two Santas belonging to distinct subsequences to
    create a combined, cyclically-connected subsequence."""
    for left_mapping, right_mapping in itertools.pairwise(mappings):
        left_mapping[-1].target, right_mapping[0].target = (
            right_mapping[0].target,
            left_mapping[-1].target,
        )


def assign_santas(santas: Sequence[Santa]) -> list[Santa]:
    mappings = convert_to_prime_sized_sets(santas)
    for mapping in mappings:
        connect_graph(mapping)
    connect_disjoint_graphs(mappings)
    mappings = itertools.chain.from_iterable(mappings)
    return list(mappings)
