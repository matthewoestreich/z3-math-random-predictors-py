import struct
from z3 import *
from typing import List, Optional

"""


THIS IS A WORK IN PROGRESS STILL!!


"""


class ChromeRandomnessPredictor:
    def __init__(self, sequence: List[float]):
        self.sequence = sequence[::-1]
        self.__mask = 0xFFFFFFFFFFFFFFFF
        self.__concrete_state0, self.__concrete_state1 = [None, None]
        self.__se_state0, self.__se_state1 = BitVecs("se_state0 se_state1", 64)
        self.__s0_ref, self.__s1_ref = self.__se_state0, self.__se_state1
        self.__solver = Solver()

        for i in range(len(sequence)):
            recovered = self.__recover_mantissa(sequence[i])
            self.__xorshift128p_symbolic(recovered)

        checked = self.__solver.check()
        print(self.__solver.to_smt2())
        if checked != sat:
            print(f"Unable to recover internal state! {checked}")
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

    def __xorshift128p_concrete(self):
        s1 = self.__concrete_state0
        s0 = self.__concrete_state1
        self.__concrete_state0 = s0
        s1 ^= (s1 << 23) & self.__mask
        s1 ^= (s1 >> 17) & self.__mask
        s1 ^= s0
        s1 ^= (s0 >> 26) & self.__mask
        self.__concrete_state1 = s1
        return (s0 + s1) & self.__mask

    def __xorshift128p_symbolic(self, val: float) -> None:
        s1 = self.__se_state0
        s0 = self.__se_state1
        t = s1
        s1 ^= s1 << 23
        s1 ^= LShR(s1, 17)
        s1 ^= s0
        s1 ^= LShR(s0, 26)
        result = (s0 + s1) & self.__mask
        self.__se_state0 = s0
        self.__se_state1 = s1
        self.__solver.add(LShR(result, 12) == int(val))

    def __to_double(self, val: int):
        double_bits = (val >> 12) | 0x3FF0000000000000
        return struct.unpack("d", struct.pack("<Q", double_bits))[0] - 1

    def __recover_mantissa(self, double: float) -> float:
        float64 = struct.pack("d", double + 1)
        u_long_long_64 = struct.unpack("<Q", float64)[0]
        return u_long_long_64 & (self.__mask >> 12)
