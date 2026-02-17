import logging

def errlogger(dir: str, err: str) -> None:
    logging.basicConfig(
        filename=dir + '/errors.log',
        level=logging.ERROR,
        format='%(asctime)s:%(message)s'
    )
    logging.error(f" Ошибка! {err}")
