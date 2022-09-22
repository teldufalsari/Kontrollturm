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
