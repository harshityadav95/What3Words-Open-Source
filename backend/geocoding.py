import math
from typing import Tuple, List

# Simplified word list for demonstration (in real What3Words, it's much larger)
WORD_LIST = [
    "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew",
    "kiwi", "lemon", "mango", "nectarine", "orange", "peach", "quince", "raspberry",
    "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "ximenia", "yam", "zucchini",
    "avocado", "blueberry", "coconut", "dragonfruit", "eggplant", "feijoa", "guava", "huckleberry",
    "jackfruit", "kumquat", "lime", "mulberry", "olive", "papaya", "rambutan", "soursop",
    "tamarind", "ume", "voavanga", "wolfberry", "yuzu", "ziziphus", "apricot", "blackberry",
    "cranberry", "durian", "elderflower", "fennel", "ginger", "hibiscus", "indigo", "jasmine",
    "kale", "lavender", "mint", "nutmeg", "oregano", "parsley", "quinoa", "rosemary",
    "sage", "thyme", "turmeric", "vanilla", "wasabi", "xanthan", "yarrow", "zinc",
    "almond", "basil", "cinnamon", "dill", "eucalyptus", "fennel", "garlic", "horseradish",
    "iris", "juniper", "kelp", "licorice", "marjoram", "nutmeg", "oregano", "pepper",
    "quince", "rosemary", "saffron", "tarragon", "uva", "verbena", "wormwood", "xylophone",
    "yew", "zephyr", "acacia", "birch", "cedar", "dogwood", "elm", "fir", "ginkgo"
]

GRID_SIZE = len(WORD_LIST) ** (1/3)  # Cube root for 3D grid

def lat_lng_to_words(lat: float, lng: float) -> Tuple[str, str, str]:
    """Convert latitude and longitude to three words"""
    # Normalize coordinates
    lat_norm = (lat + 90) / 180  # 0 to 1
    lng_norm = (lng + 180) / 360  # 0 to 1

    # Calculate grid indices
    lat_idx = int(lat_norm * GRID_SIZE)
    lng_idx = int(lng_norm * GRID_SIZE)
    alt_idx = int((lat_norm + lng_norm) / 2 * GRID_SIZE)  # Simple altitude-like index

    # Ensure indices are within bounds
    lat_idx = min(max(lat_idx, 0), len(WORD_LIST) - 1)
    lng_idx = min(max(lng_idx, 0), len(WORD_LIST) - 1)
    alt_idx = min(max(alt_idx, 0), len(WORD_LIST) - 1)

    return WORD_LIST[lat_idx], WORD_LIST[lng_idx], WORD_LIST[alt_idx]

def words_to_lat_lng(word1: str, word2: str, word3: str) -> Tuple[float, float]:
    """Convert three words to latitude and longitude"""
    try:
        idx1 = WORD_LIST.index(word1.lower())
        idx2 = WORD_LIST.index(word2.lower())
        idx3 = WORD_LIST.index(word3.lower())
    except ValueError:
        raise ValueError("Invalid words")

    # Reverse the normalization
    lat_norm = idx1 / GRID_SIZE
    lng_norm = idx2 / GRID_SIZE

    lat = lat_norm * 180 - 90
    lng = lng_norm * 360 - 180

    return lat, lng