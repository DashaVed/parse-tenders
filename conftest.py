import pytest


@pytest.fixture(scope='session')
def celery_config():
    return {
        "task_always_eager": True,
    }
