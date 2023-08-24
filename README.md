# little_tools
一些自用脚本 使用chatgpt输出 部分难题感谢**小澪同学**的帮助 [测试环境 `Python 3.10.8`]

# ass24
<details>
<summary><b>说明</b></summary>

  意为ass 24(to four) 仅需要结尾命名为`chseng`的ass文件即可批量进行转换四字幕操作

**环境**
---
```
pip install opencc-python-reimplemented
```
```
pip install pyfiglet
```
**使用**
---
如 `python ass24.py -i d:/test`

`-i`指**输入路径** 如果不填写则为当前路径

脚本将检索目录下的所有命名为`chseng`的ass文件 另外生成**chs cht chteng**三种字幕

转*单语*时将含有**分隔行**后的行进行转换 并且将样式**chs**转换为**chs1**  **tip**转换为**tip1**  **Yingzimu**转换为**Yingzimu1**  **chsHDR**转换为**chsHDR1**

转*繁体*时 可以设置跳过的行 详见第**76~80**行
</details>

# dvhdrplus
<details>
<summary><b>说明</b></summary>
批量将hdr和dv视频转为dv兼容hdr视频

**环境**
---
`ffmpeg` `dvtool` `mkvmerge` `hdr10plus_tool`
```
pip install pyfiglet
```
**使用**
---
如 `python dvhdrplus.py -i d:/test -o d:/output -m dvhdr -f 24000/1001p`

`-i`指**输入路径** 如果不填写则为当前路径 

`-o`指**输出路径**如果不填写则为输入路径下的`dvhdr`或`hdr10plus`文件夹 

`-m`指**模式** 分为`hdr10plus`和`dvhdr` 

`-f`指**输出视频的帧率**如果不填写默认为24000/1001p

如果模式为`hdr10plus`则检索目录下命名含有**hdr10plus,hdr10+**的**mp4**和**mkv**文件 且需要修改第**99**行hdr10plus的[json](https://github.com/quietvoid/dovi_tool)文件路径 输出命名修改参照第**120**行

如果模式为`dvhdr`则检索目录下命名含有**dv**与**hdr10/hdr10+**(除dv和hdr10部分其他命名需**保持一致**)的**mp4**和**mkv**文件 输出命名修改参照第**228**行
</details>

# sup
<details>
<summary><b>说明</b></summary>

批量将 **sup** 字幕封装进 **mkv** 视频 且命名为对应的轨道

**环境**
---
`mkvmerge`
```
pip install pyfiglet
```
**使用**
---
如 `python sup.py -i d:/test -o d:/out -n Hijack -m movie -t tx`

`-i`指**输入路径**(要求目录下**只允许有**转换的视频和sup文件 否则可能会报错) 如果不填写则为当前路径 

`-o`指**输出路径** `-n`指**文件识别名**(只需要填前面一小段即可) 

`-t`指**输出字幕轨道标题** tx则为命名为简英特效等 不填写为普通的简英双语等 

`-m`指**模式** 填写`movie`则为**单个**电影 不填写则为剧集 将进行季集的判断

**要求**
`sup`字幕命名必须为`sdr.chseng/hdr.chseng` 如果只封装**sdr或hdr**字幕 也需以上命名
</details>
