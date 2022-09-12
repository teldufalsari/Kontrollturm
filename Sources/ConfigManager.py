import configparser as cfg
from os.path import exists

def loadConfig(path) -> cfg.ConfigParser:
    config = cfg.ConfigParser()
    config.read(path)
    return config


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


class ConfigParser:
    def __init__(self) -> None:
        if exists('settings.ini'):
            self.settings = loadConfig('settings.ini')
        else:
            self.createDefaultConfig('settings.ini')
            self.settings = loadConfig('settings.ini')
        
        msg_file_path = 'lang/' + self.settings['GENERAL']['language']
        if not exists(msg_file_path):
            print('file ' + msg_file_path + ' does not exist, falling back to defaults')
            if not exists('lang/en_GB'):
                self.createDefaultLangFile('lang/en_GB')
            self.messages = loadConfig('lang/en_GB')
        else:
            self.messages = loadConfig(msg_file_path)


    def createDefaultConfig(self, path) -> None:
        default_config = cfg.ConfigParser()
        default_config['GENERAL'] = {
            'token' : '#write_your_token_here',
            'log_file_path' : 'KT_log.txt',
            'database_file_path' : 'KT_database.s3db',
            'language' : 'en_GB',
        }
        default_config['UNPRIVILEGED_USERS'] = {
            '#[Write Telegram id here]' : '[Write an alias that will show up in the app]',
        }
        default_config['PRIVILEGED_USERS'] = {
            '#[Write Telegram id here]' : '[Write an alias here]',
        }
        with open(path, 'w') as config_file:
            default_config.write(config_file)


    def createDefaultLangFile(self, path) -> None:
        default_lang_file = cfg.ConfigParser()
        default_lang_file['MESSAGES'] = {
            'prompt' : 'Welcome the the Kontrollturm!',
            'finish_time_saved' : 'Job finish time has been saved',
            'interval_not_finished' : 'You have not finished your job interval yet. Press "Finish" to do so',
            'start_time_saved' : 'Job start time has been saved',
            'interval_not_started' : 'You have not started your job session yet. Press "Start" to to so',
            'write_report' : 'Write a brief report of your session if you are finising the session, or write "break" if you are leaving for a break',
            'work_statistics' : 'Employee work statistics',
            'employee_activity' : 'Employee activity:',
            'intervals_started' : 'Intervals started:',
            'intervals_finished' : 'Intervals finished:',
            'unfinished_session' : 'Unfinished session:',
            'unfinished_interval' : 'Unfinished interval',
            'enter_employee_name' : 'Enter employee name to retrieve their statistics',
            'duration' : 'Duration:',
            'tasks_completed' : 'Tasks completed:',
            'today_stats' : 'Employee statistics for today',
        }
        with open(path, 'w') as lang_file:
            default_lang_file.write(lang_file)


    def loadMessages(self) -> MessagesList:
        return MessagesList(
            self.messages['MESSAGES']['prompt'],
            self.messages['MESSAGES']['finish_time_saved'],
            self.messages['MESSAGES']['interval_not_finished'],
            self.messages['MESSAGES']['start_time_saved'],
            self.messages['MESSAGES']['interval_not_started'],
            self.messages['MESSAGES']['write_report'],
            self.messages['MESSAGES']['work_statistics'],
            self.messages['MESSAGES']['employee_activity'],
            self.messages['MESSAGES']['intervals_started'],
            self.messages['MESSAGES']['intervals_finished'],
            self.messages['MESSAGES']['unfinished_session'],
            self.messages['MESSAGES']['unfinished_interval'],
            self.messages['MESSAGES']['enter_employee_name'],
            self.messages['MESSAGES']['duration'],
            self.messages['MESSAGES']['tasks_completed'],
            self.messages['MESSAGES']['today_stats'],
        )
    
    def loadSettings(self) -> SettingsList:
        return SettingsList(
            self.settings['GENERAL']['token'],
            self.settings['GENERAL']['log_file_path'],
            self.settings['GENERAL']['database_file_path'],
            self.settings['GENERAL']['language'],
        )


class ConfigManager:
    settings : SettingsList
    messages : MessagesList
    privileged_users : dict
    unprivileged_users : dict

    def __init__(self) -> None:
        parser = ConfigParser()
        self.settings = parser.loadSettings()
        self.messages = parser.loadMessages()
        self.privileged_users = {}
        for username in parser.settings['PRIVILEGED_USERS']:
            self.privileged_users.update({username : parser.settings['PRIVILEGED_USERS'].get(username, fallback=username)})
        self.unprivileged_users = {}
        for username in parser.settings['UNPRIVILEGED_USERS']:
            self.unprivileged_users.update({username : parser.settings['UNPRIVILEGED_USERS'].get(username, fallback=username)})
