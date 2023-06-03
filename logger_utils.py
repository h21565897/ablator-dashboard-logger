from typing import Dict, Optional
import numpy as np


def dict_to_json(payload: Dict) -> str:
    for key in payload.keys():
        val = payload[key]
        if isinstance(val, dict):
            payload[key] = dict_to_json(val)
        else:
            payload[key] = val_to_json(val)
    return payload


def val_to_json(value: any) -> str:
    if isinstance(value, np.ndarray):
        if value.size == 1:
            return value.flatten()[0]
        return value.tolist()
    return value
