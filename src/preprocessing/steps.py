import re

import contractions
from autocorrect import Speller
from beartype import beartype
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer


@beartype
def to_lowercase(text: str) -> str:
    """
    Convert all characters in the string to lowercase.

    Parameters
    ----------
    text : str
        Input string to be lowercased.

    Returns
    -------
    str
        The lowercased string.
    """
    return text.lower()


@beartype
def strip_whitespace(text: str) -> str:
    """
    Remove leading and trailing whitespace from the string.

    Parameters
    ----------
    text : str
        Input string.

    Returns
    -------
    str
        The trimmed string.
    """
    return text.strip()


@beartype
def remove_punctuation(text: str) -> str:
    """
    Remove all punctuation characters from the string.

    Parameters
    ----------
    text : str
        Input string.

    Returns
    -------
    str
        The string with punctuation removed.

    Notes
    -----
    The regex pattern used is:

    ``r"[^\\w\\s]"``

    - ``\\w`` matches word characters (letters, digits, and underscore).
    - ``\\s`` matches any whitespace character.
    - ``[^...]`` is a negated character class, meaning "anything *not* in this set".

    So the pattern matches any character that is **not**:
    - a letter
    - a digit
    - an underscore
    - whitespace

    All matched characters are replaced with an empty string.

    Examples
    --------
    >>> remove_punctuation("Hello, world!!!")
    'Hello world'
    >>> remove_punctuation("Wait... what?!")
    'Wait what'
    """

    return re.sub(r"[^\w\s]", "", text)


@beartype
def correct_spelling(
    text: str | list[str], speller: Speller = Speller(lang="en")
) -> str | list[str]:
    """
    Correct spelling in the text using an autocorrect speller.

    Parameters
    ----------
    text : str or list of str
        Input string to correct.
    speller : Speller, optional
        Autocorrect speller instance to use, by default a new English `Speller`.

    Returns
    -------
    str or list of str
        The corrected string.
    """
    if isinstance(text, list):
        return [speller(t) for t in text]

    return speller(text)


@beartype
def expand_contractions(text: str) -> str:
    """
    Expand contractions in the input string.

    Examples
    --------
    "can't" -> "cannot"

    Parameters
    ----------
    text : str
        Input string.

    Returns
    -------
    str
        The expanded string.

    Raises
    ------
    ValueError
        If the contractions library returns a non-string result.
    """
    result = contractions.fix(text)
    if not isinstance(result, str):
        raise ValueError("Contractions.fix did not return a string")
    return result


@beartype
def tokenize(text: str) -> list[str]:
    """
    Split the input string into tokens by whitespace.

    Parameters
    ----------
    text : str
        Input string.

    Returns
    -------
    list of str
        List of tokens.
    """
    return text.split()


@beartype
def remove_repeated_characters(text: str) -> str:
    """
    Reduce any character repeated 3 or more times down to 2 occurrences.

    Examples
    --------
    "coooool" -> "coool"

    Parameters
    ----------
    text : str
        Input string.

    Returns
    -------
    str
        The normalized string.

    Notes
    -----
    This function uses the following regular expression:

        ``r"(.)\\1{2,}"``

    Here's what each part does:

    - ``(.)``
      Captures any single character as Group 1.

    - ``\\1``
      A backreference to the character captured by Group 1, ensuring the same
      character is matched again.

    - ``{2,}``
      Specifies that the backreference must appear at least two more times.
      In total, this matches runs of **three or more** of the same character.

    The replacement string ``r"\\1\\1"`` ensures that any run of three or more
    repeated characters is reduced to exactly two.

    Examples
    --------
    >>> remove_repeated_characters("soooo coooool")
    'soo coool'
    >>> remove_repeated_characters("noooooooo wayyyyy")
    'noo wayy'`
    >>> remove_repeated_characters("yeeeessss!!!")
    'yeess!!'
    """
    return re.sub(r"(.)\1{2,}", r"\1\1", text)


@beartype
def remove_stopwords(tokens: list[str]) -> list[str]:
    """
    Remove common stopwords from a list of tokens.

    Parameters
    ----------
    tokens : list of str
        List of input tokens.
    stop_words : set of str, optional
        Set of stopwords to remove. If None, uses NLTK's English stopwords.

    Returns
    -------
    list of str
        List of tokens with stopwords removed.
    """
    stop_words: list[str] = stopwords.words("english")
    return [token for token in tokens if token not in stop_words]


@beartype
def stem_tokens(tokens: list[str]) -> list[str]:
    """
    Apply stemming to a list of tokens using the Snowball stemmer.

    Parameters
    ----------
    tokens : list of str
        List of input tokens.
    language : str, optional
        Language for the stemmer, by default "english".

    Returns
    -------
    list of str
        List of stemmed tokens.
    """
    stemmer = SnowballStemmer(language="english")
    return [stemmer.stem(token) for token in tokens]


@beartype
def lemmatize_tokens(tokens: list[str]) -> list[str]:
    """
    Apply lemmatization to a list of tokens using the WordNet lemmatizer.

    Parameters
    ----------
    tokens : list of str
        List of input tokens.

    Returns
    -------
    list of str
        List of lemmatized tokens.
    """
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]
