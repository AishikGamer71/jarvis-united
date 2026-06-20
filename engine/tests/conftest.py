import pytest

@pytest.fixture
def mock_llm():
    class MockLLM:
        async def generate(self, prompt):
            return "Mocked response"
    return MockLLM()

@pytest.fixture
def fake_redis():
    class FakeRedis:
        def __init__(self):
            self.store = {}
        async def get(self, key):
            return self.store.get(key)
        async def set(self, key, value):
            self.store[key] = value
    return FakeRedis()

@pytest.fixture
def test_db():
    # Setup test DB instance
    yield
    # Teardown
