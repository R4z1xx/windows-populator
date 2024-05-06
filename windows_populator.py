__author__ = "R4z1xx"
__copyright__ = "Copyright (c) 2024 R4z1xx"
__license__ = "MIT"
__version__ = "1.0"

import logging
import random
import sys
import os

class LoremIpsum:
    def __init__(self):
        self.words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 
                      'elit', 'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 
                      'et', 'dolore', 'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 
                      'nostrud', 'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 
                      'ea', 'commodo', 'consequat', 'duis', 'aute', 'irure', 'dolor', 'in', 
                      'reprehenderit', 'voluptate', 'velit', 'esse', 'cillum', 'dolore', 'eu', 
                      'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint', 'occaecat', 'cupidatat', 
                      'non', 'proident', 'sunt', 'in', 'culpa', 'qui', 'officia', 'deserunt', 
                      'mollit', 'anim', 'id', 'est', 'laborum']
        
    def generate_name(self):
        """
        Generate a random name using 1 word
        from the list of words in the class
        """
        return ' '.join(random.choices(self.words, k=random.randint(1, 2)))

    def generate_content(self):
        """
        Generate random content using random
        words from the list of words in the 
        class -> between 100 and 1000 words
        """
        return ' '.join(random.choices(self.words, k=1)).capitalize() + ' '.join(random.choices(self.words, k=random.randint(100, 1000))) + '.'

class WindowsPopulator:
    def __init__(self, logger):
        self.default_users = ['Administrator', 'Public', 'Default', 'All Users', 'defaultuser0', 'Default User']
        self.folders = ['Desktop', 'Documents', 'Pictures', 'Music', 'Downloads', 'Videos']
        self.extensions = ['.txt','.docx', '.xslx', '.pptx', '.pdf', '.jpg', '.jpeg', '.png', '.mp3', '.zip']
        self.user_directory = self.get_user_directory()
        self.file_count = 0
        self.subdir_count = 0
        self.logger = logger
    
    def get_user_directory(self):
        """
        Retrieve all user directories in the system 
        and only store the ones that are not default
        """
        user_directory = []
        users_path = os.path.join(os.environ['SYSTEMDRIVE'] + '\\', "Users")
        for user in os.listdir(users_path):
            user_path = os.path.join(users_path, user)
            if os.path.isdir(user_path) and not user in self.default_users:
                user_directory.append(user_path)
        return user_directory if user_directory else self.logger.error("No user directories found.") and sys.exit()
    
    def populate(self):
        """
        Populate the user directories with random files
        between 5 and 15 files per directory containing
        1000 random characters each
        """
        for user_dir in self.user_directory:
            for dir in os.listdir(user_dir):
                if dir in self.folders:
                    self.logger.info(f"Populating directory: {os.path.join(user_dir, dir)}")
                    self.create_files(os.path.join(user_dir, dir))
        self.logger.info(f"Total files created: {self.file_count}")
        self.logger.info(f"Total subdirectories created: {self.subdir_count}")
        return

    def create_file(self, user_dir):
        """
        Create a random file with a random name, a random 
        extension from the list of extensions and random 
        content between 100 and 1000 characters
        """
        file_name = lorem.generate_name()
        file_path = os.path.join(user_dir, file_name + random.choice(self.extensions))
        with open(file_path, 'w') as file:
            file.write(lorem.generate_content())
            self.logger.info(f"File created: {file_path}")
            self.file_count += 1

    def create_subdirectory(self, user_dir):
        """
        Create a random subdirectory with a random name
        and return the path to the new directory created
        """
        subdir_name = lorem.generate_name()
        subdir_path = os.path.join(user_dir, subdir_name)
        os.makedirs(subdir_path)
        self.subdir_count += 1
        return subdir_path

    def create_files(self, user_dir):
        """
        Create random files in the user directory and 
        with a 25% chance create a random subdirectory 
        with files inside
        """
        for _ in range(0, random.randint(5, 15)):
            try:
                self.create_file(user_dir)
                if random.random() < 0.25:
                    subdir_path = self.create_subdirectory(user_dir)
                    for _ in range(0, random.randint(5, 15)):
                        self.create_file(subdir_path)
            except:
                logger.error("Error creating file.") # DEBUGGING ONLY
                continue

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "created_files.txt"))
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO , format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S') # for terminal only
    logger = setup_logger()

    lorem = LoremIpsum()
    populator = WindowsPopulator(logger)
    populator.populate()
    logger.info("Populating completed.")