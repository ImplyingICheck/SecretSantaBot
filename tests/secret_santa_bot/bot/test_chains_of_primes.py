# pylint: disable=[missing-module-docstring, missing-class-docstring, protected-access]
from secret_santa_bot.bot import chains_of_primes


class TestIsPrime:

    def test_is_prime_prime(self):
        assert chains_of_primes._is_prime(3) is True

    def test_is_prime_composite(self):
        assert chains_of_primes._is_prime(4) is False

    def test_is_prime_one(self):
        assert chains_of_primes._is_prime(1) is False

    def test_is_prime_zero(self):
        assert chains_of_primes._is_prime(0) is False

    def test_is_prime_negative(self):
        assert chains_of_primes._is_prime(-1) is False

    def test_is_prime_six(self):
        assert chains_of_primes._is_prime(4) is False

    def test_is_prime_large_prime(self):
        assert chains_of_primes._is_prime(15485863) is True

    def test_is_prime_large_composite(self):
        assert chains_of_primes._is_prime(15485863 + 1) is False
