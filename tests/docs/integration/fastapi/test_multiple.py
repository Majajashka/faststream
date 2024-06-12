import pytest
from fastapi.testclient import TestClient

from tests.marks import (
    require_aiokafka,
    require_aiopika,
    require_confluent,
    require_nats,
    require_redis,
)


class BaseCase:
    def test_running(self, data):
        app, broker = data

        handlers = broker._subscribers.values()

        assert len(handlers) == 2
        for h in handlers:
            assert not h.running

        with TestClient(app):
            for h in handlers:
                assert h.running


@pytest.mark.kafka()
@require_aiokafka
class TestKafka(BaseCase):
    @pytest.fixture(scope="class")
    def data(self):
        from docs.docs_src.integrations.fastapi.kafka.multiple import app, core_router

        return (app, core_router.broker)


@pytest.mark.confluent()
@require_confluent
class TestConfluent(BaseCase):
    @pytest.fixture(scope="class")
    def data(self):
        from docs.docs_src.integrations.fastapi.confluent.multiple import (
            app,
            core_router,
        )

        return (app, core_router.broker)


@pytest.mark.nats()
@require_nats
class TestNats(BaseCase):
    @pytest.fixture(scope="class")
    def data(self):
        from docs.docs_src.integrations.fastapi.nats.multiple import app, core_router

        return (app, core_router.broker)


@pytest.mark.rabbit()
@require_aiopika
class TestRabbit(BaseCase):
    @pytest.fixture(scope="class")
    def data(self):
        from docs.docs_src.integrations.fastapi.rabbit.multiple import app, core_router

        return (app, core_router.broker)


@pytest.mark.redis()
@require_redis
class TestRedis(BaseCase):
    @pytest.fixture(scope="class")
    def data(self):
        from docs.docs_src.integrations.fastapi.redis.multiple import app, core_router

        return (app, core_router.broker)
