from typing import Any, Union

from .steps import PreprocessingStep


class Pipeline:
    def __init__(self, steps: list[PreprocessingStep]):
        self.steps = steps

    def __call__(self, input: Any) -> Any:
        value = input
        for step in self.steps:
            value = step(value)
        return value

    def __or__(self, other: Union[PreprocessingStep, "Pipeline"]) -> "Pipeline":
        if isinstance(other, Pipeline):
            return Pipeline(self.steps + other.steps)
        return Pipeline(self.steps + [other])

    def add(self, step: PreprocessingStep) -> "Pipeline":
        self.steps.append(step)
        return self

    def __repr__(self) -> str:
        names = " -> ".join(step.__class__.__name__ for step in self.steps)
        return f"Pipeline({names})"

    __str__ = __repr__
