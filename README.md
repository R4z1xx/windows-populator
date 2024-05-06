# Description
**[EN]** Windows Populator is a simple tool I've written to generate random files and directories in user directories on Windows systems. This tool was originally designed to prepare my labs for testing ransomware-like behavior, but it can be used in many other situations, such as backup testing for example.

**[FR]** Windows Populator est un outil que j'ai écrit pour générer des fichiers et dossiers aléatoirement dans les répertoires des utilisateurs sous Windows. J'ai conçu cet outil à l'origine pour préparer des labs à des tests de ransomware, mais il peut être utilisé dans d'autres situations, comme des tests de sauvegarde par exemple.

# Requirements
- Windows OS
- Python 3.6 >= (If using the Python version)

# Usage
#### Using the executable :
1. Download the latest release from the [releases](https://github.com/releases) page.
2. Extract the contents of the downloaded archive.
3. Run the exe file : `windows_populator.exe`
4. The tool will automatically generate random files and directories in the user directories under C:\Users\\\<user>.

#### Using the Python script :
1. Install Python 3.6 or superior, if not already installed.
2. Clone the Windows Populator repository.
3. Run the script : `python3 windows_populator.py`
4. The tool will automatically generate random files and directories in the user directories under C:\Users\\\<user>.

# License
Windows Populator is released under the MIT License. See [LICENSE](LICENSE)
