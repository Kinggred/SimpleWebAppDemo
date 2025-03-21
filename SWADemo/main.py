from logging import DEBUG, getLogger

from mangum import Mangum

from SWADemo.api.api import app
from SWADemo.integrations.S3Handler import S3Handler
from SWADemo.models.enums.events import EventType

logger = getLogger(__name__)
logger.setLevel(DEBUG)


def recognize_event(event) -> EventType:
    """
    Not a proper logic
    """
    if "Records" not in event:
        return EventType.API_EVENT
    return EventType.S3_EVENT


def handler(event, context):
    logger.debug(event)
    try:
        match recognize_event(event):
            case EventType.S3_EVENT:
                logger.info("Received S3 event")
                record = event["Records"][0]
                logger.debug(record)
                s3 = S3Handler(record)
                s3.handle_event()
            case EventType.API_EVENT:
                man = Mangum(app, lifespan="off")
                return man(event, context)
    except KeyError:
        logger.error(f"Unknown event type: {event}")
