import pytest
from geocoding import lat_lng_to_words, words_to_lat_lng

def test_lat_lng_to_words():
    # Test basic conversion
    words = lat_lng_to_words(51.5074, -0.1278)
    assert len(words) == 3
    assert all(isinstance(word, str) for word in words)
    assert all(word in geocoding.WORD_LIST for word in words)

def test_words_to_lat_lng():
    # Test round trip
    original_lat, original_lng = 51.5074, -0.1278
    words = lat_lng_to_words(original_lat, original_lng)
    lat, lng = words_to_lat_lng(*words)
    
    # Should be approximately equal (within grid precision)
    assert abs(lat - original_lat) < 10  # Rough approximation
    assert abs(lng - original_lng) < 10

def test_invalid_words():
    with pytest.raises(ValueError):
        words_to_lat_lng("invalid", "words", "here")