from presidio_analyzer import EntityRecognizer, RecognizerResult
from presidio_analyzer import PatternRecognizer, Pattern

from typing import List

from presidio_analyzer.nlp_engine import NlpArtifacts


def validate_inn_10(string: str) -> bool:
    if len(string) != 10:
        return False

    weights = [2, 4, 10, 3, 5, 9, 4, 6, 8, 0]

    numbers = list(string)
    numbers = list(map(int, numbers))

    control_number = 0
    for i in range(len(numbers)):
        control_number += weights[i] * numbers[i]
    control_number = control_number % 11

    if control_number > 9:
        control_number = control_number % 10

    if control_number == numbers[-1]:
        return True

    return False


def validate_inn_12(string: str) -> bool:
    if len(string) != 12:
        return False

    first_weights = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0]

    numbers = list(string)
    numbers = list(map(int, numbers))

    first_control_number = 0
    for i in range(len(numbers[:11])):
        first_control_number += first_weights[i] * numbers[i]
    first_control_number = first_control_number % 11

    if first_control_number > 9:
        first_control_number = first_control_number % 10

    second_weights = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0]

    second_control_number = 0
    for i in range(len(numbers)):
        second_control_number += second_weights[i] * numbers[i]
    second_control_number = second_control_number % 11

    if second_control_number > 9:
        second_control_number = second_control_number % 10

    if first_control_number == numbers[-2] and second_control_number == numbers[-1]:
        return True

    return False


def validate_iin(string: str) -> bool:
    if len(string) != 12:
        return False

    first_weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    numbers = list(string)
    numbers = list(map(int, numbers))

    control_number = 0
    for i in range(len(numbers[:11])):
        control_number += first_weights[i] * numbers[i]
    control_number = control_number % 11

    if control_number == 10:
        second_weights = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]

        control_number = 0
        for i in range(len(numbers[:11])):
            control_number += second_weights[i] * numbers[i]
        control_number = control_number % 11

        if control_number == 10:
            return False

    return control_number == numbers[-1]


class INNRecognizer(EntityRecognizer):

    def __init__(self, name: str | None = None):
        self.pattern_recognizer = None
        self.score = 1.0

        super().__init__(["INN"], name, "ru", "0.0.1", None)

    def load(self) -> None:
        patterns = [
            Pattern(name="inn_12", regex=r'\b\d{12}\b', score=self.score),
            Pattern(name="inn_10", regex=r'\b\d{10}\b', score=self.score)
        ]

        self.pattern_recognizer = PatternRecognizer(
            supported_entity="INN",
            name=self.name,
            supported_language=self.supported_language,
            patterns=patterns,
        )

    def analyze(
        self, text: str, entities: List[str], nlp_artifacts: NlpArtifacts = None
    ) -> List[RecognizerResult]:

        results: List[RecognizerResult] = []

        if "INN" not in entities:
            return results

        for ent in self.pattern_recognizer.analyze(text=text, entities=["INN"]):
            if self._validate_inn_string(text[ent.start : ent.end]):
                results.append(RecognizerResult(
                    entity_type="INN",
                    start=ent.start,
                    end=ent.end,
                    score=self.score
                ))

        return results

    @staticmethod
    def _validate_inn_string(string: str) -> bool:
        return validate_iin(string) or validate_inn_12(string) or validate_inn_10(string)
