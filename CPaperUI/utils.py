import os
import re
import requests
import json
import pandas as pd
import docx
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from config import parsers

def get_response(url, content, history, temperature, top_k, top_p):
    data = {
        'content': content,
        'history': history, 
        'temperature': temperature,
        'top_k': top_k,
        'top_p': top_p
    }
    response = requests.post(url + 'get_response', data=json.dumps(data))
    response.encoding = 'utf-8'
    return json.loads(response.text)

def get_stream_response(url, content, history, temperature, top_k, top_p):
    data = {
        'content': content,
        'history': history, 
        'temperature': temperature,
        'top_k': top_k,
        'top_p': top_p
    }
    response = requests.post(url + 'get_stream_response', json=data, stream=True)
    cur_size = 0
    for line in response.iter_lines():
        if line:
            item = line.decode('utf-8')
            pattern = re.compile(r'data: .*')
            match = pattern.search(item)
            if match:
                result = json.loads(match.group()[6:])
                yield result[cur_size:]
                cur_size = len(result)

def save_to_doc(content, path):
    doc = docx.Document()
    doc.styles['Normal'].font.name = u'宋体'
    doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    doc.styles['Normal'].font.size = Pt(14)
    doc.styles['Normal'].font.color.rgb = RGBColor(0, 0, 0)
    doc.add_paragraph(content)
    doc.save(path)

def save_to_csv(content, path):
    pd.DataFrame(dict([(k, pd.Series(v)) for k, v in content.items()])).to_csv(path, encoding='utf-8-sig')

def get_files(path, file_type):
    files_path = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(file_type) and not file_name.startswith('~$'):
                files_path.append(os.path.join(root, file_name))
    return files_path