from logging import getLogger

from mangum import Mangum
from SWADemo.api.api import app
from SWADemo.models.enums.events import EventType

logger = getLogger(__name__)


def recognize_event(event) -> EventType:
    """
    Not a proper logic
    """
    if "Records" not in event:
        return EventType.API_EVENT
    return EventType.S3_EVENT


def handle_event(event, context):
    try:
        match recognize_event(event):
            case EventType.S3_EVENT:
                pass
            case EventType.API_EVENT:
                return Mangum(app , event, context)
    except KeyError:
        logger.error(f"Unknown event type: {event}")
