import re
from typing import Callable, Generic, TypeVar

import contractions
from autocorrect import Speller
from beartype import beartype

T = TypeVar("T")  # Input type of the current step
U = TypeVar("U")  # Output type of the current step
V = TypeVar("V")  # Output type of the next step


class PreprocessingStep(Generic[T, U]):
    """A class representing a single preprocessing step.

    To implement a preprocessing step, subclass this and implement then
    initialize the parent class with the function that performs the step.
    """

    def __init__(self, func: Callable[[T], U]) -> None:
        self.func = func

    def __call__(self, input: T) -> U:
        return self.func(input)

    def __or__(self, other: "PreprocessingStep[U, V]") -> "PreprocessingStep[T, V]":
        return PreprocessingStep(lambda text: other(self(text)))


class ToLowercase(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__(self.to_lowercase)

    @beartype
    def to_lowercase(self, text: str) -> str:
        return text.lower()


class StripWhitespace(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__(self.strip_whitespace)

    @beartype
    def strip_whitespace(self, text: str) -> str:
        return text.strip()


class RemovePunctuation(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__(self.remove_punctuation)

    @beartype
    def remove_punctuation(self, text: str) -> str:
        return re.sub(r"[^\w\s]", "", text)


class CorrectSpelling(PreprocessingStep):
    def __init__(self, speller: Speller = Speller(lang="en")) -> None:
        self.speller = speller
        super().__init__(self.correct_spelling)

    @beartype
    def correct_spelling(self, text: str) -> str:
        return self.speller(text)


class ExpandContractions(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__(self.expand_contractions)

    @beartype
    def expand_contractions(self, text: str) -> str:
        result = contractions.fix(text)
        if not isinstance(result, str):
            raise ValueError("Contractions.fix did not return a string")
        return result


class Tokenize(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__(self.tokenize)

    @beartype
    def tokenize(self, text: str) -> list[str]:
        return text.split()


class RemoveRepeatedCharacters(PreprocessingStep):
    def __init__(self) -> None:
        super().__init__(self.remove_repeated_characters)

    @beartype
    def remove_repeated_characters(self, text: str) -> str:
        return re.sub(r"(.)\1{2,}", r"\1\1", text)
