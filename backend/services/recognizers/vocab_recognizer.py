import pymorphy2
import pymorphy2.tokenizers

from presidio_analyzer.nlp_engine import NlpArtifacts
from presidio_analyzer import EntityRecognizer, RecognizerResult, AnalysisExplanation
from typing import List, Dict


class VocabularyBasedRecognizer(EntityRecognizer):

    def __init__(
        self,
        path_to_vocabularies: Dict[str, str],
        name: str = None,
    ):
        self.path_to_vocabularies = path_to_vocabularies

        self.morph = None
        self.vocab = None

        self.score = 1.0

        super().__init__(list(path_to_vocabularies.keys()), name, "ru", "0.0.1", None)

    def load(self) -> None:
        self.morph = pymorphy2.MorphAnalyzer()

        self.vocab = {
            vocab_name: self._load_vocabulary(vocab_path) for vocab_name, vocab_path in self.path_to_vocabularies.items()
        }

    def analyze(
        self, text: str, entities: List[str], nlp_artifacts: NlpArtifacts = None
    ) -> List[RecognizerResult]:

        tokens = pymorphy2.tokenizers.simple_word_tokenize(text)

        results: list[RecognizerResult] = []
        for token in tokens:
            parsed_token = self.morph.parse(token)[0]

            for entity in self.vocab.keys():
                if token in self.vocab[entity] and parsed_token.tag.POS == "NOUN":
                    textual_explanation = f"Found word {token} in vocabulary {entity}"

                    start, end = self._get_start_end_indexes(text, token)

                    results.append(RecognizerResult(
                        start=start,
                        end=end,
                        entity_type=entity,
                        score=self.score,
                        analysis_explanation=AnalysisExplanation(
                            recognizer=self.name, textual_explanation=textual_explanation, original_score=self.score
                        )
                    ))
                else:
                    lemma = parsed_token.normal_form

                    if lemma in self.vocab[entity] and parsed_token.tag.POS == "NOUN" and parsed_token.score >= 0.5:
                        textual_explanation = f"Found lemma {lemma} in vocabulary {entity}"

                        start, end = self._get_start_end_indexes(text, token)

                        results.append(RecognizerResult(
                            start=start,
                            end=end,
                            entity_type=entity,
                            score=self.score,
                            analysis_explanation=AnalysisExplanation(
                                recognizer=self.name, textual_explanation=textual_explanation, original_score=self.score
                            )
                        ))

        return results

    @staticmethod
    def _load_vocabulary(path: str) -> set[str]:
        with open(path, encoding="utf-8") as f:
            vocab: list[str] = f.readlines()

            vocab = list(map(lambda x: x.strip().lower(), vocab))

        return set(vocab)

    @staticmethod
    def _get_start_end_indexes(text: str, word: str) -> tuple[int]:
        start = text.find(word)

        if start == -1:
            raise ValueError(f"Can't find substring {word} in string.")

        end = start + len(word)

        return start, end