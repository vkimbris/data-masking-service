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

        results = []
        search_pos = 0

        for token in tokens:
            parsed = self.morph.parse(token)[0]
            start = text.find(token, search_pos)

            if start == -1:
                continue

            end = start + len(token)
            search_pos = end

            for entity in self.vocab:
                if parsed.tag.POS == "NOUN" and (
                        token.lower() in self.vocab[entity]
                        or parsed.normal_form in self.vocab[entity] and parsed.score >= 0.5
                ):
                    explanation = (f"Found {'lemma' if parsed.normal_form in self.vocab[entity] else 'word'} "
                                   f"{parsed.normal_form if parsed.normal_form in self.vocab[entity] else token} "
                                   f"in vocabulary {entity}")

                    results.append(RecognizerResult(
                        start=start, end=end, entity_type=entity,
                        score=self.score,
                        analysis_explanation=AnalysisExplanation(
                            recognizer=self.name,
                            textual_explanation=explanation,
                            original_score=self.score
                        )
                    ))

        return results

    @staticmethod
    def _load_vocabulary(path: str) -> set[str]:
        with open(path, encoding="utf-8") as f:
            vocab: list[str] = f.readlines()

            vocab = list(map(lambda x: x.strip().lower(), vocab))

        return set(vocab)
