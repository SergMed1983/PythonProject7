from text_utils import reverse_text


def test_reverse_text_basic():
    assert reverse_text("hello") == "olleh"


def test_reverse_text_empty():
    assert reverse_text("") == ""


def test_reverse_text_single_char():
    assert reverse_text("a") == "a"


def test_reverse_text_with_spaces():
    assert reverse_text("a b c") == "c b a"


def test_reverse_text_unicode():
    assert reverse_text("Привет") == "тевирП"


def test_reverse_text_unicode_2():
    assert reverse_text("АБВГД") == "ДГВБА"


def test_reverse_text_mixed():
    assert reverse_text("Привет123") == "321тевирП"
