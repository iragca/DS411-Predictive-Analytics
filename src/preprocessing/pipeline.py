from typing import Any, Callable, Union


class Pipeline:
    """
    A simple function-based processing pipeline.

    Each step is a callable that accepts one argument and returns a value.
    The output of one step is passed as the input to the next.

    Parameters
    ----------
    steps : list of Callable[[Any], Any]
        A list of callables that will be applied in sequence.

    Examples
    --------
    >>> from src.preprocessing import steps as ps
    >>> pipeline = Pipeline([
    ...     ps.to_lowercase,
    ...     ps.remove_punctuation,
    ...     ps.tokenize,
    ...     ps.remove_stopwords,
    ... ])
    >>> result = pipeline("This is an example sentence, with punctuation!")
    >>> print(result)
    ['example', 'sentence', 'punctuation']
    >>> pipeline2 = Pipeline([
    ...     lambda x: x * 5,
    ...     lambda x: x + 2,
    ... ])
    >>> result = pipeline2(3)
    >>> print(result)
    17
    """

    def __init__(self, steps: list[Callable[[Any], Any]]):
        self.steps = steps

    def __call__(self, input: Any) -> Any:
        """
        Execute the pipeline on the provided input.

        Parameters
        ----------
        input : Any
            The initial value to be processed.

        Returns
        -------
        Any
            The final output after applying all steps sequentially.
        """
        value = input
        for step in self.steps:
            value = step(value)
        return value

    def __or__(self, other: Union[Callable, "Pipeline"]) -> "Pipeline":
        """
        Combine this pipeline with another callable or pipeline using the `|` operator.

        Parameters
        ----------
        other : Callable or Pipeline
            If a Pipeline, its steps are appended.
            If a callable, it is added as the final step.

        Returns
        -------
        Pipeline
            A new pipeline with combined steps.
        """
        if isinstance(other, Pipeline):
            return Pipeline(self.steps + other.steps)
        return Pipeline(self.steps + [other])

    def add(self, step: Callable) -> "Pipeline":
        """
        Append a step to the current pipeline.

        Parameters
        ----------
        step : Callable
            A function to append to the pipeline.

        Returns
        -------
        Pipeline
            The pipeline instance (enables chaining).
        """
        self.steps.append(step)
        return self

    def __repr__(self) -> str:
        """
        Return a string representation of the pipeline with visual arrows.

        Returns
        -------
        str
            A formatted representation of the pipeline and its steps.
        """
        indent = "  "
        arrows = "\n    ⬇\n".join(f"{indent}{step.__name__}" for step in self.steps)
        return f"Pipeline(\n{arrows}\n)"

    __str__ = __repr__
