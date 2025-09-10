import pytest
from geocoding import lat_lng_to_words, words_to_lat_lng, WORD_LIST, LATITUDE_CELLS, LONGITUDE_CELLS

def test_lat_lng_to_words():
    # Test basic conversion
    words = lat_lng_to_words(51.5074, -0.1278)
    assert len(words) == 3
    assert all(isinstance(word, str) for word in words)
    assert all(word in WORD_LIST for word in words)
    assert all(word.isalpha() for word in words)
    assert len(set(words)) == 3

def test_all_words_are_alpha():
    for word in WORD_LIST:
        assert word.isalpha(), f"Word '{word}' is not purely alphabetic."

def test_words_to_lat_lng():
    # Test round trip
    original_lat, original_lng = 51.5074, -0.1278
    words = lat_lng_to_words(original_lat, original_lng)
    lat, lng = words_to_lat_lng(*words)

    # The reverse conversion should be within the same grid cell
    assert abs(lat - original_lat) < (180 / LATITUDE_CELLS)
    assert abs(lng - original_lng) < (360 / LONGITUDE_CELLS)

def test_invalid_words():
    with pytest.raises(ValueError):
        words_to_lat_lng("invalid", "words", "here")
    with pytest.raises(ValueError):
        words_to_lat_lng("apple", "apple", "banana")
    with pytest.raises(ValueError):
        words_to_lat_lng("apple1", "banana", "cherry")

def test_uniqueness():
    # Test that different coordinates give different words
    coords = [
        (51.5074, -0.1278),  # London
        (40.7128, -74.0060), # New York
        (35.6895, 139.6917), # Tokyo
        (-33.8688, 151.2093), # Sydney
    ]

    word_sets = set()
    for lat, lng in coords:
        words = lat_lng_to_words(lat, lng)
        word_tuple = tuple(words)
        assert word_tuple not in word_sets, f"Duplicate words for {lat}, {lng}: {words}"
        word_sets.add(word_tuple)

def test_bounds():
    # Test coordinate bounds
    with pytest.raises(ValueError):
        lat_lng_to_words(91, 0)  # Invalid latitude

    with pytest.raises(ValueError):
        lat_lng_to_words(0, 181)  # Invalid longitude
