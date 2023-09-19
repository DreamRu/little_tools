import os
import re
from opencc import OpenCC
import pyfiglet
import argparse

title = pyfiglet.figlet_format('DreamRu', font='larry3d')
print(f'\033[36m{title}\033[0m')
print('Powered by XiaoLing&GPT3.5,thanks!')

arguments = argparse.ArgumentParser()
arguments.add_argument("-i", dest="folder_path")  # 指定文件夹路径
args = arguments.parse_args()

folder_path = args.folder_path or os.getcwd()

# 遍历当前目录下的所有文件和文件夹
for filename in os.listdir(folder_path):
    # 判断文件是否是以 .ass 结尾且包含 'chseng' 或 'chs' 字样
    if filename.endswith(".ass"):
        file_path = os.path.join(folder_path, filename)

        def process_ass_file(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            updated_lines = []
            found_events = False

            for line in lines:
                if '分隔行' in line:
                    found_events = True
                if found_events and ',chs,' in line:
                    line = re.sub(r'\\N.*$', '', line)
                if found_events and ',chsHDR,' in line:
                    line = re.sub(r'\\N.*$', '', line)            
                if found_events and ',LRC,' in line:
                    line = re.sub(r'\\N.*$', '', line)
                if found_events and ',chs,' in line:
                    line = line.replace(',chs,', ',chs1,')
                if found_events and ',tip,' in line:
                    line = line.replace(',tip,', ',tip1,')
                if found_events and ',Yingzimu,' in line:
                    line = line.replace(',Yingzimu,', ',Yingzimu1,')  
                if found_events and ',chsHDR,' in line:
                    line = line.replace(',chsHDR,', ',1chsHDR,')         
                updated_lines.append(line)

            # 获取输入文件名并修改输出文件名
            input_filename = os.path.basename(file_path)
            output_filename = input_filename.replace('chseng', 'chs')
            output_file_path = os.path.join(folder_path, output_filename)

            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.writelines(updated_lines)

        process_ass_file(file_path)



# 遍历当前目录下的所有文件和文件夹
for filename in os.listdir(folder_path):
    # 判断文件是否是以 .ass 结尾
    if filename.endswith(".ass") and 'chs' in filename:
        cc = OpenCC('s2t')
        input_file_path = os.path.join(folder_path, filename)
        output_filename = filename.replace('chs', 'cht')
        output_file_path = os.path.join(folder_path, output_filename)

        start_converting = False

        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()

        converted_lines = []

        for line in lines:
            # 判断是否包含特定字符串，如果包含则不进行转换
            if any(substring in line for substring in ["\\fn方正少儿_GBK", "\\fn方正启体_GBK", '\\fn方正少儿繁体', '\\fn素材集市社会体', '\\fn方正苏新诗古印宋 简', '\\fn方正美黑_GBK', '\\fn方正美黑繁体', '\\fn方正宋黑_GBK', '\\fn方正宋黑繁体', '\\fn方正新舒体_GBK', '\\fn方正新舒体繁体']):
                # 替换
                line = line.replace('\\fn方正少儿_GBK', '\\fn方正少儿繁体').replace('\\fn方正美黑_GBK', '\\fn方正美黑繁体').replace("\\fn方正启体_GBK", "\\fn方正启体繁体").replace('\\fn方正宋黑_GBK', '\\fn方正宋黑繁体').replace('\\fn方正新舒体_GBK', '\\fn方正新舒体繁体')
                converted_lines.append(line)
                continue

            # 如果遇到[Events]行，将开始转换
            if "[Events]" in line:
                start_converting = True

            if start_converting:
                inside_brackets = False
                new_line = ''
                for char in line:
                    if char == '{':
                        inside_brackets = True
                        new_line += char
                    elif char == '}':
                        inside_brackets = False
                        new_line += char
                    elif not inside_brackets:
                        new_line += cc.convert(char)
                    else:
                        new_line += char

                line = new_line.replace('\\fn条幅黑体', '\\fn方正大黑_GBK')

            converted_lines.append(line)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.writelines(converted_lines)

    elif filename.endswith(".ass") and 'cht' in filename:
        cc = OpenCC('t2s')
        input_file_path = os.path.join(folder_path, filename)
        output_filename = filename.replace('cht', 'chs')
        output_file_path = os.path.join(folder_path, output_filename)

        start_converting = False

        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()

        converted_lines = []

        for line in lines:
            # 判断是否包含特定字符串，如果包含则不进行转换
            if any(substring in line for substring in ["\\fn方正少儿_GBK", "\\fn方正启体_GBK", '\\fn方正少儿繁体', '\\fn素材集市社会体', '\\fn方正苏新诗古印宋 简']):
                # 替换
                line = line.replace('\\fn方正少儿_GBK', '\\fn方正少儿繁体')
                converted_lines.append(line)
                continue

            # 如果遇到[Events]行，将开始转换
            if "[Events]" in line:
                start_converting = True

            if start_converting:
                inside_brackets = False
                new_line = ''
                for char in line:
                    if char == '{':
                        inside_brackets = True
                        new_line += char
                    elif char == '}':
                        inside_brackets = False
                        new_line += char
                    elif not inside_brackets:
                        new_line += cc.convert(char)
                    else:
                        new_line += char

                line = new_line

            converted_lines.append(line)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.writelines(converted_lines)
print("转换完成")
