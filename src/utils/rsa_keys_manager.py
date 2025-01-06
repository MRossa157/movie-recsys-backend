from __future__ import annotations

from typing import TYPE_CHECKING

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

if TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric.rsa import (
        RSAPrivateKey,
        RSAPublicKey,
    )

_PUBLIC_EXPONENT: int = 65537
_KEY_SIZE: int = 2048


class _RSAKeysManager:
    def __init__(self) -> None:
        self.__private_key: RSAPrivateKey | None = None
        self.__public_key: RSAPublicKey | None = None

    def generate_keys(self) -> None:
        """
        Создать пару из публичного и приватного ключей для шифрования.
        """
        self.__private_key = rsa.generate_private_key(
            public_exponent=_PUBLIC_EXPONENT,
            key_size=_KEY_SIZE,
            backend=default_backend(),
        )
        self.__public_key = self.__private_key.public_key()

    @property
    def get_private_key(self) -> RSAPrivateKey | None:
        return self.__private_key

    @property
    def get_public_key(self) -> RSAPublicKey | None:
        return self.__public_key


keys_manager = _RSAKeysManager()
