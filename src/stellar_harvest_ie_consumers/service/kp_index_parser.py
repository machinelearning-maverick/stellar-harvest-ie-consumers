from typing import Dict, Optional
from datetime import datetime

from stellar_harvest_ie_models.stellar.swpc.entities import KpIndexEntity

from stellar_harvest_ie_config.utils.log_decorators import log_io

class KpIndexConsumerParser:
    @staticmethod
    @log_io
    def parse(data: Dict) -> KpIndexEntity:
        time_tag_raw = data["time_tag"]
        if isinstance(time_tag_raw, str):
            time_tag = datetime.fromisoformat(time_tag_raw.replace("Z", "+00:00"))
        else:
            time_tag = time_tag_raw

        kp_index = int(data["kp_index"])
        estimated_kp_raw = data["estimated_kp"]
        estimated_kp: Optional[float] = (
            float(estimated_kp_raw) if estimated_kp_raw is not None else None
        )
        kp_str: Optional[str] = data["kp"]

        return KpIndexEntity(
            time_tag=time_tag, kp_index=kp_index, estimated_kp=estimated_kp, kp=kp_str
        )
