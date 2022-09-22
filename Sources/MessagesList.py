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

    def __init__(self, prompt_,
    finish_time_saved_, interval_not_finished_,
    start_time_saved_, interval_not_started_,
    write_report_, work_statistics_,
    employee_activity_, intervals_started_,
    intervals_finished_, unfinished_session_,
    unfinished_interval_, enter_employee_name_,
    duration_, tasks_completed_,
    today_stats_) -> None:
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
