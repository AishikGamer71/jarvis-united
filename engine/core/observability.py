from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Configure basic OpenTelemetry tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Basic console exporter (could be replaced with Jaeger/OTLP exporter in prod)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

def instrument_agent(agent_cls):
    """Decorator to instrument agent methods."""
    class InstrumentedAgent(agent_cls):
        async def act(self, *args, **kwargs):
            with tracer.start_as_current_span(f"{agent_cls.__name__}.act"):
                return await super().act(*args, **kwargs)
    return InstrumentedAgent
