from z3 import *
import random
from typing import List, Optional, Dict

"""
In your generator, you go from internal state → double output using this flow:
 - `state → uint64_t from next() → masked mantissa → normalized [0, 1) float (nextDouble)`
 
In the predictor, you're doing the reverse:
 - `observed float → recover masked mantissa → backtrack to possible `next()` result → solve for initial states`
"""


class FirefoxRandomnessPredictor:
    def __init__(self, sequence: List[float]):
        self.sequence = sequence
        self.__mask = 0xFFFFFFFFFFFFFFFF
        self.__internalSequence = sequence
        self.__solver = Solver()
        self.__se_state0: BitVecRef = None
        self.__se_state1: BitVecRef = None
        self.__concrete_state0 = None
        self.__concrete_state1 = None

    def predict_next(self) -> Optional[float]:
        """
        Predict the next random number.
        """
        next_value = self.__predict()
        if next_value is None:
            print("No valid prediction found.")
            return None
        return next_value
    
    def __predict(self):
        if self.__concrete_state0 is not None and self.__concrete_state1 is not None:
            concrete_state0, concrete_state1, out = self.__xorshift128p_concrete(self.__concrete_state0, self.__concrete_state1)
            self.__concrete_state0 = concrete_state0
            self.__concrete_state1 = concrete_state1
            return self.__to_double(out)
            
        self.__se_state0, self.__se_state1 = BitVecs("se_state0 se_state1", 64)
        self.__solver = Solver()
        
        conditions = []
        for i in range(len(self.__internalSequence)):
            #sym_state0, sym_state1, ret_conditions = sym_xs128p(slvr, sym_state0, sym_state1, generated[ea], browser)
            recovered = self.__recover_mantissa(self.__internalSequence[i])
            conds = self.__xorshift128p_symbolic(recovered)
            conditions += conds
        
        if self.__solver.check(conditions) != sat:
            print("Failed to recover state")
            return None
        
        model = self.__solver.model()
        
        states: Dict[str, z3.FuncDeclRef] = {}
        for state in model.decls():
            states[state.__str__()] = model[state]

        concrete_state0 = states["se_state0"].as_long()
        concrete_state1 = states["se_state1"].as_long()
        
        for i in range(len(self.__internalSequence)):
            # Since this is concrete impl from og state, we discard known rands
            concrete_state0, concrete_state1, out = self.__xorshift128p_concrete(concrete_state0, concrete_state1)
            self.__to_double(out)
            
        concrete_state0, concrete_state1, out = self.__xorshift128p_concrete(concrete_state0, concrete_state1)
        self.__concrete_state0 = concrete_state0
        self.__concrete_state1 = concrete_state1
        return self.__to_double(out)
            
    def __xorshift128p_concrete(self, state0, state1):
        s1 = state0 & self.__mask
        s0 = state1 & self.__mask
        s1 ^= (s1 << 23) & self.__mask
        s1 ^= (s1 >> 17) & self.__mask
        s1 ^= s0 & self.__mask
        s1 ^= (s0 >> 26) & self.__mask
        state0 = state1 & self.__mask
        state1 = s1 & self.__mask
        generated = (state0 + state1) & self.__mask
        return state0, state1, generated

    def __xorshift128p_symbolic(self, val):
        s1 = self.__se_state0 #sym_state0
        s0 = self.__se_state1 #sym_state1
        s1 ^= s1 << 23
        s1 ^= LShR(s1, 17)
        s1 ^= s0
        s1 ^= LShR(s0, 26)
        self.__se_state0 = self.__se_state1 #sym_state0 = sym_state1
        self.__se_state1 = s1 #sym_state1 = s1
        calc = self.__se_state0 + self.__se_state1 #calc = sym_state0 + sym_state1
            
        condition = Bool("c%d" % int(val * random.random()))
        self.__solver.add(Implies(condition, (calc & 0x1FFFFFFFFFFFFF) == int(val)))
        return [condition]
    
    def __to_double(self, val):
        return float(val & 0x1FFFFFFFFFFFFF) / (0x1 << 53)
    
    def __recover_mantissa(self, dbl):
        return dbl * (0x1 << 53)