"""N-gram language models implemented from counts for Lab 02.

The implementation deliberately avoids ready-made language-model libraries.
It supports unigram, bigram, and trigram models; MLE and Laplace estimates;
log probability; perplexity; next-word prediction; and continuation ranking.
"""

from __future__ import annotations

from collections import Counter
import gzip
import json
from math import exp, inf, log
from pathlib import Path
import re
from typing import Iterable, Iterator, Sequence
import unicodedata


BOS = "<s>"
EOS = "</s>"
UNK = "<UNK>"

_TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")
_SENTENCE_BOUNDARY = re.compile(r"[.!?]+|\n+")


def tokenize(text: str) -> list[str]:
    """Normalize English text and return word/number tokens."""
    normalized = unicodedata.normalize("NFKC", text).lower()
    return _TOKEN_PATTERN.findall(normalized)


def split_sentences(text: str, max_length: int = 80) -> list[list[str]]:
    """Split a document into tokenized sentences, chunking very long spans."""
    normalized = unicodedata.normalize("NFKC", text).lower()
    sentences: list[list[str]] = []
    for span in _SENTENCE_BOUNDARY.split(normalized):
        tokens = _TOKEN_PATTERN.findall(span)
        for start in range(0, len(tokens), max_length):
            chunk = tokens[start : start + max_length]
            if chunk:
                sentences.append(chunk)
    return sentences


def load_c4_documents(path: str | Path, limit: int | None = None) -> list[str]:
    """Load text fields from the gzipped JSON Lines C4 sample."""
    documents: list[str] = []
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            documents.append(json.loads(line)["text"])
            if limit is not None and len(documents) >= limit:
                break
    return documents


def prepare_sentences(
    documents: Iterable[str], max_sentence_length: int = 80
) -> list[list[str]]:
    """Convert documents into tokenized sentences."""
    return [
        sentence
        for document in documents
        for sentence in split_sentences(document, max_length=max_sentence_length)
    ]


def build_vocabulary(
    corpus: Iterable[Sequence[str]], min_count: int = 1
) -> set[str]:
    """Build a token vocabulary and reserve UNK/EOS symbols."""
    if min_count < 1:
        raise ValueError("min_count must be at least 1")
    counts = Counter(token for sentence in corpus for token in sentence)
    vocabulary = {token for token, count in counts.items() if count >= min_count}
    vocabulary.update({UNK, EOS})
    return vocabulary


def _mapped_sentence(sentence: Sequence[str], vocabulary: set[str]) -> list[str]:
    return [token if token in vocabulary else UNK for token in sentence]


def iter_ngrams(
    sentence: Sequence[str], n: int, vocabulary: set[str] | None = None
) -> Iterator[tuple[str, ...]]:
    """Yield padded n-grams for one sentence, including an EOS prediction."""
    if n not in {1, 2, 3}:
        raise ValueError("n must be 1, 2, or 3")
    tokens = list(sentence)
    if vocabulary is not None:
        tokens = _mapped_sentence(tokens, vocabulary)
    padded = [BOS] * (n - 1) + tokens + [EOS]
    for index in range(len(padded) - n + 1):
        yield tuple(padded[index : index + n])


def count_ngrams(
    corpus: Iterable[Sequence[str]],
    n: int,
    vocabulary: set[str] | None = None,
) -> Counter[tuple[str, ...]]:
    """Count padded n-grams in a tokenized corpus."""
    counts: Counter[tuple[str, ...]] = Counter()
    for sentence in corpus:
        counts.update(iter_ngrams(sentence, n, vocabulary))
    return counts


class NGramLanguageModel:
    """Count-based n-gram LM with MLE and add-one smoothing."""

    def __init__(self, n: int, min_count: int = 2) -> None:
        if n not in {1, 2, 3}:
            raise ValueError("n must be 1, 2, or 3")
        if min_count < 1:
            raise ValueError("min_count must be at least 1")
        self.n = n
        self.min_count = min_count
        self.vocabulary: set[str] = set()
        self.ngram_counts: Counter[tuple[str, ...]] = Counter()
        self.context_counts: Counter[tuple[str, ...]] = Counter()
        self.training_sentences = 0
        self.training_predictions = 0

    def fit(self, corpus: Sequence[Sequence[str]]) -> "NGramLanguageModel":
        """Estimate counts from tokenized training sentences."""
        self.vocabulary = build_vocabulary(corpus, min_count=self.min_count)
        self.ngram_counts = count_ngrams(corpus, self.n, self.vocabulary)
        self.context_counts = Counter()
        for ngram, count in self.ngram_counts.items():
            self.context_counts[ngram[:-1]] += count
        self.training_sentences = len(corpus)
        self.training_predictions = sum(self.ngram_counts.values())
        return self

    @property
    def vocabulary_size(self) -> int:
        """Number of possible predicted symbols (UNK and EOS included)."""
        return len(self.vocabulary)

    @property
    def unique_ngrams(self) -> int:
        return len(self.ngram_counts)

    @property
    def singleton_ngrams(self) -> int:
        return sum(count == 1 for count in self.ngram_counts.values())

    def _map_word(self, word: str) -> str:
        if word in {BOS, EOS}:
            return word
        return word if word in self.vocabulary else UNK

    def _context(self, context: Sequence[str]) -> tuple[str, ...]:
        if self.n == 1:
            return ()
        mapped = [self._map_word(token) for token in context]
        required = self.n - 1
        return tuple(([BOS] * required + mapped)[-required:])

    def probability(
        self,
        context: Sequence[str],
        word: str,
        smoothing: str = "mle",
    ) -> float:
        """Return P(word | context) under MLE or Laplace smoothing."""
        if not self.vocabulary:
            raise RuntimeError("fit must be called before probability")
        if smoothing not in {"mle", "laplace"}:
            raise ValueError("smoothing must be 'mle' or 'laplace'")
        history = self._context(context)
        mapped_word = self._map_word(word)
        numerator = self.ngram_counts[history + (mapped_word,)]
        denominator = self.context_counts[history]
        if smoothing == "laplace":
            return (numerator + 1) / (denominator + self.vocabulary_size)
        if denominator == 0:
            return 0.0
        return numerator / denominator

    def sentence_log_probability(
        self, sentence: Sequence[str] | str, smoothing: str = "mle"
    ) -> float:
        """Compute log P(sentence), including the EOS prediction."""
        tokens = tokenize(sentence) if isinstance(sentence, str) else list(sentence)
        mapped = [self._map_word(token) for token in tokens]
        history = [BOS] * (self.n - 1)
        total = 0.0
        for word in mapped + [EOS]:
            value = self.probability(history, word, smoothing=smoothing)
            if value == 0.0:
                return -inf
            total += log(value)
            history.append(word)
        return total

    def sentence_probability(
        self, sentence: Sequence[str] | str, smoothing: str = "mle"
    ) -> float:
        """Compute P(sentence); log probability is safer for long text."""
        value = self.sentence_log_probability(sentence, smoothing=smoothing)
        return 0.0 if value == -inf else exp(value)

    def perplexity(
        self, corpus: Iterable[Sequence[str]], smoothing: str = "mle"
    ) -> float:
        """Compute token-level perplexity, counting one EOS per sentence."""
        total_log_probability = 0.0
        prediction_count = 0
        for sentence in corpus:
            value = self.sentence_log_probability(sentence, smoothing=smoothing)
            if value == -inf:
                return inf
            total_log_probability += value
            prediction_count += len(sentence) + 1
        if prediction_count == 0:
            raise ValueError("corpus must contain at least one prediction")
        return exp(-total_log_probability / prediction_count)

    def next_word_distributions(
        self,
        contexts: Sequence[Sequence[str] | str],
        top_k: int = 5,
        smoothing: str = "laplace",
    ) -> dict[tuple[str, ...], list[tuple[str, float]]]:
        """Return Top-K next words for many contexts with one count scan."""
        if top_k < 1:
            raise ValueError("top_k must be positive")
        original_contexts: list[tuple[str, ...]] = []
        normalized_contexts: dict[tuple[str, ...], tuple[str, ...]] = {}
        for value in contexts:
            tokens = tokenize(value) if isinstance(value, str) else list(value)
            original = tuple(tokens)
            original_contexts.append(original)
            normalized_contexts[original] = self._context(tokens)

        target_histories = set(normalized_contexts.values())
        followers = {history: Counter() for history in target_histories}
        for ngram, count in self.ngram_counts.items():
            history, word = ngram[:-1], ngram[-1]
            if history in followers and word not in {EOS, UNK}:
                followers[history][word] = count

        fallback = sorted(self.vocabulary - {EOS, UNK})
        output: dict[tuple[str, ...], list[tuple[str, float]]] = {}
        for original in original_contexts:
            history = normalized_contexts[original]
            words = [word for word, _ in followers[history].most_common(top_k)]
            if len(words) < top_k:
                for word in fallback:
                    if word not in words:
                        words.append(word)
                    if len(words) >= top_k:
                        break
            output[original] = [
                (word, self.probability(history, word, smoothing=smoothing))
                for word in words
            ]
        return output

    def next_word_distribution(
        self,
        context: Sequence[str] | str,
        top_k: int = 5,
        smoothing: str = "laplace",
    ) -> list[tuple[str, float]]:
        tokens = tuple(tokenize(context) if isinstance(context, str) else context)
        return self.next_word_distributions(
            [tokens], top_k=top_k, smoothing=smoothing
        )[tokens]

    def continuation_log_probability(
        self,
        context: Sequence[str] | str,
        continuation: Sequence[str] | str,
        smoothing: str = "laplace",
        include_eos: bool = True,
    ) -> tuple[float, int]:
        """Score a continuation conditional on a supplied context."""
        context_tokens = tokenize(context) if isinstance(context, str) else list(context)
        continuation_tokens = (
            tokenize(continuation)
            if isinstance(continuation, str)
            else list(continuation)
        )
        history = [self._map_word(token) for token in context_tokens]
        targets = [self._map_word(token) for token in continuation_tokens]
        if include_eos:
            targets.append(EOS)
        total = 0.0
        for word in targets:
            value = self.probability(history, word, smoothing=smoothing)
            if value == 0.0:
                return -inf, len(targets)
            total += log(value)
            history.append(word)
        return total, len(targets)


def train_unigram(
    corpus: Sequence[Sequence[str]], min_count: int = 2
) -> NGramLanguageModel:
    return NGramLanguageModel(1, min_count=min_count).fit(corpus)


def train_bigram(
    corpus: Sequence[Sequence[str]], min_count: int = 2
) -> NGramLanguageModel:
    return NGramLanguageModel(2, min_count=min_count).fit(corpus)


def train_trigram(
    corpus: Sequence[Sequence[str]], min_count: int = 2
) -> NGramLanguageModel:
    return NGramLanguageModel(3, min_count=min_count).fit(corpus)


def probability(
    model: NGramLanguageModel,
    context: Sequence[str],
    word: str,
    smoothing: str = "mle",
) -> float:
    """Functional wrapper required by the assignment."""
    return model.probability(context, word, smoothing=smoothing)


def sentence_probability(
    model: NGramLanguageModel,
    sentence: Sequence[str] | str,
    smoothing: str = "mle",
) -> float:
    """Functional wrapper required by the assignment."""
    return model.sentence_probability(sentence, smoothing=smoothing)


def sentence_log_probability(
    model: NGramLanguageModel,
    sentence: Sequence[str] | str,
    smoothing: str = "mle",
) -> float:
    """Functional wrapper required by the assignment."""
    return model.sentence_log_probability(sentence, smoothing=smoothing)
