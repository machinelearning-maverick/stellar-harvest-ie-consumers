from datetime import datetime
from stellar_harvest_ie_models.stellar.swpc.models import KpIndexRecord as KpIndexModel


def parse_planetary_kp_index(kp_index: dict) -> dict:
    """
    Take the JSON-dict from Kafka and produce a flat dict
    with exactly the columns for your ORM model.
    """
    record: KpIndexModel = KpIndexModel(**kp_index)
    return {
        "time_tag": record.time_tag,
        "kp_index": record.kp_index,
        "estimated_kp": record.estimated_kp,
        "kp": record.kp,
    }
