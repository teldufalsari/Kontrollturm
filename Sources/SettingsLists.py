class ButtonsList():
    start_interval = ''
    finish_interval = ''
    info = ''
    today_report = ''
    status = ''
    downloads = ''
    download_user = ''
    download_day = ''
    download_whole_csv = ''
    download_whole_db = ''

    def __init__(self, start_interval_, finish_interval_, info_, today_report_, status_,
                 downloads_, download_user_, download_day_, download_whole_csv_, download_whole_db_) -> None:
        self.start_interval = start_interval_
        self.finish_interval = finish_interval_
        self.info = info_
        self.today_report = today_report_
        self.status = status_
        self.downloads = downloads_
        self.download_user = download_user_
        self.download_day = download_day_
        self.download_whole_csv = download_whole_csv_
        self.download_whole_db = download_whole_db_


class SettingsList():
    token = ''
    log_file_path = ''
    database_file_path = ''
    language = ''

    def __init__(self, token_, log_file_path_, database_file_path_, language_) -> None:
        self.token = token_
        self.log_file_path = log_file_path_
        self.database_file_path = database_file_path_
        self.language = language_


class MessagesList():
    prompt = ''
    finish_time_saved = ''
    interval_not_finished = ''
    start_time_saved = ''
    interval_not_started = ''
    write_report = ''
    work_statistics = ''
    employee_activity = ''
    intervals_started = ''
    intervals_finished = ''
    unfinished_session = ''
    unfinished_interval = ''
    enter_employee_name = ''
    duration = ''
    tasks_completed = ''
    today_stats = ''
    nothing_to_download = ''

    def __init__(self, prompt_,
    finish_time_saved_, interval_not_finished_,
    start_time_saved_, interval_not_started_,
    write_report_, work_statistics_,
    employee_activity_, intervals_started_,
    intervals_finished_, unfinished_session_,
    unfinished_interval_, enter_employee_name_,
    duration_, tasks_completed_,
    today_stats_,
    nothing_to_download_) -> None:
        self.prompt = prompt_
        self.finish_time_saved = finish_time_saved_
        self.interval_not_finished = interval_not_finished_
        self.start_time_saved = start_time_saved_
        self.interval_not_started = interval_not_started_
        self.write_report = write_report_
        self.work_statistics = work_statistics_
        self.employee_activity = employee_activity_
        self.intervals_started = intervals_started_
        self.intervals_finished = intervals_finished_
        self.unfinished_session = unfinished_session_
        self.unfinished_interval = unfinished_interval_
        self.enter_employee_name = enter_employee_name_
        self.duration = duration_
        self.tasks_completed = tasks_completed_
        self.today_stats = today_stats_
        self.nothing_to_download = nothing_to_download_
