from datetime import datetime
from stellar_harvest_ie_models.stellar.swpc.models import KpIndexRecord as KpIndexModel


def parse_planetary_kp_index(kp_index: dict):
    """ """
    record: KpIndexModel = KpIndexModel(**kp_index)
    return {"time_tag": record.time_tag}
