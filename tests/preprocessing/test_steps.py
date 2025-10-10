from src.preprocessing import steps as ps


def test_to_lowercase():
    assert ps.to_lowercase("HELLO World!") == "hello world!"
    assert ps.to_lowercase("123 ABC xyz") == "123 abc xyz"


def test_strip_whitespace():
    assert ps.strip_whitespace("   hello world   ") == "hello world"
    assert ps.strip_whitespace("\n\t test \t\n") == "test"


def test_remove_punctuation():
    assert ps.remove_punctuation("Hello, world!!!") == "Hello world"
    assert ps.remove_punctuation("Wait... what?!") == "Wait what"
    assert ps.remove_punctuation("No punctuation") == "No punctuation"


def test_correct_spelling_str():
    # "speling" -> "spelling" (autocorrect)
    result = ps.correct_spelling("speling")
    assert isinstance(result, str)
    assert "spell" in result


def test_correct_spelling_list():
    words = ["speling", "korrect", "writen"]
    result = ps.correct_spelling(words)
    assert isinstance(result, list)
    assert len(result) == 3
    assert all(isinstance(w, str) for w in result)


def test_expand_contractions():
    assert ps.expand_contractions("can't") == "cannot"
    assert ps.expand_contractions("he's going") == "he is going"


def test_tokenize():
    assert ps.tokenize("hello world") == ["hello", "world"]
    assert ps.tokenize("a b  c") == ["a", "b", "c"]


def test_remove_repeated_characters():
    assert ps.remove_repeated_characters("soooo coooool") == "soo cool"
    assert ps.remove_repeated_characters("noooooooo wayyyyy") == "noo wayy"
    assert ps.remove_repeated_characters("yeeeessss!!!") == "yeess!!"
    assert ps.remove_repeated_characters("ok") == "ok"


def test_remove_stopwords():
    tokens = ["this", "is", "a", "test"]
    result = ps.remove_stopwords(tokens)
    # "is" and "a" are stopwords in English
    assert "is" not in result
    assert "a" not in result
    assert "this" in result or "test" in result


def test_stem_tokens():
    tokens = ["running", "flies", "easily", "fairly"]
    result = ps.stem_tokens(tokens)
    # Check that stemming reduces words
    assert result == ["run", "fli", "easili", "fair"]


def test_lemmatize_tokens():
    tokens = ["running", "flies", "better"]
    result = ps.lemmatize_tokens(tokens)
    # "running" -> "running" (default is noun), "flies" -> "fly"
    assert "fly" in result
    assert "running" in result or "run" in result
