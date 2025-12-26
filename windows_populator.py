__author__ = "R4z1xx"
__copyright__ = "Copyright (c) 2025 R4z1xx"
__license__ = "MIT"
__version__ = "2.0"

import logging
import random
import sys
import os
import zipfile
import struct
import zlib
from datetime import datetime

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
        Generate a random name using 1-2 words
        from the list of words in the class
        """
        return '_'.join(random.choices(self.words, k=random.randint(1, 2)))

    def generate_title(self):
        """
        Generate a random title (capitalized words)
        """
        words = random.choices(self.words, k=random.randint(2, 5))
        return ' '.join(word.capitalize() for word in words)

    def generate_sentence(self):
        """
        Generate a single random sentence
        """
        words = random.choices(self.words, k=random.randint(5, 15))
        return words[0].capitalize() + ' ' + ' '.join(words[1:]) + '.'

    def generate_paragraph(self):
        """
        Generate a random paragraph (3-6 sentences)
        """
        sentences = [self.generate_sentence() for _ in range(random.randint(3, 6))]
        return ' '.join(sentences)

    def generate_content(self, num_paragraphs=None):
        """
        Generate random content with multiple paragraphs
        """
        if num_paragraphs is None:
            num_paragraphs = random.randint(3, 8)
        paragraphs = [self.generate_paragraph() for _ in range(num_paragraphs)]
        return '\n\n'.join(paragraphs)

class FileGenerator:
    """
    Generate files with proper headers and content based on file type
    Supported types: txt, docx, xlsx, pptx, pdf, png, jpg, mp3

    Functions:
    - create_txt_file(file_path)
    - create_docx_file(file_path)
    - create_xlsx_file(file_path)
    - create_pptx_file(file_path)
    - create_pdf_file(file_path)
    - create_png_file(file_path)
    - create_jpg_file(file_path)
    - create_mp3_file(file_path)
    """
    def __init__(self, lorem):
        self.lorem = lorem
    
    def create_txt_file(self, file_path):
        """
        Create a txt file
        """
        title = self.lorem.generate_title()
        content = self.lorem.generate_content()
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        text_content = f"""{title}
            {'=' * len(title)}

            Created: {date_str}
            Author: Generated Document

            {content}

            ---
            End of document
            """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
    
    def create_docx_file(self, file_path):
        """
        Create a valid .docx
        """
        title = self.lorem.generate_title()
        content = self.lorem.generate_content()
        
        document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
                <w:body>
                    <w:p>
                        <w:pPr><w:pStyle w:val="Title"/></w:pPr>
                        <w:r><w:t>{title}</w:t></w:r>
                    </w:p>
                    <w:p>
                        <w:r><w:t>{content}</w:t></w:r>
                    </w:p>
                </w:body>
            </w:document>'''

        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
                <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
                <Default Extension="xml" ContentType="application/xml"/>
                <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
            </Types>'''

        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
            </Relationships>'''

        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as docx:
            docx.writestr('[Content_Types].xml', content_types)
            docx.writestr('_rels/.rels', rels)
            docx.writestr('word/document.xml', document_xml)
    
    def create_xlsx_file(self, file_path):
        """
        Create a valid .xlsx
        """
        headers = [self.lorem.generate_name().capitalize() for _ in range(5)]
        rows_data = [[self.lorem.generate_name() for _ in range(5)] for _ in range(10)]
        
        all_strings = headers + [cell for row in rows_data for cell in row]
        shared_strings_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        shared_strings_xml += f'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(all_strings)}" uniqueCount="{len(all_strings)}">'
        for s in all_strings:
            shared_strings_xml += f'<si><t>{s}</t></si>'
        shared_strings_xml += '</sst>'
        
        sheet_data = ''
        for col_idx, _ in enumerate(headers):
            col_letter = chr(65 + col_idx)
            sheet_data += f'<c r="{col_letter}1" t="s"><v>{col_idx}</v></c>'
        
        string_idx = len(headers)
        for row_idx, row in enumerate(rows_data, start=2):
            for col_idx, _ in enumerate(row):
                col_letter = chr(65 + col_idx)
                sheet_data += f'<c r="{col_letter}{row_idx}" t="s"><v>{string_idx}</v></c>'
                string_idx += 1
        
        sheet_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
                <sheetData>
                    <row r="1">{sheet_data[:sheet_data.find('</c>') * len(headers) + len('</c>') * len(headers)]}</row>
                </sheetData>
            </worksheet>'''
        
        sheet_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
                <sheetData>'''
        
        sheet_xml += '<row r="1">'
        for col_idx in range(len(headers)):
            col_letter = chr(65 + col_idx)
            sheet_xml += f'<c r="{col_letter}1" t="s"><v>{col_idx}</v></c>'
        sheet_xml += '</row>'
        
        string_idx = len(headers)
        for row_idx in range(2, len(rows_data) + 2):
            sheet_xml += f'<row r="{row_idx}">'
            for col_idx in range(5):
                col_letter = chr(65 + col_idx)
                sheet_xml += f'<c r="{col_letter}{row_idx}" t="s"><v>{string_idx}</v></c>'
                string_idx += 1
            sheet_xml += '</row>'
        
        sheet_xml += '</sheetData></worksheet>'
        
        workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
                <sheets>
                    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
                </sheets>
            </workbook>'''

        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
                <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
                <Default Extension="xml" ContentType="application/xml"/>
                <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
                <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
                <Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
            </Types>'''

        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
            </Relationships>'''

        workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
                <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
            </Relationships>'''

        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as xlsx:
            xlsx.writestr('[Content_Types].xml', content_types)
            xlsx.writestr('_rels/.rels', rels)
            xlsx.writestr('xl/workbook.xml', workbook_xml)
            xlsx.writestr('xl/_rels/workbook.xml.rels', workbook_rels)
            xlsx.writestr('xl/worksheets/sheet1.xml', sheet_xml)
            xlsx.writestr('xl/sharedStrings.xml', shared_strings_xml)
    
    def create_pptx_file(self, file_path):
        """
        Create a valid .pptx
        """
        title = self.lorem.generate_title()
        subtitle = self.lorem.generate_sentence()
        
        slide_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
                <p:cSld>
                    <p:spTree>
                        <p:nvGrpSpPr>
                            <p:cNvPr id="1" name=""/>
                            <p:cNvGrpSpPr/>
                            <p:nvPr/>
                        </p:nvGrpSpPr>
                        <p:grpSpPr/>
                        <p:sp>
                            <p:nvSpPr>
                                <p:cNvPr id="2" name="Title"/>
                                <p:cNvSpPr/>
                                <p:nvPr/>
                            </p:nvSpPr>
                            <p:spPr>
                                <a:xfrm>
                                    <a:off x="457200" y="274638"/>
                                    <a:ext cx="8229600" cy="1143000"/>
                                </a:xfrm>
                                <a:prstGeom prst="rect"/>
                            </p:spPr>
                            <p:txBody>
                                <a:bodyPr/>
                                <a:p>
                                    <a:r>
                                        <a:rPr lang="en-US" sz="4400" b="1"/>
                                        <a:t>{title}</a:t>
                                    </a:r>
                                </a:p>
                            </p:txBody>
                        </p:sp>
                        <p:sp>
                            <p:nvSpPr>
                                <p:cNvPr id="3" name="Subtitle"/>
                                <p:cNvSpPr/>
                                <p:nvPr/>
                            </p:nvSpPr>
                            <p:spPr>
                                <a:xfrm>
                                    <a:off x="457200" y="1600200"/>
                                    <a:ext cx="8229600" cy="800000"/>
                                </a:xfrm>
                                <a:prstGeom prst="rect"/>
                            </p:spPr>
                            <p:txBody>
                                <a:bodyPr/>
                                <a:p>
                                    <a:r>
                                        <a:rPr lang="en-US" sz="2000"/>
                                        <a:t>{subtitle}</a:t>
                                    </a:r>
                                </a:p>
                            </p:txBody>
                        </p:sp>
                    </p:spTree>
                </p:cSld>
            </p:sld>'''

        presentation_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
                <p:sldIdLst>
                    <p:sldId id="256" r:id="rId2"/>
                </p:sldIdLst>
                <p:sldSz cx="9144000" cy="6858000" type="screen4x3"/>
            </p:presentation>'''

        content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
                <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
                <Default Extension="xml" ContentType="application/xml"/>
                <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
                <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
            </Types>'''

        rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
            </Relationships>'''

        presentation_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
                <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
            </Relationships>'''

        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as pptx:
            pptx.writestr('[Content_Types].xml', content_types)
            pptx.writestr('_rels/.rels', rels)
            pptx.writestr('ppt/presentation.xml', presentation_xml)
            pptx.writestr('ppt/_rels/presentation.xml.rels', presentation_rels)
            pptx.writestr('ppt/slides/slide1.xml', slide_xml)
    
    def create_pdf_file(self, file_path):
        """
        Create a valid PDF
        """
        title = self.lorem.generate_title()
        content = self.lorem.generate_content(num_paragraphs=3)
        
        pdf_content = b'%PDF-1.4\n'
        pdf_content += b'%\xe2\xe3\xcf\xd3\n'
        
        obj1_offset = len(pdf_content)
        pdf_content += b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'
        
        obj2_offset = len(pdf_content)
        pdf_content += b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n'
        
        obj3_offset = len(pdf_content)
        pdf_content += b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n'
        
        text_content = f'BT\n/F1 24 Tf\n50 750 Td\n({title}) Tj\n'
        text_content += '/F1 12 Tf\n0 -40 Td\n'
        
        words = content.split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 70:
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        for line in lines[:30]:
            safe_line = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
            text_content += f'0 -16 Td\n({safe_line}) Tj\n'
        
        text_content += 'ET'
        text_bytes = text_content.encode('latin-1')
        
        obj4_offset = len(pdf_content)
        pdf_content += f'4 0 obj\n<< /Length {len(text_bytes)} >>\nstream\n'.encode('latin-1')
        pdf_content += text_bytes
        pdf_content += b'\nendstream\nendobj\n'
        
        obj5_offset = len(pdf_content)
        pdf_content += b'5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n'
        
        xref_offset = len(pdf_content)
        pdf_content += b'xref\n0 6\n'
        pdf_content += b'0000000000 65535 f \n'
        pdf_content += f'{obj1_offset:010d} 00000 n \n'.encode()
        pdf_content += f'{obj2_offset:010d} 00000 n \n'.encode()
        pdf_content += f'{obj3_offset:010d} 00000 n \n'.encode()
        pdf_content += f'{obj4_offset:010d} 00000 n \n'.encode()
        pdf_content += f'{obj5_offset:010d} 00000 n \n'.encode()
        
        pdf_content += b'trailer\n<< /Size 6 /Root 1 0 R >>\n'
        pdf_content += f'startxref\n{xref_offset}\n'.encode()
        pdf_content += b'%%EOF'
        
        with open(file_path, 'wb') as f:
            f.write(pdf_content)
    
    def create_png_file(self, file_path):
        """
        Create a valid PNG
        """
        width, height = random.randint(100, 400), random.randint(100, 400)
        
        r, g, b = random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)
        
        png_signature = b'\x89PNG\r\n\x1a\n'
        
        ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
        ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
        ihdr_chunk = struct.pack('>I', 13) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)
        
        raw_data = b''
        for _ in range(height):
            raw_data += b'\x00'
            for _ in range(width):
                raw_data += bytes([r, g, b])
        
        compressed_data = zlib.compress(raw_data, 9)
        idat_crc = zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff
        idat_chunk = struct.pack('>I', len(compressed_data)) + b'IDAT' + compressed_data + struct.pack('>I', idat_crc)
        
        iend_crc = zlib.crc32(b'IEND') & 0xffffffff
        iend_chunk = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', iend_crc)
        
        with open(file_path, 'wb') as f:
            f.write(png_signature + ihdr_chunk + idat_chunk + iend_chunk)
    
    def create_jpg_file(self, file_path):
        """
        Create a valid JPEG
        """
        width, height = random.randint(100, 400), random.randint(100, 400)
        
        jpeg_data = bytearray([
            0xFF, 0xD8,  # SOI
            0xFF, 0xE0,  # APP0
            0x00, 0x10,  # Length
            0x4A, 0x46, 0x49, 0x46, 0x00,  # JFIF\0
            0x01, 0x01,  # Version
            0x00,  # Units
            0x00, 0x01, 0x00, 0x01,  # Density
            0x00, 0x00,  # Thumbnail
            0xFF, 0xDB,  # DQT
            0x00, 0x43,  # Length
            0x00,  # Table ID
        ])
        
        # Quantization table
        qt = [16, 11, 10, 16, 24, 40, 51, 61, 12, 12, 14, 19, 26, 58, 60, 55,
              14, 13, 16, 24, 40, 57, 69, 56, 14, 17, 22, 29, 51, 87, 80, 62,
              18, 22, 37, 56, 68, 109, 103, 77, 24, 35, 55, 64, 81, 104, 113, 92,
              49, 64, 78, 87, 103, 121, 120, 101, 72, 92, 95, 98, 112, 100, 103, 99]
        jpeg_data.extend(qt)
        
        # SOF0
        jpeg_data.extend([0xFF, 0xC0, 0x00, 0x0B, 0x08])
        jpeg_data.extend([(height >> 8) & 0xFF, height & 0xFF])
        jpeg_data.extend([(width >> 8) & 0xFF, width & 0xFF])
        jpeg_data.extend([0x01, 0x01, 0x11, 0x00])
        
        # DHT (DC)
        jpeg_data.extend([0xFF, 0xC4, 0x00, 0x1F, 0x00])
        jpeg_data.extend([0x00, 0x01, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        jpeg_data.extend([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B])
        
        # DHT (AC)
        jpeg_data.extend([0xFF, 0xC4, 0x00, 0xB5, 0x10])
        jpeg_data.extend([0x00, 0x02, 0x01, 0x03, 0x03, 0x02, 0x04, 0x03, 0x05, 0x05, 0x04, 0x04, 0x00, 0x00, 0x01, 0x7D])
        jpeg_data.extend([0x01, 0x02, 0x03, 0x00, 0x04, 0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07])
        jpeg_data.extend([0x22, 0x71, 0x14, 0x32, 0x81, 0x91, 0xA1, 0x08, 0x23, 0x42, 0xB1, 0xC1, 0x15, 0x52, 0xD1, 0xF0])
        jpeg_data.extend([0x24, 0x33, 0x62, 0x72, 0x82, 0x09, 0x0A, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x25, 0x26, 0x27, 0x28])
        jpeg_data.extend([0x29, 0x2A, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49])
        jpeg_data.extend([0x4A, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69])
        jpeg_data.extend([0x6A, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89])
        jpeg_data.extend([0x8A, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7])
        jpeg_data.extend([0xA8, 0xA9, 0xAA, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xC2, 0xC3, 0xC4, 0xC5])
        jpeg_data.extend([0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xE1, 0xE2])
        jpeg_data.extend([0xE3, 0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8])
        jpeg_data.extend([0xF9, 0xFA])
        
        # SOS
        jpeg_data.extend([0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01, 0x00, 0x00, 0x3F, 0x00])
        
        # Data
        gray_value = random.randint(64, 192)
        jpeg_data.extend([gray_value, 0x00])
        
        # EOI
        jpeg_data.extend([0xFF, 0xD9])
        
        with open(file_path, 'wb') as f:
            f.write(bytes(jpeg_data))
    
    def create_mp3_file(self, file_path):
        """
        Create a silent MP3 file
        """
        mp3_data = bytearray([
            0x49, 0x44, 0x33,  # ID3
            0x04, 0x00,  # 2.4.0
            0x00,  # Flags
            0x00, 0x00, 0x00, 0x00,
        ])
        
        title = self.lorem.generate_title()
        title_bytes = title.encode('utf-8')
        
        mp3_data.extend([0x54, 0x49, 0x54, 0x32])  # TIT2
        frame_size = len(title_bytes) + 1
        mp3_data.extend([0x00, 0x00, (frame_size >> 8) & 0x7F, frame_size & 0x7F])
        mp3_data.extend([0x00, 0x00])  # Flags
        mp3_data.extend([0x03])  # UTF-8
        mp3_data.extend(title_bytes)
        
        # ID3 size
        id3_size = len(mp3_data) - 10
        mp3_data[6] = (id3_size >> 21) & 0x7F
        mp3_data[7] = (id3_size >> 14) & 0x7F
        mp3_data[8] = (id3_size >> 7) & 0x7F
        mp3_data[9] = id3_size & 0x7F
        
        # Silent MP3 frames (~1 second)
        for _ in range(50):
            mp3_data.extend([0xFF, 0xFB, 0x90, 0x00])
            mp3_data.extend([0x00] * 413)
        
        with open(file_path, 'wb') as f:
            f.write(bytes(mp3_data))
    
    def create_zip_file(self, file_path):
        """
        Create a valid ZIP archive with text files in it
        """
        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for i in range(random.randint(2, 5)):
                filename = f"{self.lorem.generate_name()}.txt"
                content = self.lorem.generate_content(num_paragraphs=2)
                zf.writestr(filename, content)
    
    def create_file(self, file_path, extension):
        """
        Create a file based on extension
        """
        extension = extension.lower()
        
        creators = {
            '.txt': self.create_txt_file,
            '.docx': self.create_docx_file,
            '.xlsx': self.create_xlsx_file,
            '.pptx': self.create_pptx_file,
            '.pdf': self.create_pdf_file,
            '.jpg': self.create_jpg_file,
            '.jpeg': self.create_jpg_file,
            '.png': self.create_png_file,
            '.mp3': self.create_mp3_file,
            '.zip': self.create_zip_file,
        }
        
        creator = creators.get(extension)
        if creator:
            creator(file_path)
            return True
        return False


class WindowsPopulator:
    def __init__(self, lorem, file_generator):
        self.default_users = ['Administrator', 'Public', 'Default', 'All Users', 'defaultuser0', 'Default User']
        self.folders = ['Desktop', 'Documents', 'Pictures', 'Music', 'Downloads', 'Videos']
        self.extensions = ['.txt', '.docx', '.xlsx', '.pptx', '.pdf', '.jpg', '.jpeg', '.png', '.mp3', '.zip']
        self.user_directory = self.get_user_directory()
        self.file_count = 0
        self.subdir_count = 0
        self.lorem = lorem
        self.file_generator = file_generator
    
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
        return user_directory if user_directory else logger.error("No user directories found.") and sys.exit()
    
    def populate(self):
        """
        Populate the user directories with random files
        between 5 and 15 files per directory containing
        1000 random characters each
        """
        for user_dir in self.user_directory:
            for dir in os.listdir(user_dir):
                if dir in self.folders:
                    logger.info(f"Populating directory: {os.path.join(user_dir, dir)}")
                    self.create_files(os.path.join(user_dir, dir))
        logger.info(f"Total files created: {self.file_count}")
        logger.info(f"Total subdirectories created: {self.subdir_count}")
        return

    def create_file(self, user_dir):
        """
        Create a random file with a random name, a random 
        extension from the list of extensions and content 
        based on the file type
        """
        file_name = self.lorem.generate_name()
        extension = random.choice(self.extensions)
        file_path = os.path.join(user_dir, file_name + extension)
        
        try:
            self.file_generator.create_file(file_path, extension)
            logger.info(f"File created: {file_path}")
            self.file_count += 1
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {e}")

    def create_subdirectory(self, user_dir):
        """
        Create a random subdirectory with a random name
        and return the path to the new directory created
        """
        subdir_name = self.lorem.generate_name()
        subdir_path = os.path.join(user_dir, subdir_name)
        os.makedirs(subdir_path, exist_ok=True)
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
            except Exception as e:
                logger.error(f"Error creating file: {e}")
                continue

def setup_logger(directory):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(str(os.path.join(os.path.join(directory, "Desktop"), "CREATED_FILES.txt")))
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    lorem = LoremIpsum()
    file_generator = FileGenerator(lorem)
    populator = WindowsPopulator(lorem, file_generator)
    logger = setup_logger(populator.user_directory[0])

    populator.populate()
    logger.info("Populating completed.")