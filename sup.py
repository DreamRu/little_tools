from distutils.file_util import move_file
from doctest import OutputChecker
import os
import re
import argparse
import subprocess
import pyfiglet
import shutil

title = pyfiglet.figlet_format('DreamRu', font='larry3d')
print(f'\033[36m{title}\033[0m')
print('Powered by XiaoLing&GPT3.5')

# 参数
arguments = argparse.ArgumentParser()
arguments.add_argument("-i", dest="folder_path")  # 指定文件夹路径
arguments.add_argument("-o", dest="output_path")  # 指定输出路径
arguments.add_argument("-m", dest="mode")  # 指定模式
arguments.add_argument("-n", dest="search_name")  # 指定文件名
arguments.add_argument("-t", dest="tittle")  # 指定标题
args = arguments.parse_args()

mkvmerge_path = shutil.which("mkvmerge")
if mkvmerge_path is None:
    script_folder = os.path.dirname(os.path.abspath(__file__))
    mkvmerge_path = os.path.join(script_folder, "mkvmerge")  # mkvmerge路径

folder_path = args.folder_path or os.getcwd()
search_name = args.search_name
output_path = args.output_path
mode = args.mode
title = args.tittle

video_extensions = [".mkv"]
subtitle_extensions = [".sup"]

subtitle_categories = {
    "sdr.chseng": [],
    "sdr.chteng": [],
    "sdr.chs": [],
    "sdr.cht": [],
    "hdr.chseng": [],
    "hdr.chteng": [],
    "hdr.chs": [],
    "hdr.cht": []  
}

file_groups = {}
files = os.listdir(folder_path)
file_type=None
for file in files:
    if search_name in file:
        if mode == "movie":
           episode_match = re.search(search_name,file)
        else:
           episode_match = re.search(r"S\d+E\d+", file)
        if episode_match:
            episode_number = episode_match.group()
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in video_extensions:
                video_file = file  # 保存完整文件名（带路径）
                video_name = os.path.splitext(os.path.basename(file))[0]  # 提取文件名（不带路径）
                file_type = "video"
            elif file_extension in subtitle_extensions:
                file_type = "subtitle"
                for category in subtitle_categories:
                    if category in file:
                        subtitle_category = category
                        break

            if episode_number not in file_groups:
                file_groups[episode_number] = {}

            if file_type == "video":
                file_groups[episode_number]["video"] = {
                    "path": os.path.join(folder_path, video_file),
                    "name": video_name
                }
            elif file_type == "subtitle":
                if subtitle_category not in file_groups[episode_number]:
                    file_groups[episode_number][subtitle_category] = []
                file_groups[episode_number][subtitle_category].append(os.path.join(folder_path, file))



for episode, categories in file_groups.items():
  if title == "tx":
      # sdr*4 hdr*4
      if "sdr.chseng" in categories and "sdr.chteng" in categories and "video"  in categories and "hdr.chseng" in categories and "hdr.chteng" in categories and "hdr.cht" in categories and "hdr.chs" in categories and "sdr.cht" in categories and "sdr.chs" in categories:
        sdr_chseng_files = " ".join(categories["sdr.chseng"])
        sdr_chteng_files = " ".join(categories["sdr.chteng"])
        hdr_chseng_files = " ".join(categories["hdr.chseng"])
        hdr_chteng_files = " ".join(categories["hdr.chteng"])
        sdr_chs_files = " ".join(categories["sdr.chs"])
        sdr_cht_files = " ".join(categories["sdr.cht"])
        hdr_chs_files = " ".join(categories["hdr.chs"])
        hdr_cht_files = " ".join(categories["hdr.cht"]) 
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:SDR简英特效",
            "--language",
            "0:zh-Hans",
            sdr_chseng_files,
            "--track-name",
            "0:SDR繁英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_chteng_files,
            "--track-name",
            "0:SDR简体特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hans",
            sdr_chs_files,            
            "--track-name",
            "0:SDR繁體特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_cht_files,
            "--track-name",
            "0:HDR简英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chseng_files,
            "--track-name",
            "0:HDR繁英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_chteng_files,           
            "--track-name",
            "0:HDR简体特效",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chs_files,         
            "--track-name",
            "0:HDR繁體特效",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_cht_files

        ])
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*2 hdr*2 双语
      elif "sdr.chseng" in categories and "sdr.chteng" in categories and "video"  in categories and "hdr.chseng" in categories and "hdr.chteng" in categories:
        sdr_chseng_files = " ".join(categories["sdr.chseng"])
        sdr_chteng_files = " ".join(categories["sdr.chteng"])
        hdr_chseng_files = " ".join(categories["hdr.chseng"])
        hdr_chteng_files = " ".join(categories["hdr.chteng"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:SDR简英特效",
            "--language",
            "0:zh-Hans",
            sdr_chseng_files,
            "--track-name",
            "0:SDR繁英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_chteng_files,
            "--track-name",
            "0:HDR简英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chseng_files,
            "--track-name",
            "0:HDR繁英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_chteng_files,           
            "--track-order",
            "1:0,2:0",
            "--default-track-flag",
            "1:yes"
        ])
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*2 hdr*2 单语
      elif "sdr.chs" in categories and "sdr.cht" in categories and "video"  in categories and "hdr.chs" in categories and "hdr.cht" in categories:
        sdr_chs_files = " ".join(categories["sdr.chs"])
        sdr_cht_files = " ".join(categories["sdr.cht"])
        hdr_chs_files = " ".join(categories["hdr.chs"])
        hdr_cht_files = " ".join(categories["hdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:SDR简体特效",
            "--language",
            "0:zh-Hans",
            sdr_chs_files,
            "--track-name",
            "0:SDR繁體特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_cht_files,
            "--track-name",
            "0:HDR简体特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chs_files,
            "--track-name",
            "0:HDR繁體特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_cht_files,           
            "--track-order",
            "1:0,2:0",
            "--default-track-flag",
            "1:yes"
        ])
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*4 双语
      elif "sdr.chseng" in categories and "sdr.chteng" in categories and "video"  in categories and "sdr.chs" in categories and "sdr.cht" in categories:
        sdr_chseng_files = " ".join(categories["sdr.chseng"])
        sdr_chteng_files = " ".join(categories["sdr.chteng"])
        sdr_chs_files = " ".join(categories["sdr.chs"])
        sdr_cht_files = " ".join(categories["sdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简英特效",
            "--language",
            "0:zh-Hans",
            sdr_chseng_files,
            "--track-name",
            "0:繁英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_chteng_files,
            "--track-name",
            "0:简体特效",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hans",
            sdr_chs_files,         
            "--track-name",
            "0:繁體特效",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_cht_files
        ])
        
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*2 双语
      elif "sdr.chseng" in categories and "sdr.chteng" in categories and "video"  in categories:
        sdr_chseng_files = " ".join(categories["sdr.chseng"])
        sdr_chteng_files = " ".join(categories["sdr.chteng"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简英特效",
            "--language",
            "0:zh-Hans",
            sdr_chseng_files,
            "--track-name",
            "0:繁英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_chteng_files
        ])        

        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*2 单语
      elif "sdr.chs" in categories and "sdr.cht" in categories and "video"  in categories:
        sdr_chs_files = " ".join(categories["sdr.chs"])
        sdr_cht_files = " ".join(categories["sdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简体特效",
            "--language",
            "0:zh-Hans",
            sdr_chs_files,
            "--track-name",
            "0:繁體特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_cht_files
        ])        

        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')

      # hdr*4 双语
      elif "hdr.chseng" in categories and "hdr.chteng" in categories and "video"  in categories and "hdr.chs" in categories and "hdr.cht" in categories:
        hdr_chseng_files = " ".join(categories["hdr.chseng"])
        hdr_chteng_files = " ".join(categories["hdr.chteng"])
        hdr_chs_files = " ".join(categories["hdr.chs"])
        hdr_cht_files = " ".join(categories["hdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简英特效",
            "--language",
            "0:zh-Hans",
            hdr_chseng_files,
            "--track-name",
            "0:繁英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_chteng_files,
            "--track-name",
            "0:简体特效",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chs_files,         
            "--track-name",
            "0:繁體特效",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_cht_files
        ])
        
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # hdr*2 双语
      elif "hdr.chseng" in categories and "hdr.chteng" in categories and "video"  in categories:
        hdr_chseng_files = " ".join(categories["hdr.chseng"])
        hdr_chteng_files = " ".join(categories["hdr.chteng"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简英特效",
            "--language",
            "0:zh-Hans",
            hdr_chseng_files,
            "--track-name",
            "0:繁英特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_chteng_files
        ])        

        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # hdr*2 单语
      elif "hdr.chs" in categories and "hdr.cht" in categories and "video"  in categories:
        hdr_chs_files = " ".join(categories["hdr.chs"])
        hdr_cht_files = " ".join(categories["hdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简体特效",
            "--language",
            "0:zh-Hans",
            hdr_chs_files,
            "--track-name",
            "0:繁體特效",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_cht_files
        ])        

        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
   
  else:
      # sdr*4 hdr*4
      if "sdr.chseng" in categories and "sdr.chteng" in categories and "video"  in categories and "hdr.chseng" in categories and "hdr.chteng" in categories and "hdr.cht" in categories and "hdr.chs" in categories and "sdr.cht" in categories and "sdr.chs" in categories:
        sdr_chseng_files = " ".join(categories["sdr.chseng"])
        sdr_chteng_files = " ".join(categories["sdr.chteng"])
        hdr_chseng_files = " ".join(categories["hdr.chseng"])
        hdr_chteng_files = " ".join(categories["hdr.chteng"])
        sdr_chs_files = " ".join(categories["sdr.chs"])
        sdr_cht_files = " ".join(categories["sdr.cht"])
        hdr_chs_files = " ".join(categories["hdr.chs"])
        hdr_cht_files = " ".join(categories["hdr.cht"]) 
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:SDR简英双语",
            "--language",
            "0:zh-Hans",
            sdr_chseng_files,
            "--track-name",
            "0:SDR繁英雙語",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_chteng_files,
            "--track-name",
            "0:SDR简体中文",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hans",
            sdr_chs_files,            
            "--track-name",
            "0:SDR繁體中文",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_cht_files,
            "--track-name",
            "0:HDR简英双语",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chseng_files,
            "--track-name",
            "0:HDR繁英雙語",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_chteng_files,           
            "--track-name",
            "0:HDR简体中文",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chs_files,         
            "--track-name",
            "0:HDR繁體中文",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_cht_files

        ])
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*2 hdr*2 双语
      elif "sdr.chseng" in categories and "sdr.chteng" in categories and "video"  in categories and "hdr.chseng" in categories and "hdr.chteng" in categories:
        sdr_chseng_files = " ".join(categories["sdr.chseng"])
        sdr_chteng_files = " ".join(categories["sdr.chteng"])
        hdr_chseng_files = " ".join(categories["hdr.chseng"])
        hdr_chteng_files = " ".join(categories["hdr.chteng"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:SDR简英双语",
            "--language",
            "0:zh-Hans",
            sdr_chseng_files,
            "--track-name",
            "0:SDR繁英雙語",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_chteng_files,
            "--track-name",
            "0:HDR简英双语",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chseng_files,
            "--track-name",
            "0:HDR繁英雙語",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_chteng_files,           
            "--track-order",
            "1:0,2:0",
            "--default-track-flag",
            "1:yes"
        ])
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*2 hdr*2 单语
      elif "sdr.chs" in categories and "sdr.cht" in categories and "video"  in categories and "hdr.chs" in categories and "hdr.cht" in categories:
        sdr_chs_files = " ".join(categories["sdr.chs"])
        sdr_cht_files = " ".join(categories["sdr.cht"])
        hdr_chs_files = " ".join(categories["hdr.chs"])
        hdr_cht_files = " ".join(categories["hdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:SDR简体中文",
            "--language",
            "0:zh-Hans",
            sdr_chs_files,
            "--track-name",
            "0:SDR繁體中文",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_cht_files,
            "--track-name",
            "0:HDR简体中文",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chs_files,
            "--track-name",
            "0:HDR繁體中文",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_cht_files,           
            "--track-order",
            "1:0,2:0",
            "--default-track-flag",
            "1:yes"
        ])
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*4 双语
      elif "sdr.chseng" in categories and "sdr.chteng" in categories and "video"  in categories and "sdr.chs" in categories and "sdr.cht" in categories:
        sdr_chseng_files = " ".join(categories["sdr.chseng"])
        sdr_chteng_files = " ".join(categories["sdr.chteng"])
        sdr_chs_files = " ".join(categories["sdr.chs"])
        sdr_cht_files = " ".join(categories["sdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简英双语",
            "--language",
            "0:zh-Hans",
            sdr_chseng_files,
            "--track-name",
            "0:繁英雙語",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_chteng_files,
            "--track-name",
            "0:简体中文",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hans",
            sdr_chs_files,         
            "--track-name",
            "0:繁體中文",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_cht_files
        ])
        
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*2 双语
      elif "sdr.chseng" in categories and "sdr.chteng" in categories and "video"  in categories:
        sdr_chseng_files = " ".join(categories["sdr.chseng"])
        sdr_chteng_files = " ".join(categories["sdr.chteng"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简英双语",
            "--language",
            "0:zh-Hans",
            sdr_chseng_files,
            "--track-name",
            "0:繁英雙語",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_chteng_files
        ])        

        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # sdr*2 单语
      elif "sdr.chs" in categories and "sdr.cht" in categories and "video"  in categories:
        sdr_chs_files = " ".join(categories["sdr.chs"])
        sdr_cht_files = " ".join(categories["sdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简体中文",
            "--language",
            "0:zh-Hans",
            sdr_chs_files,
            "--track-name",
            "0:繁體中文",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            sdr_cht_files
        ])        

        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')

      # hdr*4 双语
      elif "hdr.chseng" in categories and "hdr.chteng" in categories and "video"  in categories and "hdr.chs" in categories and "hdr.cht" in categories:
        hdr_chseng_files = " ".join(categories["hdr.chseng"])
        hdr_chteng_files = " ".join(categories["hdr.chteng"])
        hdr_chs_files = " ".join(categories["hdr.chs"])
        hdr_cht_files = " ".join(categories["hdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简英双语",
            "--language",
            "0:zh-Hans",
            hdr_chseng_files,
            "--track-name",
            "0:繁英雙語",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_chteng_files,
            "--track-name",
            "0:简体中文",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hans",
            hdr_chs_files,         
            "--track-name",
            "0:繁體中文",
            "--default-track-flag",
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_cht_files
        ])
        
        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # hdr*2 双语
      elif "hdr.chseng" in categories and "hdr.chteng" in categories and "video"  in categories:
        hdr_chseng_files = " ".join(categories["hdr.chseng"])
        hdr_chteng_files = " ".join(categories["hdr.chteng"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简英双语",
            "--language",
            "0:zh-Hans",
            hdr_chseng_files,
            "--track-name",
            "0:繁英雙語",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_chteng_files
        ])        

        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
  
      # hdr*2 单语
      elif "hdr.chs" in categories and "hdr.cht" in categories and "video"  in categories:
        hdr_chs_files = " ".join(categories["hdr.chs"])
        hdr_cht_files = " ".join(categories["hdr.cht"])
        video_path = categories["video"]["path"]
        video_name = categories["video"]["name"]
        
        subprocess.run([
            mkvmerge_path,
            '--quiet',
            "-o",
            f"{output_path}/{video_name}.mkv",
            "--no-subtitles",
            video_path,
            "--track-name",
            "0:简体中文",
            "--language",
            "0:zh-Hans",
            hdr_chs_files,
            "--track-name",
            "0:繁體中文",
            "--default-track-flag", 
            "0:no",
            "--language",
            "0:zh-Hant",
            hdr_cht_files
        ])        

        if os.path.exists(f"{output_path}/{video_name}.mkv"):
            print(f'已输出\033[35m{video_name}.mkv\033[0m')
        else:
            print(f'输出\033[31m{video_name}.mkv失败\033[0m')
