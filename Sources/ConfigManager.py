import configparser as cfg
from os.path import exists

from Sources.MenuBuilder import MenuBuilder
from Sources.SettingsLists import ButtonsList, MessagesList, SettingsList

def loadConfig(path) -> cfg.ConfigParser:
    config = cfg.ConfigParser()
    config.read(path)
    return config


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
            'interval_not_finished' : 'You have not finished your job interval yet. Press "Finish interval" to do so',
            'start_time_saved' : 'Job start time has been saved',
            'interval_not_started' : 'You have not started your job session yet. Press "Start interval" to to so',
            'write_report' : 'Write a brief report of your session if you are finising the session, or write "break" if you are leaving for a break',
            'work_statistics' : 'Statistics for employee',
            'employee_activity' : 'Employee activity',
            'intervals_started' : 'Intervals started',
            'intervals_finished' : 'Intervals finished',
            'unfinished_session' : 'Unfinished session',
            'unfinished_interval' : 'Unfinished interval',
            'enter_employee_name' : 'Enter employee name to retrieve their statistics',
            'duration' : 'Duration',
            'tasks_completed' : 'Tasks completed',
            'today_stats' : 'Employee statistics for today',
            'nothing_to_download' : 'Nothing to download',
        }
        default_lang_file['BUTTONS'] = {
            'start_interval' : 'Start interval',
            'finish_interval' : 'Finish interval',
            'info' : 'Info',
            'today_report' : 'Report for today',
            'status' : 'Status',
            'downloads' : 'Downloads',
            'download_user' : 'Downloads stats for employee',
            'download_day' : 'Download stats for today',
            'download_whole_csv' : 'Download whole DB (.csv)',
            'download_whole_db' : 'Download whole DB (.s3db)',
        }
        with open(path, 'w') as lang_file:
            default_lang_file.write(lang_file)


    def loadMessages(self) -> MessagesList:
        msgs = self.messages['MESSAGES']
        return MessagesList(
            msgs['prompt'],
            msgs['finish_time_saved'],
            msgs['interval_not_finished'],
            msgs['start_time_saved'],
            msgs['interval_not_started'],
            msgs['write_report'],
            msgs['work_statistics'],
            msgs['employee_activity'],
            msgs['intervals_started'],
            msgs['intervals_finished'],
            msgs['unfinished_session'],
            msgs['unfinished_interval'],
            msgs['enter_employee_name'],
            msgs['duration'],
            msgs['tasks_completed'],
            msgs['today_stats'],
            msgs['nothing_to_download'],
        )

    def loadSettings(self) -> SettingsList:
        return SettingsList(
            self.settings['GENERAL']['token'],
            self.settings['GENERAL']['log_file_path'],
            self.settings['GENERAL']['database_file_path'],
            self.settings['GENERAL']['language'],
        )

    def loadButtons(self) -> ButtonsList:
        btns = self.messages['BUTTONS']
        return ButtonsList(
            btns['start_interval'],
            btns['finish_interval'],
            btns['info'],
            btns['today_report'],
            btns['status'],
            btns['downloads'],
            btns['download_user'],
            btns['download_day'],
            btns['download_whole_csv'],
            btns['download_whole_db'],
        )


class ConfigManager:
    settings : SettingsList
    messages : MessagesList
    menu_builder : MenuBuilder
    privileged_users : dict
    unprivileged_users : dict

    def __init__(self) -> None:
        parser = ConfigParser()
        self.settings = parser.loadSettings()
        self.messages = parser.loadMessages()
        self.menu_builder = MenuBuilder(parser.loadButtons())
        self.privileged_users = {}
        for username in parser.settings['PRIVILEGED_USERS']:
            self.privileged_users.update({username : parser.settings['PRIVILEGED_USERS'].get(username, fallback=username)})
        self.unprivileged_users = {}
        for username in parser.settings['UNPRIVILEGED_USERS']:
            self.unprivileged_users.update({username : parser.settings['UNPRIVILEGED_USERS'].get(username, fallback=username)})
