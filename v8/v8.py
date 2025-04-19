import z3
import struct
from typing import List, Dict, Tuple


class V8RandomnessPredictor:
    def __init__(self, sequence: List[float]):
        self.sequence = sequence
        self.__solver = z3.Solver()
        self.__se_state0: z3.BitVecRef = None
        self.__se_state1: z3.BitVecRef = None
        self.__internalSequence = sequence[::-1]

    def predict_next(self) -> Tuple[None, float]:
        """
        Predict next random number.
        """
        next = self.__predict()
        if next is None:
            return None
        self.__internalSequence.insert(0, next)
        # Only keep 4 elements for efficient processing
        self.__internalSequence = self.__internalSequence[:4]
        return next

    def __predict(self) -> Tuple[None, float]:
        self.__solver = z3.Solver()
        self.__se_state0, self.__se_state1 = z3.BitVecs("se_state0 se_state1", 64)

        for i in range(len(self.__internalSequence)):
            self.__xorshift128p()
            u_long_long_64 = self.__double_to_u_long_long_64(self.__internalSequence[i] + 1)
            mantissa = u_long_long_64 & ((1 << 52) - 1)
            self.__solver.add(mantissa == z3.LShR(self.__se_state0, 12))

        checked = self.__check()
        if checked == False:
            return None
        return self.__to_double(checked)

    def __check(self) -> Tuple[bool, int]:
        """
        Check for a solution
        """
        if self.__solver.check() != z3.sat:
            return False

        model = self.__solver.model()

        states: Dict[str, z3.FuncDeclRef] = {}
        for state in model.decls():
            states[state.__str__()] = model[state]

        return states["se_state0"].as_long()

    def __double_to_u_long_long_64(self, val) -> int:
        """
        Technically returns an int but we treat it as `u_long_long_64`

        Pack as `double` and re-interpret as unsigned `long long` (little endian)
        > https://stackoverflow.com/a/65377273

        IEEE 754 double-precision binary floating-point format
        > https://en.wikipedia.org/wiki/Double-precision_floating-point_format
        > https://www.youtube.com/watch?v=p8u_k2LIZyo&t=257s

        Sign (1)    Exponent (11)    Mantissa (52)
        [#]         [###########]    [####################################################]
        """
        float_64 = struct.pack("d", val)
        return struct.unpack("<Q", float_64)[0]

    def __to_double(self, val: int) -> float:
        """
        Extract mantissa
        - Add `1.0` (+ 0x3FF0000000000000) to 52 bits
        - Get the double and Subtract `1` to obtain the random number between [0, 1)

        > https://github.com/v8/v8/blob/a9f802859bc31e57037b7c293ce8008542ca03d8/src/base/utils/random-number-generator.h#L111

        static inline double ToDouble(uint64_t state0) {
            // Exponent for double values for [1.0 .. 2.0)
            static const uint64_t kExponentBits = uint64_t{0x3FF0000000000000};
            uint64_t random = (state0 >> 12) | kExponentBits;
            return base::bit_cast<double>(random) - 1;
        }
        """
        u_long_long_64 = (val >> 12) | 0x3FF0000000000000
        float_64 = struct.pack("<Q", u_long_long_64)
        next_sequence: float = struct.unpack("d", float_64)[0]
        next_sequence -= 1
        return next_sequence

    def __xorshift128p(self):
        """
        XorShift128+
        > https://vigna.di.unimi.it/ftp/papers/xorshiftplus.pdf
        > https://github.com/v8/v8/blob/a9f802859bc31e57037b7c293ce8008542ca03d8/src/base/utils/random-number-generator.h#L119

        class V8_BASE_EXPORT RandomNumberGenerator final {
            ...
            static inline void XorShift128(uint64_t* state0, uint64_t* state1) {
                uint64_t s1 = *state0;
                uint64_t s0 = *state1;
                *state0 = s0;
                s1 ^= s1 << 23;
                s1 ^= s1 >> 17;
                s1 ^= s0;
                s1 ^= s0 >> 26;
                *state1 = s1;
            }
            ...
        }
        """
        se_s1 = self.__se_state0
        se_s0 = self.__se_state1
        self.__se_state0 = se_s0
        se_s1 ^= se_s1 << 23
        se_s1 ^= z3.LShR(se_s1, 17)  # Logical shift instead of Arthmetric shift
        se_s1 ^= se_s0
        se_s1 ^= z3.LShR(se_s0, 26)
        self.__se_state1 = se_s1
