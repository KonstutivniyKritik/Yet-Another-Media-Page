import pathlib


BaseDirectory = str(pathlib.Path(__file__).parent.resolve()) + '/'
SourceDirectory = BaseDirectory + 'source/'
LocalDerictory = BaseDirectory + 'local/'
ConfigDirectory = BaseDirectory + 'configuration_files/'
TBotConfigFile = ConfigDirectory + 'TelegramBotConfiguration.ini'
RScrConfigFile = ConfigDirectory + 'RedditScraperConfiguration.ini'
Font = BaseDirectory + "arial.ttf"
PassWord = "Password"
