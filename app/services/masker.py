from abc import ABC, abstractmethod
from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_anonymizer import AnonymizerEngine, ConflictResolutionStrategy

from hydra.utils import instantiate
from omegaconf import OmegaConf

from dataclasses import dataclass

@dataclass
class MaskedOutput:
    masked_text: str
    mask_mapping: dict[str, str]

class BaseMasker(ABC):

    entities: list[str] = ["EMAIL_ADDRESS", "PHONE_NUMBER", "INN", "NAME", "SURNAME", "MIDNAME"]

    @abstractmethod
    def mask(self, text: str) -> MaskedOutput:
        pass

    @abstractmethod
    def de_mask(self, text: str, entities: dict[str, str]) -> str:
        pass

class PresidioMasker(BaseMasker):

    def __init__(self, path_to_config: str):
        self.analyzer: AnalyzerEngine = instantiate(OmegaConf.load(path_to_config).analyzer)

        self.anonymizer = AnonymizerEngine()

    def mask(self, text: str) -> MaskedOutput:
        results = self.analyzer.analyze(text, language="ru", entities=self.entities)

        results = self.anonymizer._remove_conflicts_and_get_text_manipulation_data(
            analyzer_results=results, conflict_resolution=ConflictResolutionStrategy.MERGE_SIMILAR_OR_CONTAINED
        )

        results = self._postprocess_recognizer_results(results)

        mask_mapping = self._get_mask_mapping(text, results)
        anonymizer_result = self.anonymizer.anonymize(text, analyzer_results=results)

        return MaskedOutput(masked_text=anonymizer_result.text, mask_mapping=mask_mapping)

    def de_mask(self, text: str, entities: dict[str, str]) -> str:
        for token, value in entities.items():
            text = text.replace(token, value)

        return text

    def _postprocess_recognizer_results(self, results: list[RecognizerResult]) -> list[RecognizerResult]:
        postprocessed_analyzer_result: list[RecognizerResult] = []

        for ent in self.entities:
            results_per_ent = [res for res in results if res.entity_type == ent]
            results_per_ent.sort(key=lambda x: x.start)

            postprocessed_analyzer_result.extend(
                [
                    RecognizerResult(
                        entity_type=res.entity_type + "_" + str(k),
                        start=res.start, end=res.end, score=res.score
                    )

                    for k, res in enumerate(results_per_ent)
                ]
            )

        return postprocessed_analyzer_result

    @staticmethod
    def _get_mask_mapping(text: str, results: list[RecognizerResult]) -> dict[str, str]:
        mask_mapping: dict[str, str] = {}

        for ent in results:
            mask_mapping[f"<{ent.entity_type}>"] = text[ent.start : ent.end]

        return mask_mapping