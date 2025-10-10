import pytest
from src.preprocessing import Pipeline


@pytest.mark.parametrize(
    "steps,input,expected",
    [
        (  # Test with simple functions
            [str.lower, lambda s: s + " world", str.upper],
            "hello",
            "HELLO WORLD",
        ),
        ([lambda x: x * 3], 5, 15),  # Test with a single step
        ([], "test", "test"),  # Test with no steps (identity function)
        ([lambda x: x + 1, lambda x: x * 2, str], 3, "8"),  # Test with mixed types
    ],
)
def test_pipeline(steps, input, expected):
    pipeline = Pipeline(steps)
    result = pipeline(input)
    assert result == expected
