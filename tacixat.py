import math
import struct
import random
from z3 import *

MASK = 0xFFFFFFFFFFFFFFFF


# xor_shift_128_plus algorithm
def xs128p(state0, state1, browser):
    print("xs128p")
    s1 = state0 & MASK
    s0 = state1 & MASK
    s1 ^= (s1 << 23) & MASK
    s1 ^= (s1 >> 17) & MASK
    s1 ^= s0 & MASK
    s1 ^= (s0 >> 26) & MASK
    state0 = state1 & MASK
    state1 = s1 & MASK
    if browser == "chrome":
        generated = state0 & MASK
    else:
        generated = (state0 + state1) & MASK
    return state0, state1, generated


# Symbolic execution of xs128p
def sym_xs128p(slvr, sym_state0, sym_state1, generated, browser):
    s1 = sym_state0
    s0 = sym_state1
    s1 ^= s1 << 23
    s1 ^= LShR(s1, 17)
    s1 ^= s0
    s1 ^= LShR(s0, 26)
    sym_state0 = sym_state1
    sym_state1 = s1
    if browser == "chrome":
        calc = sym_state0
    else:
        calc = sym_state0 + sym_state1

    condition = Bool("c%d" % int(generated * random.random()))
    if browser == "chrome":
        impl = Implies(condition, LShR(calc, 12) == int(generated))
    elif browser == "firefox" or browser == "safari":
        # Firefox and Safari save an extra bit
        impl = Implies(condition, (calc & 0x1FFFFFFFFFFFFF) == int(generated))

    slvr.add(impl)
    return sym_state0, sym_state1, [condition]


def reverse17(val):
    return val ^ (val >> 17) ^ (val >> 34) ^ (val >> 51)


def reverse23(val):
    return (val ^ (val << 23) ^ (val << 46)) & MASK


def xs128p_backward(state0, state1, browser):
    prev_state1 = state0
    prev_state0 = state1 ^ (state0 >> 26)
    prev_state0 = prev_state0 ^ state0
    prev_state0 = reverse17(prev_state0)
    prev_state0 = reverse23(prev_state0)
    # this is only called from an if chrome
    # but let's be safe in case someone copies it out
    if browser == "chrome":
        generated = prev_state0
    else:
        generated = (prev_state0 + prev_state1) & MASK
    return prev_state0, prev_state1, generated


# Print 'last seen' random number
#   and winning numbers following that.
# This was for debugging. We know that Math.random()
#   is called in the browser zero times (updated) for each page click
#   in Chrome and once for each page click in Firefox.
#   Since we have to click once to enter the numbers
#   and once for Play, we indicate the winning numbers
#   with an arrow.
def power_ball(generated, browser):
    # for each random number (skip 4 of 5 that we generated)
    for idx in range(len(generated[4:])):
        # powerball range is 1 to 69
        poss = list(range(1, 70))
        # base index 4 to skip
        gen = generated[4 + idx :]
        # get 'last seen' number
        g0 = gen[0]
        gen = gen[1:]
        # make sure we have enough numbers
        if len(gen) < 6:
            break
        print(g0)

        # generate 5 winning numbers
        nums = []
        for jdx in range(5):
            index = int(gen[jdx] * len(poss))
            val = poss[index]
            poss = poss[:index] + poss[index + 1 :]
            nums.append(val)

        # print indicator
        if idx == 0 and browser == "chrome":
            print("--->", end="")
        elif idx == 2 and browser == "firefox":
            print("--->", end="")
        else:
            print("    ", end="")
        # print winning numbers
        print(sorted(nums), end="")

        # generate / print power number or w/e it's called
        double = gen[5]
        val = int(math.floor(double * 26) + 1)
        print(val)


# Firefox nextDouble():
# (rand_uint64 & ((1 << 53) - 1)) / (1 << 53)
# Chrome nextDouble():
# (state0 | 0x3FF0000000000000) - 1.0
# Safari weakRandom.get():
# (rand_uint64 & ((1 << 53) - 1) * (1.0 / (1 << 53)))
def to_double(browser, out):
    if browser == "chrome":
        double_bits = (out >> 12) | 0x3FF0000000000000
        double = struct.unpack("d", struct.pack("<Q", double_bits))[0] - 1
    elif browser == "firefox":
        double = float(out & 0x1FFFFFFFFFFFFF) / (0x1 << 53)
    elif browser == "safari":
        double = float(out & 0x1FFFFFFFFFFFFF) * (1.0 / (0x1 << 53))
    return double


def main():
    # Note:
    # Safari tests have always turned up UNSAT
    # Wait for an update from Apple?
    # browser = 'safari'
    browser = "firefox"
    # browser = 'firefox'
    print("BROWSER: %s" % browser)

    # In your browser's JavaScript console:
    # _ = []; for(var i=0; i<5; ++i) { _.push(Math.random()) } ; console.log(_)
    # Enter at least the 3 first random numbers you observed here:
    # Observations show Chrome needs ~5
    dubs = [
        0.6001352587932771,
        0.3250225488841686,
        0.2681294834228445,
        0.7019064719602867,
        0.5599697355474599,
    ]
    expected = [
        0.5837681703073178,
        0.18128470048076706,
        0.2553924400843819,
        0.2388525040412779,
        0.9099321641840764,
    ]
    if browser == "chrome":
        dubs = dubs[::-1]

    print("dubs")
    [print(x) for x in dubs]
    print("")

    # from the doubles, generate known piece of the original uint64
    generated = []
    for idx in range(len(dubs)):
        if browser == "chrome":
            recovered = struct.unpack("<Q", struct.pack("d", dubs[idx] + 1))[0] & (
                MASK >> 12
            )
        elif browser == "firefox":
            recovered = dubs[idx] * (0x1 << 53)
        elif browser == "safari":
            recovered = dubs[idx] / (1.0 / (1 << 53))
        print(f"{dubs[idx]} recovered to {recovered}")
        generated.append(recovered)

    # setup symbolic state for xorshift128+
    ostate0, ostate1 = BitVecs("ostate0 ostate1", 64)
    sym_state0 = ostate0
    sym_state1 = ostate1
    slvr = Solver()
    conditions = []

    # run symbolic xorshift128+ algorithm for three iterations
    # using the recovered numbers as constraints
    for ea in range(len(dubs)):
        sym_state0, sym_state1, ret_conditions = sym_xs128p(
            slvr, sym_state0, sym_state1, generated[ea], browser
        )
        conditions += ret_conditions

    print("conditions:")
    [print(c) for c in conditions]
    
    if slvr.check(conditions) == sat:
        # get a solved state
        m = slvr.model()
        print(f"type of ostate0 is {type(ostate0)}")
        print(f"type of ostate1 is {type(ostate1)}")
        state0 = m[ostate0].as_long()
        state1 = m[ostate1].as_long()
        print(f"state0={state0} state1={state1}")
        # slvr.add(Or(ostate0 != m[ostate0], ostate1 != m[ostate1]))
        # if slvr.check(conditions) == sat:
        #    print("WARNING: multiple solutions found! use more dubs!")

        num_of_next_predictions = 5
        predictions = []
        # generate random numbers from recovered state
        for idx in range(num_of_next_predictions + len(dubs)):
            if browser == "chrome":
                state0, state1, out = xs128p_backward(state0, state1, browser)
                out = state0 & MASK
            else:
                state0, state1, out = xs128p(state0, state1, browser)

            double = to_double(browser, out)
            if idx >= len(dubs):
                predictions.append(double)

        print("\npredictions:")
        [print(i) for i in predictions]

        # use generated numbers to predict powerball numbers
        # power_ball(generated, browser)
    else:
        print("UNSAT")


main()
