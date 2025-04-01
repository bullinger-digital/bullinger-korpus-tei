#!/usr/bin/env python3
# coding: utf8

""" Language identifier based on multiple character-level models. """


import warnings


class LanguageIdentifier:

    """ Identify the language used in any string. """

    def __init__(self):
        self._models = {}

    def identify(self, sentence):
        if len(self._models) < 2: raise ValueError("At least two models are needed for language identification.")
        perplexities = {
            language_code: model.get_perplexity(sentence)
            for language_code, model in self._models.items()
        }
        return min(perplexities, key=perplexities.get)

    def get_languages(self): return list(self._models.keys())

    def add_model(self, language_code, model):
        if language_code in self._models:
            warnings.warn(
                "Already defined language code {0}. "
                "Current model will be replaced.".format(language_code))
        self._models[language_code] = model
