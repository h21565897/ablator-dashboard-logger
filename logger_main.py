from logger_buffer import LoggerBuffer
from logger_utils import dict_to_json
import json
from typing import Dict, List
from logger_message import ScalerMessage
import copy


class TrialMetaData:
    trial_name: str = None
    project_name: str = None

    def __init__(self, trial_name: str, project_name: None):
        self.trial_name = trial_name
        self.project_name = project_name


class ScalerLogger:
    metrics_steps: Dict[str, int] = None
    message_buffer: List[str] = None
    trial_meta_data: TrialMetaData = None
    logger_buffer: LoggerBuffer = None

    def __init__(self, buffer=None, trial_meta_data=None):
        if buffer is None:
            raise ValueError("buffer can not be None")
        if trial_meta_data is None:
            raise ValueError("trial_meta_data can not be None")
        self.metrics_steps = {}
        self.message_buffer = []
        self.trial_meta_data = trial_meta_data
        self.logger_buffer = buffer

    def log(self, key: str, value: any):
        if key not in self.metrics_steps:
            self.metrics_steps[key] = 0
        self.metrics_steps[key] += 1
        scalers = {"step": self.metrics_steps[key], key: value}
        scalers = dict_to_json(scalers)
        scalers = json.dumps(scalers)
        self.message_buffer.append(scalers)
        if len(self.message_buffer) > 10:
            self.flush()

    def flush(self):
        scaler_message = ScalerMessage(
            projectName=self.trial_meta_data.project_name,
            trialName=self.trial_meta_data.trial_name,
            scalers=self.message_buffer[:],
        )
        self.message_buffer.clear()
        self.logger_buffer.append(scaler_message)


# todo: implement
class ArtifactLogger:
    pass


# todo: implement
class tableLogger:
    pass


class DashboardLogger:
    buffer: LoggerBuffer = None
    trial_meta_data: TrialMetaData = None
    scalars_logger: ScalerLogger = None

    def __init__(
        self, project_name: str = "default_project", trial_name: str = "default_trial"
    ):
        self.buffer = LoggerBuffer()
        self.trial_meta_data = TrialMetaData(trial_name, project_name)
        self.scalars_logger = ScalerLogger(self.buffer, self.trial_meta_data)

    def log_scalers(self, key: str, value: any):
        self.scalars_logger.log(key, value)
