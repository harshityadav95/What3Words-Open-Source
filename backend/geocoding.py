import math
from typing import Tuple, List
import os

from typing import Set
INDIA_ONLY = os.getenv("INDIA_ONLY_WORDS", "").lower() in ("1", "true", "yes", "on")

# Cache for different modes
WORD_LIST_CACHE = {}
WORD_TO_INDEX_CACHE = {}
WORD_COMBINATIONS_CACHE = {}

# Target 3m resolution across Earth's surface (approx 3m x 3m squares)
# We'll size the grid independently of dictionary size and then ensure
# the dictionary capacity (unique permutations of 3 words) is sufficient.
EARTH_RADIUS_M = 6_371_008.8  # Authalic radius (equal-area sphere), meters

# Total number of ~3m squares based on spherical surface area A = 4*pi*R^2, each of area ~9 m^2
# what3words quotes ~57 trillion squares; this formula yields ~56.7 trillion.
TARGET_TOTAL_SQUARES = int(4 * math.pi * EARTH_RADIUS_M * EARTH_RADIUS_M // 9)

def min_words_for_total(total: int) -> int:
    """
    Compute minimum vocabulary size n such that permutations P(n,3) = n*(n-1)*(n-2) >= total.
    Uses a cubic-root initial guess and increments until the condition is met.
    """
    n = int(round(total ** (1/3)))  # initial guess
    n = max(n, 3)
    # Ensure strictly sufficient capacity
    while n * (n - 1) * (n - 2) < total:
        n += 1
    return n

REQUIRED_MIN_WORDS = min_words_for_total(TARGET_TOTAL_SQUARES)

def generate_synthetic_words(min_count: int, existing: Set[str], mode: str = "global") -> List[str]:
    """
    Deterministically generate pronounceable ASCII alphabetic tokens to extend the vocabulary
    up to at least min_count items. Only letters a-z, lowercase. No numbers, no punctuation.

    If INDIA_ONLY is enabled (env INDIA_ONLY_WORDS=1/true/yes/on), synthesize tokens using
    Indian phonotactics and common morphemes (e.g., pr/kr/sh/bh/kh... with vowels a/aa/ee/... and
    suffixes like raj, deep, jeet, preet, veer, kumar, nath, dev, pal, das, jit, kant, ish, esh, indra).
    """
    seen = set(existing)
    out: List[str] = []

    def add_word(w: str):
        if len(seen) >= min_count:
            return
        if w.isalpha() and w.encode("ascii", "ignore").decode() == w and w not in seen:
            seen.add(w)
            out.append(w)

    if INDIA_ONLY:
        # Indian-style synthesis
        vowels = ["a", "aa", "i", "ee", "u", "oo", "e", "ai", "o", "au"]
        onsets = [
            "k","kh","g","gh","ch","j","jh","t","th","d","dh","n","p","ph","b","bh","m",
            "y","r","l","v","w","s","sh","h",
            "tr","dr","pr","br","kr","gr","vr","sr","shr","sri","sk","st","sp","kl","gl","pl","bl"
        ]
        codas = [
            "n","m","r","l","sh","th","dh","nd","nt","nk","mp","rk","rt","rd","rm","rv","rs","rl",
            "an","in","it","ik","il","ir","ar","al","am","as","at","ash"
        ]
        suffixes = [
            "raj","deep","jeet","preet","veer","kumar","nath","dev","pal","das","jit","kant",
            "ish","esh","eshwar","indra","anand","inder","jeev","prasad","lal","bai","ben"
        ]

        # 1) onset + vowel + coda
        for o in onsets:
            for v in vowels:
                for c in codas:
                    add_word(o + v + c)
                    if len(seen) >= min_count:
                        return out

        # 2) onset + vowel + onset2 + vowel2
        for o1 in onsets:
            for v1 in vowels:
                for o2 in onsets:
                    for v2 in vowels:
                        add_word(o1 + v1 + o2 + v2)
                        if len(seen) >= min_count:
                            return out

        # 3) onset + vowel + suffix
        for o in onsets:
            for v in vowels:
                for sfx in suffixes:
                    add_word(o + v + sfx)
                    if len(seen) >= min_count:
                        return out

        # 4) Common standalone suffix-morpheme words
        for sfx in suffixes:
            add_word(sfx)
            if len(seen) >= min_count:
                return out

        # 5) Small fallback CV/CVC if still needed
        basic_v = ["a","e","i","o","u"]
        basic_c = list("bcdfghjklmnpqrstvwxyz")
        for c1 in basic_c:
            for v1 in basic_v:
                add_word(c1 + v1)
                if len(seen) >= min_count:
                    return out
        for c1 in basic_c:
            for v1 in basic_v:
                for c2 in basic_c:
                    add_word(c1 + v1 + c2)
                    if len(seen) >= min_count:
                        return out

        return out
    else:
        # Generic pronounceable synthesis (previous behavior)
        vowels = ["a", "e", "i", "o", "u"]
        cons = list("bcdfghjklmnpqrstvwxyz")  # 21 consonants

        # 1) CVCV
        for c1 in cons:
            for v1 in vowels:
                for c2 in cons:
                    for v2 in vowels:
                        add_word(c1 + v1 + c2 + v2)
                        if len(seen) >= min_count:
                            return out

        # 2) CVCVC
        for c1 in cons:
            for v1 in vowels:
                for c2 in cons:
                    for v2 in vowels:
                        for c3 in cons:
                            add_word(c1 + v1 + c2 + v2 + c3)
                            if len(seen) >= min_count:
                                return out

        # 2b) CVCCV
        for c1 in cons:
            for v1 in vowels:
                for c2 in cons:
                    for c3 in cons:
                        for v2 in vowels:
                            add_word(c1 + v1 + c2 + c3 + v2)
                            if len(seen) >= min_count:
                                return out

        # 3) Fallbacks
        for c1 in cons:
            for v1 in vowels:
                for c2 in cons:
                    add_word(c1 + v1 + c2)
                    if len(seen) >= min_count:
                        return out
        for c1 in cons:
            for v1 in vowels:
                add_word(c1 + v1)
                if len(seen) >= min_count:
                    return out

        return out
def load_word_list(filename: str, mode: str = "global") -> List[str]:
    """Load a word list strictly filtering to lowercase ASCII alphabetic words.

    mode="india":
      - Load exclusively from backend/wordlists/india_only/*.txt
    mode="global":
      - Load base filename and merge backend/wordlists/*.txt
    """
    if mode in WORD_LIST_CACHE:
        return WORD_LIST_CACHE[mode]

    current_dir = os.path.dirname(os.path.abspath(__file__))
    words: List[str] = []

    if mode == "india":
        india_dir = os.path.join(current_dir, "wordlists", "india_only")
        if not os.path.isdir(india_dir):
            raise FileNotFoundError(f"India mode enabled but directory not found: {india_dir}")
        for name in os.listdir(india_dir):
            if name.lower().endswith(".txt"):
                extra_path = os.path.join(india_dir, name)
                try:
                    with open(extra_path, "r") as ef:
                        words.extend([line.strip().lower() for line in ef if line.strip()])
                except Exception:
                    # Skip unreadable files silently to avoid breaking startup
                    pass
    else:
        # Base file
        file_path = os.path.join(current_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The word list file was not found at: {file_path}")
        with open(file_path, "r") as f:
            words = [line.strip().lower() for line in f if line.strip()]

        # Merge in additional curated wordlists
        extra_dir = os.path.join(current_dir, "wordlists")
        if os.path.isdir(extra_dir):
            for name in os.listdir(extra_dir):
                if name.lower().endswith(".txt"):
                    extra_path = os.path.join(extra_dir, name)
                    try:
                        with open(extra_path, "r") as ef:
                            words.extend([line.strip().lower() for line in ef if line.strip()])
                    except Exception:
                        # Skip unreadable files silently to avoid breaking startup
                        pass

    # Keep only a-z letters; drop any item containing non-letters (digits, hyphens, accents, punctuation)
    alpha_words = [
        w for w in words
        if w.isalpha() and w.encode("ascii", "ignore").decode() == w
    ]
    unique_words = sorted(set(alpha_words))

    if not unique_words or len(unique_words) < 3:
        raise ValueError("The word list is empty or insufficient after filtering (need at least 3 words).")
    if any(any(c.isdigit() for c in w) for w in unique_words):
        raise ValueError("Filtered word list still contains digits; aborting load.")

    WORD_LIST_CACHE[mode] = unique_words
    return unique_words

def get_word_data(mode: str = "global"):
    """Get word list, word_to_index, and combinations for the given mode."""
    if mode not in WORD_LIST_CACHE:
        load_word_list('words.txt', mode)

    word_list = WORD_LIST_CACHE[mode]

    # Ensure vocabulary can uniquely address ~3m squares globally
    if len(word_list) < REQUIRED_MIN_WORDS:
        extras = generate_synthetic_words(REQUIRED_MIN_WORDS, set(word_list), mode)
        word_list = sorted(set(word_list).union(extras))
        WORD_LIST_CACHE[mode] = word_list

    word_count = len(word_list)
    if word_count < 3:
        raise ValueError("Word list must contain at least 3 words after augmentation.")

    if mode not in WORD_TO_INDEX_CACHE:
        WORD_TO_INDEX_CACHE[mode] = {w: i for i, w in enumerate(word_list)}
        WORD_COMBINATIONS_CACHE[mode] = word_count * (word_count - 1) * (word_count - 2)

    return word_list, WORD_TO_INDEX_CACHE[mode], WORD_COMBINATIONS_CACHE[mode]

# For backward compatibility, load default mode
try:
    WORD_LIST = load_word_list('words.txt', "global")
    if not WORD_LIST:
        raise ValueError("The word list is empty or could not be loaded.")
except (FileNotFoundError, ValueError) as e:
    print(f"Error loading word list: {e}")
    WORD_LIST = ["apple", "banana", "cherry"]

# Ensure vocabulary can uniquely address ~3m squares globally
if len(WORD_LIST) < REQUIRED_MIN_WORDS:
    extras = generate_synthetic_words(REQUIRED_MIN_WORDS, set(WORD_LIST), "global")
    WORD_LIST = sorted(set(WORD_LIST).union(extras))

word_count = len(WORD_LIST)
if word_count < 3:
    raise ValueError("Word list must contain at least 3 words after augmentation.")

# Fast lookup for reverse conversion
WORD_TO_INDEX = {w: i for i, w in enumerate(WORD_LIST)}
WORD_COMBINATIONS = word_count * (word_count - 1) * (word_count - 2)

# Define a ~3m grid targeting what3words-like resolution using a 2:1 aspect (lon:lat)
LATITUDE_CELLS = int(math.sqrt(TARGET_TOTAL_SQUARES / 2))
LONGITUDE_CELLS = LATITUDE_CELLS * 2
TOTAL_GRID_SQUARES = LATITUDE_CELLS * LONGITUDE_CELLS

# Final safety check: permutations capacity must be >= total grid squares
if WORD_COMBINATIONS < TOTAL_GRID_SQUARES:
    raise ValueError("Insufficient vocabulary size for 3m resolution grid.")

def lat_lng_to_words(lat: float, lng: float, mode: str = "global") -> Tuple[str, str, str]:
    """Convert latitude and longitude to three unique alphabetic words."""
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= lng <= 180):
        raise ValueError("Longitude must be between -180 and 180")

    word_list, word_to_index, word_combinations = get_word_data(mode)
    word_count = len(word_list)

    lat_grid = int((lat + 90) / 180 * LATITUDE_CELLS)
    lng_grid = int((lng + 180) / 360 * LONGITUDE_CELLS)

    lat_grid = max(0, min(lat_grid, LATITUDE_CELLS - 1))
    lng_grid = max(0, min(lng_grid, LONGITUDE_CELLS - 1))

    grid_index = (lat_grid * LONGITUDE_CELLS + lng_grid)

    # Encode grid_index into a unique permutation of 3 distinct indices without building large arrays
    p_base2 = (word_count - 1) * (word_count - 2)

    a = grid_index // p_base2
    r = grid_index % p_base2
    b = r // (word_count - 2)
    c = r % (word_count - 2)

    # Map second index b from [0..n-2] to actual index skipping a
    i1 = a
    i2 = b + (1 if b >= i1 else 0)

    # Map third index c from [0..n-3] to actual index skipping {i1, i2}
    x = c
    lo = i1 if i1 < i2 else i2
    hi = i2 if i2 > i1 else i1
    if x >= lo:
        x += 1
    if x >= hi:
        x += 1
    i3 = x

    selected = (word_list[i1], word_list[i2], word_list[i3])

    # Defensive validation to guarantee alphabetic-only and uniqueness
    if not all(w.isalpha() for w in selected):
        raise ValueError("Internal error: non-alphabetic word produced.")
    if len(set(selected)) != 3:
        raise ValueError("Internal error: duplicate words produced.")

    return selected

def words_to_lat_lng(word1: str, word2: str, word3: str, mode: str = "global") -> Tuple[float, float]:
    """Convert three unique words back to latitude and longitude."""
    word1, word2, word3 = word1.lower(), word2.lower(), word3.lower()

    if not (word1.isalpha() and word2.isalpha() and word3.isalpha()):
        raise ValueError("Words must contain only alphabetic characters.")
    if len(set([word1, word2, word3])) != 3:
        raise ValueError("Words must be unique.")

    word_list, word_to_index, word_combinations = get_word_data(mode)
    word_count = len(word_list)

    try:
        w1_val = word_to_index[word1]
        w2_val = word_to_index[word2]
        w3_val = word_to_index[word3]
    except KeyError:
        raise ValueError("One or more words not found in the dictionary")

    # Decode the permutation back to the grid_index using inverse mapping
    p_base2 = (word_count - 1) * (word_count - 2)

    a = w1_val
    # Inverse of i2 mapping (skip a)
    b = w2_val - (1 if w2_val > a else 0)

    # Inverse of i3 mapping (skip {a, w2_val})
    c = w3_val
    lo = a if a < w2_val else w2_val
    hi = w2_val if w2_val > a else a
    if c > hi:
        c -= 1
    if c > lo:
        c -= 1

    grid_index = a * p_base2 + b * (word_count - 2) + c

    lat_grid = grid_index // LONGITUDE_CELLS
    lng_grid = grid_index % LONGITUDE_CELLS

    lat = (lat_grid / LATITUDE_CELLS) * 180 - 90
    lng = (lng_grid / LONGITUDE_CELLS) * 360 - 180

    # Center the coordinates in the middle of the square
    lat += (180 / LATITUDE_CELLS) / 2
    lng += (360 / LONGITUDE_CELLS) / 2

    return max(-90, min(90, lat)), max(-180, min(180, lng))

if __name__ == "__main__":
    print(f"Word list size: {len(WORD_LIST)}")
    print(f"Word combinations: {WORD_COMBINATIONS}")
    print(f"Grid dimension: {LATITUDE_CELLS}x{LONGITUDE_CELLS}")

    test_lat, test_lng = 51.5074, -0.1278
    words = lat_lng_to_words(test_lat, test_lng)
    print(f"\nLondon: {test_lat}, {test_lng} -> {words}")

    back_lat, back_lng = words_to_lat_lng(*words)
    print(f"Reverse: {words} -> {back_lat}, {back_lng}")
    print(f"Accuracy: lat={abs(test_lat - back_lat):.6f}, lng={abs(test_lng - back_lng):.6f}")
