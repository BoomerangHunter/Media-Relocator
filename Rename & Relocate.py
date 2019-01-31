import re
import os
import subprocess
import logging
import json

#Generates config file if it doesn't exist
if not os.path.isfile('config.json'):
    download_location_config = input("Enter the path of your downloads: ")
    while not os.path.isdir(download_location_config):
        download_location_config = input("Unable to find directory at "
                                  + download_location_config
                                  + ". Please try again: ")
    media_location_config = input("Enter the path of your media: ")
    while not os.path.isdir(media_location_config):
        media_location = input("Unable to find directory at "
                               + media_location_config +
                               ". Please try again: ")

    paths = {
        "download_location" : download_location_config,
        "media_location" : media_location_config
    }

    json_config_content = json.dumps(paths, sort_keys = True, indent = 4)

    with open('config.json', 'w') as f:
        f.write(json_config_content)

#Load paths from config
with open('config.json') as f:
    config = json.load(f)

download_location = config['download_location']
media_location = config['media_location']
logger_location = './log.log'

#Configure Logger
log_format = "[%(levelname)s]: %(asctime)s - %(message)s"
logging.basicConfig(filename=logger_location, level=logging.DEBUG,
format = log_format, filemode = 'a')
logger = logging.getLogger()

#Set working directory
os.chdir(download_location)

#Defines regular expressions for later use
format_expression = r"\[\w+\] (.+?)- (\d{1,2}).*(\.mkv)"
season_expression = r"(.+?S)(\d) S01(.+?)(\.mkv)"


#Create a list of all files in working directory
media_files = [f for f in os.listdir(download_location) if re.match(
    format_expression, f)]

#Check to see if list is empty. If not proceeds with sorting.
if not media_files:
    logger.info("Directory contains no valid files. Exiting...\n")
    quit()
else:
    try:
        for f in media_files:
            f_new = re.sub(format_expression, r"\1S01E\2\3", f)
            if bool(re.match(season_expression, f_new)):
                f_new = re.sub(season_expression, r"\g<1>0\2\3\4", f_new)
            print(f_new)
            f_new_path = re.match(r"^(.*?)\sS0", f_new).group(1)
            f_new_path = os.path.join(media_location, f_new_path)
            if not os.path.exists(f_new_path):
                os.makedirs(f_new_path)
            os.rename(f, os.path.join(f_new_path, f_new))
            logger.info(os.path.abspath(f) + " ---> " + os.path.join(
                                                            f_new_path,
                                                            f_new))
    except Exception:
        logger.exception("Caught exception: ")

logger.info("Process complete. Exiting..." + "\n")
quit()
