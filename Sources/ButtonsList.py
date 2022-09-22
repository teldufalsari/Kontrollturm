class ButtonsList():
    start_interval = ''
    finish_interval = ''
    info = ''
    today_report = ''
    status = ''

    def __init__(self, start_interval_, finish_interval_, info_, today_report_, status_) -> None:
        self.start_interval = start_interval_
        self.finish_interval = finish_interval_
        self.info = info_
        self.today_report = today_report_
        self.status = status_
