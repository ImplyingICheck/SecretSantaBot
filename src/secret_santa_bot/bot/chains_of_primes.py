"""Creates a completely connected mapping of gift recipients and gift givers."""
from __future__ import annotations

import itertools
import math
from collections.abc import Iterable, Sequence
from typing import Literal, TYPE_CHECKING


if TYPE_CHECKING:
    from secret_santa_bot.bot.santa import Santa

_PRIME_CYCLE = 6


def _generate_coprime(n: int) -> int:
    """This function should only be used with chains_of_primes._connect_graph.
    It returns 0 when n < 3 to remain internally consistent.

    Args:
        n: An integer for which to generate a co-prime.

    Returns:
        An integer co-prime with *n*.
        If *n* is 3, the function returns 4 to prevent degenerate mapping in
            chains_of_primes._connect_graph.
    """
    # coprime of 0 gives a step size of 1 in chains_of_primes._connect_graph
    if n < 3:
        return 0
    coprime = 3
    while math.gcd(n, coprime) != 1:
        coprime += 1
    return coprime


def is_prime(n: int) -> bool:
    """Calculates if a number is prime by checking divisibility by squares."""
    if n <= 1:
        return False
    for divisor in range(2, math.floor(math.sqrt(n)) + 1):
        if not n % divisor:
            return False
    return True


def _check_compliment(
    candidate: int, target: int
) -> tuple[int, int] | Literal[False]:
    """Verifies that two summands are prime.

    Args:
        candidate: A number to be tested. One of the two summands is sufficient
            to uniquely identify the pair.
        target: The result to which the candidate and compliment sum to

    Returns:
        A tuple of (int, int) if the candidate and compliment are both prime.
        Otherwise, False.
    """
    compliment = target - candidate
    if is_prime(candidate) and is_prime(compliment):
        return candidate, compliment
    return False


def _even_decomposition(n: int) -> tuple[int, int]:
    """Decomposes an even number into two primes. Uses Goldbach's conjecture,
    and that all primes p > 5 can be expressed as p = 6q ± 1.

    Args:
        n: An even integer in the range [8, ∞)

    Returns:
        A tuple of two prime numbers whose sum is *n*. No guarantees are made
        other than the return value is prime and sum to *n*.
    """
    if n <= _PRIME_CYCLE:
        raise ValueError(
            (
                f'The number to be decomposed must be greater than '
                f'{_PRIME_CYCLE}.'
            )
        )
    if n % 2 == 1:
        raise ValueError('The number to be decomposed must be even.')
    start = n // 6 * 6
    for candidate_median in range(start, 0, -_PRIME_CYCLE):
        if decomposition := _check_compliment(candidate_median + 1, n):
            return decomposition
        if decomposition := _check_compliment(candidate_median - 1, n):
            return decomposition
    raise RuntimeWarning('Mr. Gold is going to be real mad.')


def _odd_decomposition(n: int) -> tuple[int, ...]:
    """Decomposition based on Goldbach's weak conjecture. See
    santa._even_decomposition for further detail.

    Implementation detail: special checks are done in
    chains_of_primes.prime_decomposition to improve coverage. This function
    should not hand off directly to chains_of_primes._even_decomposition.

    Args:
        n: An odd integer in the range [5, ∞)

    Returns:
        While the naive implementation returns 3 as the last integer in the
        tuple, this is not guaranteed and should not be relied upon.
    """
    if n % 2 == 0:
        raise ValueError('The number to be decomposed must be odd.')
    even_number = n - 3
    return *prime_decomposition(even_number), 3


def prime_decomposition(n: int) -> tuple[int, ...]:
    """Generates the prime decomposition of an integer *n*.

    Implementation detail: The set of if ... elif ... statements expand coverage
    of integers from [2, 6] as these would raise an exception in
    chains_of_primes._even_decomposition.

    Args:
        n: Any integer in the domain [2, ∞)

    Returns:
        The prime decomposition of *n*. No guarantees are made as to the content
        other than the return values sum to *n* and are all prime.
    """
    if n <= 1:
        raise ValueError(
            f'Prime decomposition can only be done for n greater '
            f'than 1. Received: {n}'
        )
    elif is_prime(n):
        return (n,)
    elif n in [4, 6]:
        return n // 2, n // 2
    return _even_decomposition(n) if n % 2 == 0 else _odd_decomposition(n)


def _adjust_index(decomposition: Iterable[int]) -> list[int]:
    adjusted_index: list[int] = []
    current_sum = 0
    for entry in decomposition:
        current_sum += entry
        adjusted_index.append(current_sum)
    return adjusted_index


def _convert_to_prime_sized_sets(
    santas: Sequence[Santa],
) -> list[Sequence[Santa]]:
    """Makes sets A for which |A| is a prime number."""
    decomposition_indices = prime_decomposition(len(santas))
    decomposition_indices = _adjust_index(decomposition_indices)
    mappings: list[Sequence[Santa]] = []
    lower_boundary = 0
    for upper_boundary in decomposition_indices:
        prime_mapping = santas[lower_boundary:upper_boundary]
        mappings.append(prime_mapping)
        lower_boundary = upper_boundary
    return mappings


def _connect_graph(santas: Sequence[Santa]) -> None:
    """Updates Santa.target to be another Santa within the Sequence.

    Uses the cyclical nature of the modulo of prime number multiples."""
    n = len(santas)
    k = _generate_coprime(n)
    current_santa = santas[0]
    for index in range(n + 1):
        target_index = ((k + 1) * index) % n
        current_santa.target = santas[target_index].member
        current_santa = santas[target_index]


def _connect_disjoint_graphs(mappings: Sequence[Sequence[Santa]]) -> None:
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
    mappings = _convert_to_prime_sized_sets(santas)
    for mapping in mappings:
        _connect_graph(mapping)
    _connect_disjoint_graphs(mappings)
    mappings = itertools.chain.from_iterable(mappings)
    return list(mappings)
