from logger_main import DashboardLogger


def test_logger_1():
    logger = DashboardLogger()
    for i in range(1, 100):
        logger.log_scalers("test", {"metrics0": i, "metrics1": i * 2})


test_logger_1()
