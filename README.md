# Description
**[EN]** Windows Populator is a tool to generate realistic files and directories in user directories on Windows systems. Originally designed to prepare labs for testing ransomware-like behavior, it can be used in many situations such as backup testing, data recovery scenarios, or filesystem testing.

**[FR]** Windows Populator est un outil pour générer des fichiers et dossiers réalistes dans les répertoires des utilisateurs sous Windows. Conçu à l'origine pour préparer des labs à des tests de ransomware, il peut être utilisé dans diverses situations comme des tests de sauvegarde, des scénarios de récupération de données, ou des tests de systèmes de fichiers.

# Requirements
- Windows OS
- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

# Usage
1. Install Python 3.6 or higher, if not already installed.
2. Clone the Windows Populator repository.
3. Run the script : `python.exe windows_populator.py`
4. The tool will automatically generate random files and directories in the user directories under C:\Users\\\<user>.

**Note**: All created files are valid and can be opened in their respective applications (Word, Excel, PowerPoint, PDF readers, image viewers, etc.).

# Features
- **Realistic File Generation**: Creates valid, openable files with proper internal structure
- **Multiple File Types**: Supports .txt, .docx, .xlsx, .pptx, .pdf, .jpg, .jpeg, .png, .mp3, and .zip files
- **Proper File Headers**: Each file type includes correct headers and metadata:
  - **Text files (.txt)**: Formatted with title, date, author, and structured paragraphs
  - **Office documents**: Valid Office Open XML format for Word (.docx), Excel (.xlsx), and PowerPoint (.pptx)
  - **PDFs**: Proper PDF structure with catalog, pages, fonts, and formatted content
  - **Images**: Valid PNG and JPEG files with correct headers, chunk structure, and random colors
  - **Audio**: MP3 files with ID3v2 tags (including title metadata)
  - **Archives**: ZIP files containing multiple text documents
- **Random Content**: Uses Lorem Ipsum text generation for realistic-looking documents
- **Directory Structure**: Creates subdirectories with 25% probability for complex file trees
- **Logging**: Tracks all created files in CREATED_FILES.txt on the Desktop
- **Automatic User Detection**: Populates common folders (Desktop, Documents, Pictures, Music, Downloads, Videos) for all non-system/default users

# License
Windows Populator is released under the MIT License. See [LICENSE](LICENSE)
