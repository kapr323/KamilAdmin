from __future__ import absolute_import, unicode_literals

# Tímto způsobem zajistíš, že Celery bude inicializována při startu projektu
from .celery import celery_app


__all__ = ('celery_app',)
