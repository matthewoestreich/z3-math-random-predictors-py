import z3
import struct
from typing import List, Optional


class V8RandomnessPredictor:
    def __init__(self, sequence: List[float]):
        self.sequence = sequence
        self.__c_state0, self.__c_state1 = None, None
        self.__internalSequence = sequence[::-1]
        self.__mask = 0xFFFFFFFFFFFFFFFF
        self.__solver = z3.Solver()
        self.__se_state0, self.__se_state1 = z3.BitVecs("se_state0 se_state1", 64)
        self.__s0_ref, self.__s1_ref = self.__se_state0, self.__se_state1

        for i in range(len(self.__internalSequence)):
            self.__xorshift128p_symbolic()
            mantissa = self.__recover_mantissa(self.__internalSequence[i] + 1)
            self.__solver.add(mantissa == z3.LShR(self.__se_state0, 12))

        if self.__solver.check() != z3.sat:
            return None

        model = self.__solver.model()
        self.__c_state0 = model[self.__s0_ref].as_long()
        self.__c_state1 = model[self.__s1_ref].as_long()

    def predict_next(self) -> Optional[float]:
        if self.__c_state0 is None or self.__c_state1 is None:
            return None
        out = self.__xorshift128p_concrete_backwards()
        return self.__to_double(out)

    def __to_double(self, val: int) -> float:
        u_long_long_64 = (val >> 12) | 0x3FF0000000000000
        float_64 = struct.pack("<Q", u_long_long_64)
        return (struct.unpack("d", float_64)[0]) - 1

    def __xorshift128p_symbolic(self) -> None:
        se_s1 = self.__se_state0
        se_s0 = self.__se_state1
        self.__se_state0 = se_s0
        se_s1 ^= se_s1 << 23
        se_s1 ^= z3.LShR(se_s1, 17)  # Logical shift instead of Arthmetric shift
        se_s1 ^= se_s0
        se_s1 ^= z3.LShR(se_s0, 26)
        self.__se_state1 = se_s1

    # Performs the typical XorShift128p but in reverse.
    def __xorshift128p_concrete_backwards(self):
        """
        - V8 gives us random numbers by popping them off of their cache.
        - This is why we have to reverse `sequence` to `__internal_sequence = sequence[::-1]` in the constructor.
        - Essentially, they give us random numbers in LIFO order, so we need to process them in reverse (like a simulated FIFO).
        
        - In order to move forward down the chain, we have to perform our concrete XOR backwards. If we performed
        our XOR forwards, we would technically be moving backwards in time, and therefore return numbers to the caller
        that they already have.
        """
        # Must set resullt here, otherwise we skip numbers by 1 step
        result = self.__c_state0
        ps1 = self.__c_state0
        ps0 = self.__c_state1 ^ (self.__c_state0 >> 26)
        ps0 = ps0 ^ self.__c_state0
        # Performs the normal shift 17 but in reverse.
        ps0 = ps0 ^ (ps0 >> 17) ^ (ps0 >> 34) ^ (ps0 >> 51)
        # Performs the normal shift 23 bbut in reverse.
        ps0 = (ps0 ^ (ps0 << 23) ^ (ps0 << 46)) & self.__mask  # self.__reverse23(ps0)
        self.__c_state0, self.__c_state1 = ps0, ps1
        return result

    def __recover_mantissa(self, double: float) -> float:
        float_64 = struct.pack("d", double)
        u_long_long_64 = struct.unpack("<Q", float_64)[0]
        return u_long_long_64 & ((1 << 52) - 1)
