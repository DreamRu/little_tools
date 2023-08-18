import argparse
import os
import shutil
import subprocess
import pyfiglet
import re

title = pyfiglet.figlet_format('DreamRu', font='larry3d')
print(f'\033[36m{title}\033[0m')
print('Powered by XiaoLing&GPT3.5')

# 参数
arguments = argparse.ArgumentParser()
arguments.add_argument("-i", dest="folder_path")  # 指定文件夹路径
arguments.add_argument("-o", dest="output_path")  # 指定输出路径
arguments.add_argument("-m", dest="mode")  # 指定模式
arguments.add_argument("-f", dest="fps")  # 输出帧率
args = arguments.parse_args()

ffmpeg_path = shutil.which("ffmpeg")
if ffmpeg_path is None:
    script_folder = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(script_folder, "ffmpeg")  # ffmpeg路径

dovi_tool_path = shutil.which("dovi_tool")
if dovi_tool_path is None:
    script_folder = os.path.dirname(os.path.abspath(__file__))
    dovi_tool_path = os.path.join(script_folder, "dovi_tool")  # dvtool路径

mkvmerge_path = shutil.which("mkvmerge")
if mkvmerge_path is None:
    script_folder = os.path.dirname(os.path.abspath(__file__))
    mkvmerge_path = os.path.join(script_folder, "mkvmerge")  # mkvmerge路径

hdr10plus_tool_path = shutil.which("hdr10plus_tool")
if hdr10plus_tool_path is None:
    script_folder = os.path.dirname(os.path.abspath(__file__))
    hdr10plus_tool_path = os.path.join(script_folder, "hdr10plus_tool")  # hdr10plus_tool路径

folder_path = args.folder_path or os.getcwd()  # 未填写输入文件夹则为当前文件夹

# 未填写输出路径则为当前路径下的hdr10plus或dvhdr文件夹
if args.output_path:
    output_path = args.output_path
elif args.mode == "hdr10plus":
    hdr10plus_folder_path = os.path.join(folder_path, "hdr10plus")
    if not os.path.exists(hdr10plus_folder_path):
        os.makedirs(hdr10plus_folder_path)
    output_path = hdr10plus_folder_path
elif args.mode == "dvhdr":
    dvhdr_folder_path = os.path.join(folder_path, "dvhdr")
    if not os.path.exists(dvhdr_folder_path):
        os.makedirs(dvhdr_folder_path)
    output_path = dvhdr_folder_path
else:
    output_path = folder_path
mode = args.mode
fps = args.fps or "24000/1001p"  # 未填写默认为23.976

if mode == "hdr10plus":
    if files := [
        os.path.join(folder_path, file_name)
        for file_name in os.listdir(folder_path)
        if (
                   "hdr10plus" in file_name.lower()
                   or "hdr10+" in file_name.lower()
                   or "HDR10+" in file_name.lower()
           )
           and (file_name.endswith('.mp4') or file_name.endswith('.mkv'))
    ]:
        for file in files:
            subprocess.run([
                ffmpeg_path,
                "-hide_banner",
                "-loglevel",
                "fatal",
                "-y",
                "-i",
                file,
                "-an",
                "-c:v",
                "copy",
                "-f",
                "hevc",
                f"{output_path}/hdr10plus.hevc"
            ])
            subprocess.run([
                hdr10plus_tool_path,
                '--skip-validation',
                "extract",
                f"{output_path}/hdr10plus.hevc",
                "-o",
                f"{output_path}/metadata.json"
            ])
            subprocess.run([
                dovi_tool_path,
                "generate",
                "-j",
                'd:/dvhdr/default.json',
                "--hdr10plus-json",
                f"{output_path}/metadata.json",
                "-o",
                f"{output_path}/RPU_hdr10plus.bin"
            ])
            subprocess.run([
                dovi_tool_path,
                'inject-rpu',
                '-i',
                f'{output_path}/hdr10plus.hevc',
                '--rpu-in',
                f"{output_path}/RPU_hdr10plus.bin",
                '-o',
                f'{output_path}/output.hevc'
            ])
            file_name = os.path.splitext(os.path.basename(file))[0]
            output_name = file_name.replace("hdr10+", "DV.HDR10+").replace("HDR10+", "DV.HDR10+")
            match = re.search(r'-(?!.*-)([^.]+)$', file_name)

            if match:
                output_name = output_name.replace(match.group(1), "DreamRu")
            else:
                output_name = output_name + "-DreamRu"
            output_file = os.path.join(output_path, output_name)
            subprocess.run([
                mkvmerge_path,
                '--quiet',
                '--output',
                f"{output_file}.mkv",
                "--default-duration",
                f"0:{fps}",
                f'{output_path}/output.hevc',
                "--no-video",
                file
            ])
            os.remove(f'{output_path}/output.hevc')
            os.remove(f"{output_path}/RPU_hdr10plus.bin")
            os.remove(f"{output_path}/metadata.json")
            os.remove(f"{output_path}/hdr10plus.hevc")
            if os.path.exists(f'{output_file}.mkv'):
                print(f'\033[35m已输出{output_name}.mkv\033[0m')
            else:
                print(f'\033[31m输出{output_name}.mkv失败\033[0m')

    else:
        print("\033[31m未找到目录下名称包含hdr10plus名称的视频文件\033[0m")


def classification(_file_list: list) -> dict:
    _files = {}
    _file_list.sort()
    for name in _file_list:
        s = name.lower().split('.')

        keyword = ['dv', 'hdr', 'hdr10', 'hdr10+']
        dv_or_hdr_index = next((s.index(ii) for ii in keyword if ii in s), None)

        if dv_or_hdr_index is None: continue
        file_name = '.'.join(s[:dv_or_hdr_index])
        cl = s[dv_or_hdr_index].replace('10+', '').replace('10', '')
        if _files.get(file_name):
            _files[file_name][cl] = name
        else:
            _files[file_name] = {cl: name}

    for key, value in list(_files.items()):
        if len(value) == 1:
            del _files[key]
    return _files


if args.mode == "dvhdr":
    file_list = os.listdir(folder_path)
    dvhdr = classification(file_list)
    for file in dvhdr.values():
        dv = file['dv']
        hdr = file['hdr']
        print('\033[35m转换DV视频为hevc\033[0m')
        subprocess.run([
            ffmpeg_path,
            "-hide_banner",
            "-loglevel",
            "fatal",
            "-y",
            "-i",
            f'{folder_path}/{dv}',
            "-an",
            "-c:v",
            "copy",
            "-f",
            "hevc",
            f"{output_path}/dv.hevc"
        ])
        print('\033[35m提取DV视频中RPU层\033[0m')
        subprocess.run([dovi_tool_path, "-m", "3", "extract-rpu", f"{output_path}/dv.hevc", "-o",
                        f"{output_path}/RPU.bin"])
        print('\033[35m转换HDR视频为hevc\033[0m')
        subprocess.run([
            ffmpeg_path,
            "-hide_banner",
            "-loglevel",
            "fatal",
            "-y",
            "-i",
            f'{folder_path}/{hdr}',
            "-an",
            "-c:v",
            "copy",
            "-f",
            "hevc",
            f"{output_path}/hdr.hevc"
        ])
        print('\033[35m为HDR视频注入RPU层\033[0m')
        subprocess.run([
            dovi_tool_path,
            "inject-rpu",
            "-i",
            f"{output_path}/hdr.hevc",
            "--rpu-in",
            f"{output_path}/RPU.bin",
            "-o",
            f"{output_path}/dvhdr.hevc"
        ])
        file_name = os.path.splitext(dv)[0]
        output_name = file_name.replace("DV", "DV.HDR").replace("dv", "DV.HDR")
        match = re.search(r'-(?!.*-)([^.]+)$', file_name)

        if match:
            output_name = output_name.replace(match.group(1), "DreamRu")
        else:
            output_name = output_name + "-DreamRu"
        output_file = os.path.join(output_path, output_name)
        print('\033[35m输出DVHDR视频\033[0m')
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            '--output',
            f"{output_file}.mkv",
            "--default-duration",
            f"0:{fps}",
            f'{output_path}/dvhdr.hevc',
            "--no-video",
            f'{folder_path}/{hdr}'
        ])
        os.remove(f'{output_path}/dv.hevc')
        os.remove(f'{output_path}/dvhdr.hevc')
        os.remove(f'{output_path}/hdr.hevc')
        os.remove(f"{output_path}/RPU.bin")
        if os.path.exists(f"{output_file}.mkv"):
            print(f'\033[35m已输出{output_name}.mkv\033[0m')
        else:
            print(f'\033[31m输出{output_name}.mkv失败\033[0m')
