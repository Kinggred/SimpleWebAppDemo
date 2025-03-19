from enum import StrEnum


class EventType(StrEnum):
    S3_EVENT = "s3_event"
    API_EVENT = "api_event"
