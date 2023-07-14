from mnemonic import Mnemonic

def generate_flag(prefix="flag"):
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=128)

    # Take only the first 4 words
    words = words.split(" ")[0:4]

    # Insert the header of the flag and "_" between words like "flag{word1_word2_word3_word4}"
    flag = prefix + "{" + "_".join(words) + "}"
    return flag