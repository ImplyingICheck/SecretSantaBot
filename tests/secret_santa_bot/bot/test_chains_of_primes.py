# pylint: disable=[missing-module-docstring, missing-class-docstring, protected-access, redefined-outer-name]
import math

import pytest

from secret_santa_bot.bot import chains_of_primes


@pytest.fixture
def large_prime():
    return 15485863


@pytest.fixture
def large_composite(large_prime):
    return large_prime + 1


class TestIsPrime:

    def test_is_prime_prime(self):
        assert chains_of_primes.is_prime(3) is True

    def test_is_prime_composite(self):
        assert chains_of_primes.is_prime(4) is False

    def test_is_prime_one(self):
        assert chains_of_primes.is_prime(1) is False

    def test_is_prime_zero(self):
        assert chains_of_primes.is_prime(0) is False

    def test_is_prime_negative(self):
        assert chains_of_primes.is_prime(-1) is False

    def test_is_prime_six(self):
        assert chains_of_primes.is_prime(4) is False

    def test_is_prime_large_prime(self, large_prime):
        assert chains_of_primes.is_prime(large_prime) is True

    def test_is_prime_large_composite(self, large_composite):
        assert chains_of_primes.is_prime(large_composite) is False


class TestGenerateCoprime:
    """_generate_coprime returns 0 when n < 3 to remain internally consistent
    ."""

    def test_generate_coprime_less_than_3(self):
        assert chains_of_primes._generate_coprime(2) == 0

    def test_generate_coprime_negative(self):
        assert chains_of_primes._generate_coprime(-1) == 0

    def test_generate_coprime_3(self):
        assert chains_of_primes._generate_coprime(3) == 4

    def test_generate_coprime_prime(self):
        assert math.gcd(7, chains_of_primes._generate_coprime(7)) == 1

    def test_generate_coprime_composite(self):
        assert math.gcd(8, chains_of_primes._generate_coprime(8)) == 1

    def test_generate_coprime_large_prime(self, large_prime):
        assert (
            math.gcd(
                large_prime, chains_of_primes._generate_coprime(large_prime)
            )
            == 1
        )

    def test_generate_coprime_large_composite(self, large_composite):
        assert (
            math.gcd(
                large_composite,
                chains_of_primes._generate_coprime(large_composite),
            )
            == 1
        )
