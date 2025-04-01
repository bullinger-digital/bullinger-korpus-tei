#!/usr/bin/env python3
# coding: utf8

""" Language modeling with character-level n-grams """

import math
from collections import defaultdict
from collections import Counter


class CharLM:

	""" A character-level n-gram language model. """

	BOS_SYMBOL = object()
	EOS_SYMBOL = object()

	def __init__(self, n=3, smoothing=1):
		""" Initialise a language model of order @param n. """
		self._order = n
		self._logprobs = defaultdict(lambda: defaultdict(float))
		self._smoothing = smoothing

	@staticmethod
	def log(probability): return math.log2(probability)

	@staticmethod
	def perplexity(log_probability, n_items): return math.pow(2, -log_probability/n_items)

	def _extract_ngrams(self, sentence):
		symbols = [self.BOS_SYMBOL] * (self._order-1) + [char for char in sentence] + [self.EOS_SYMBOL]
		return list(zip(*[symbols[i:] for i in range(self._order)]))

	def _add_ngram(self, head, history, log_probability):
		self._logprobs[history][head] = log_probability

	def _set_unk_given_unknown_history(self, log_probability):
		self._logprobs.default_factory = lambda: defaultdict(lambda: log_probability)

	def _set_unk_given_known_history(self, history, log_probability):
		self._logprobs[history].default_factory = lambda: log_probability

	def train(self, training_data):
		with open(training_data, 'r') as infile:
			ngrams = Counter([ngram for line in infile for ngram in self._extract_ngrams(line)])
		histories = Counter([elem[:-1] for elem in ngrams])
		v = len(histories)
		for ngram in ngrams:
			head, history = ngram[-1], ngram[:-1]
			log_probability = self.log((ngrams[ngram]+self._smoothing)/(histories[history]+self._smoothing*v))
			self._add_ngram(head, history, log_probability)
		for history in histories:
			self._set_unk_given_known_history(history, self.log(self._smoothing/(histories[history]+self._smoothing*v)))
		self._set_unk_given_unknown_history(self.log(self._smoothing/(self._smoothing*v)))

	def get_perplexity(self, sentence):
		log_probability = 0.0
		for ngram in self._extract_ngrams(sentence):
			head, history = ngram[-1], ngram[:-1]
			log_probability += self._logprobs[history][head]
		return self.perplexity(log_probability, len(sentence)+1)
