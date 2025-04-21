from z3 import *
from typing import List, Optional


class FirefoxRandomnessPredictor:
    def __init__(self, sequence: List[float]):
        self.sequence = sequence
        self.__mask = 0xFFFFFFFFFFFFFFFF
        self.__concrete_state0, self.__concrete_state1 = [None, None]
        self.__se_state0, self.__se_state1 = BitVecs("se_state0 se_state1", 64)
        self.__s0_ref, self.__s1_ref = self.__se_state0, self.__se_state1
        self.__solver = Solver()

        for i in range(len(sequence)):
            mantissa = self.__recover_mantissa(sequence[i])
            self.__xorshift128p_symbolic()
            self.__solver.add(
                ((self.__se_state0 + self.__se_state1) & 0x1FFFFFFFFFFFFF)
                == int(mantissa)
            )

        if self.__solver.check() != sat:
            return None

        model = self.__solver.model()
        self.__concrete_state0 = model[self.__s0_ref].as_long()
        self.__concrete_state1 = model[self.__s1_ref].as_long()

        # We have to get our concrete state up to the same point as our symbolic state,
        # therefore, we discard as many "predict_next()" calls as we have len(sequence).
        # Otherwise, we would return random numbers to the caller that they already have.
        # Now, when we return from predict_next() we get the actual next
        for i in range(len(sequence)):
            self.__xorshift128p_concrete()

    def predict_next(self) -> Optional[float]:
        """
        Predict the next random number.
        """
        if self.__concrete_state0 is None or self.__concrete_state1 is None:
            return None
        out = self.__xorshift128p_concrete()
        return self.__to_double(out)

    def __xorshift128p_concrete(self) -> int:
        s1 = self.__concrete_state0 & self.__mask  # state0 & self.__mask
        s0 = self.__concrete_state1 & self.__mask  # state1 & self.__mask
        s1 ^= (s1 << 23) & self.__mask
        s1 ^= (s1 >> 17) & self.__mask
        s1 ^= s0 & self.__mask
        s1 ^= (s0 >> 26) & self.__mask
        self.__concrete_state0 = s0 & self.__mask
        self.__concrete_state1 = s1 & self.__mask
        return (self.__concrete_state0 + self.__concrete_state1) & self.__mask

    def __xorshift128p_symbolic(self) -> None:
        s1 = self.__se_state0  # sym_state0
        s0 = self.__se_state1  # sym_state1
        s1 ^= s1 << 23
        s1 ^= LShR(s1, 17)
        s1 ^= s0
        s1 ^= LShR(s0, 26)
        self.__se_state0 = self.__se_state1  # sym_state0 = sym_state1
        self.__se_state1 = s1  # sym_state1 = s1

    def __to_double(self, val: int):
        return float(val & 0x1FFFFFFFFFFFFF) / (0x1 << 53)

    def __recover_mantissa(self, double: float) -> float:
        return double * (0x1 << 53)
