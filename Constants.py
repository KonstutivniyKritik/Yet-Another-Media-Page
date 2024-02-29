import pathlib


BaseDirectory = str(pathlib.Path(__file__).parent.resolve()) + '/'
SourceDirectory = BaseDirectory + 'source/'
LocalDerictory = BaseDirectory + 'local/'
ConfigDirectory = BaseDirectory + 'configurationfiles/'
TBotConfigFile = ConfigDirectory + 'TelegramBotConfiguration.ini'
RScrConfigFile = ConfigDirectory + 'RedditScraperConfiguration.ini'
PassWord = "Password"
