# app/monitoring.py
from opentelemetry import metrics, trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.exporter.cloud_monitoring import CloudMonitoringSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter

class MonitoringConfig:
    def __init__(self):
        self._initialize_tracing()
        self._initialize_metrics()
        
    def _initialize_tracing(self):
        """Initialize OpenTelemetry tracing."""
        self.tracer_provider = TracerProvider()
        self.tracer = trace.get_tracer(__name__)
        
        # Initialize exporters
        trace_exporter = CloudTraceSpanExporter()
        self.tracer_provider.add_span_processor(
            SimpleSpanProcessor(trace_exporter)
        )
        
    def _initialize_metrics(self):
        """Initialize OpenTelemetry metrics."""
        self.meter_provider = MeterProvider()
        self.meter = metrics.get_meter(__name__)
        
        # Create metrics
        self.request_counter = self.meter.create_counter(
            "api_requests",
            description="Total API requests",
            unit="1"
        )
        self.latency_histogram = self.meter.create_histogram(
            "request_latency",
            description="Request latency distribution",
            unit="ms"
        )