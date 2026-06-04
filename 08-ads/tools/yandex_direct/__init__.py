"""Лёгкий клиент Yandex Direct API v5 (stdlib, zero-dep).

См. README.md в этой папке — возможности API, форматы объявлений, char-лимиты,
таргетинги и safety-режимы. Точка входа для запуска кампаний — ../build_campaign.py.
"""
from .client import DirectClient, DirectError, Units
from .services import Services

__all__ = ["DirectClient", "DirectError", "Units", "Services"]
