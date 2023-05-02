import functools
import os
from contextlib import nullcontext
from typing import Callable, ContextManager

from dotenv import load_dotenv
from flask import Flask, request
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import Span, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import NonRecordingSpan


load_dotenv()


def request_hook(span: Span, environ) -> None:
    if span and span.is_recording():
        request_id = request.headers["X-Request-Id"]
        span.set_attribute("http.request_id", request_id)


def configure_tracer(app: Flask) -> None:
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create(
                attributes={
                    SERVICE_NAME: "auth_app",
                },
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=os.getenv("JAEGER_HOST", default="jaeger"),
                agent_port=int(os.getenv("JAEGER_PORT", default=6831)),
            )
        )
    )
    FlaskInstrumentor().instrument_app(
        app=app,
        excluded_urls="/api/ping,/swagger.json,/api/swagger,/swaggerui/*",
        request_hook=request_hook,
    )
    RequestsInstrumentor().instrument()


def get_span(func: Callable, name: str) -> ContextManager:
    if isinstance(trace.get_current_span(), NonRecordingSpan):
        return nullcontext()
    return trace.get_tracer(func.__module__).start_as_current_span(name)


def trace_request(name: str):
    def decorator_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with get_span(func, name):
                return func(*args, **kwargs)

        return wrapper

    return decorator_func
