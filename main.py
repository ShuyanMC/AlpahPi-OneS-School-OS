# 从这里开始编写代码
#-- Red Star OS For SCHOOL--
#ARE YOU OK?_record
#import
import time
import network
import random
#ret# 
# 小说数据
novels = {
    "末日小说": {
        "1-1": """
小说内容-小说1的第一章
        """,
        "1-2": """
小说内容-小说1的第二章
        """
    },
    "小说2": {
        "1-1": "小说内容-小说2的第一章",
        "1-2": "小说内容-小说2的第二章"
    }
}

keyx=int(0)
# 初始化Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#def
# 扫描Wi-Fi并筛选指定网络
def scan_wifi():
    wlan.scan()
    time.sleep(2)  # 等待扫描完成
    networks = wlan.scan()
    target_ssids = ["Tenda_CF13B0", "Tenda_CF13B0_5G", "房间-5G", "房间-4G"]
    target_networks = []

    for ssid, bssid, channel, rssi, authmode, hidden in networks:
        ssid = ssid.decode()
        if ssid in target_ssids:
            target_networks.append((ssid, rssi))

    # 按信号强度排序(信号越强,rssi值越小)
    target_networks.sort(key=lambda x: x[1], reverse=True)
    return target_networks


# 连接Wi-Fi
def connect_wifi(ssid, password):
    clear()
    printPos("正在连接中...", "中间")

    wlan.connect(ssid, password)
    start_time = time.time()
    while not wlan.isconnected():
        time.sleep(1)
        if time.time() - start_time > 30:
            clear()
            printPos("连接失败!", "中间")
            return False

    clear()
    printPos(f"连接成功!Wi-Fi名:{ssid}", "中间")
    return True

# Wi-Fi连接函数
def wifi():
    clear()
    printPos("正在扫描Wi-Fi...", "中间")
    target_networks = scan_wifi()

    if not target_networks:
        clear()
        printPos("未找到目标Wi-Fi,跳过连接", "中间")
        time.sleep(3)
        return

    # 选择信号最强的Wi-Fi
    ssid, _ = target_networks[0]
    password = "d21812900"

    while True:
        if connect_wifi(ssid, password):
            break
        else:
            while True:
                clear()
                printPos("连接失败,按A键重试,按B键跳过", "中间")
                if isPressed('A'):
                    clear()
                    printPos("正在重新连接...", "中间")
                    break
                elif isPressed('B'):
                    clear()
                    printPos("跳过Wi-Fi连接,继续后续操作", "中间")
                    time.sleep(3)
                    return

# 红外遥控功能
def IRS():
    key = getIRKey()
    if key == '1':
        playMusic()
        clear()
        song = getSongName()
        printPos(song, '中间')
        printPos("退出D", "右下")
    if isPressed('D'):
        stopMusic()
        clear()
    if key == '上':
        volumeUp()
    if key == "下":
        volumeDown()
    
def book():
    while True:
        clear()  # 清屏
        printPos("请选择小说:", "中间")  # 提示用户选择小说
        printPos("    1. 小说1", "左上")
        printPos("    2. 小说2", "左下")
        printPos("按OK键确认选择", "中间")

        selected_novel = None
        while True:
            key = getIRKey()  # 获取按键
            if key == '1':
                selected_novel = "末日小说"
                break
            elif key == '2':
                selected_novel = "小说2"
                break
            elif key == 'OK':
                if selected_novel:
                    break

        if selected_novel:
            clear()  # 清屏
            printPos(f"您选择了:{selected_novel}", "中间")
            printPos("1. 第1章", "中间")
            printPos("    2. 第2章", "左下")
            printPos("    按OK键确认选择", "右上")

            selected_chapter = None
            while True:
                key = getIRKey()  # 获取按键
                if key == '1':
                    selected_chapter = "1-1"
                    break
                elif key == '2':
                    selected_chapter = "1-2"
                    break
                elif key == 'OK':
                    if selected_chapter:
                        break

            if selected_chapter:
                clear()  # 清屏
                printPos(f"您正在阅读:{selected_novel} - {selected_chapter}", "中间")
                content = novels[selected_novel][selected_chapter]  # 获取章节内容
                content_length = len(content)  # 获取总长度
                start_index = 0  # 开始显示的索引

                while True:
                    clear()  # 清屏
                    printPos(f"您正在阅读:{selected_novel} - {selected_chapter}", "中间")
                    # 显示从 start_index 开始的70个字符
                    end_index = min(start_index + 70, content_length)
                    printPos(content[start_index:end_index], "下面")

                    # 等待用户按键
                    while True:  # 进入等待循环
                        key = getIRKey()
                        if key == '#':  # 按下 # 键,显示下一页
                            start_index += 70
                            if start_index >= content_length:  # 如果已经到达末尾
                                start_index = content_length - (content_length % 70 or 70)
                            break  # 跳出等待循环,重新显示内容
                        elif key == '*':  # 按下 * 键,显示上一页
                            start_index -= 70
                            if start_index < 0:  # 如果超出开头
                                start_index = 0
                            break  # 跳出等待循环,重新显示内容
                        elif key == 'OK':  # 按下 OK 键,返回
                            return  # 退出阅读模式,返回主菜单

                clear()  # 清屏
                printPos("    按OK键返回", "左下")
                while True:
                    key = getIRKey()  # 等待返回
                    if key == 'OK':  # 检测到 OK 键
                        break

        clear()  # 清屏
        printPos("感谢使用小说阅读器!", "中间")
        printPos("按OK键退出或重新选择", "下面")
        while True:
            key = getIRKey()  # 等待退出或重新选择
            if key == 'OK':  # 检测到 OK 键
                break            
# UI界面
def UI():
    print_star()
    printPos("    A.番茄学习法", "左上")
    printPos("B.太阳の威严", "中间")
    printPos("    C.Addon", "左下")
    printPos("退出D", "右下")

def fkxsf():
    tomato = readPic('tomato')
    showPic(tomato)
    board = readPic('board')
    showPic(board, 34, 45)
    # 改变下面的分钟数和秒数,就可以改变倒计时时间
    minute = 25
    second = 0
    total = minute * 60 + second
    for i in range(total):
        if second == 0:
            minute = minute - 1
            second = 60
        time.sleep(1)
        second = second - 1
        result = str(minute) + ':' + str(second)
        printPos(result, '中间','中')
    printPos('时间结束', '中间')
# 把下面的playMusic()语句替换成playRecord()
    playMusic()
#while True:
#    key = getIRKey()
    #if key =="0":
      #  clear()
        #printPos("录制中...","中间")
       # record(1)
    #if key =="#":
      #  clear()
       # printPos("听取中...","中间")
        #playRecord(1)
 # OS   
#-- Red Star OS For SCHOOL--|--START--|
#logo
def print_star():
    # 定义rs的图案
    star = [
        "-- Red Star OS For SCHOOL--",
    ]

    # 获取终端宽度
    try:
        import os
        terminal_width = os.get_terminal_size().columns
    except Exception:
        terminal_width = 80  # 默认宽度

    # 计算居中偏移量
    max_length = max(len(line) for line in star)
    offset = (terminal_width - max_length) // 2

    # 打印rs并居中
    for line in star:
        print(" " * offset + line)

print_star()
############################################################
#playRecord
  #用法:playRecord(1) io:(x)的x代表第x个record
playRecord(1)
# 执行Wi-Fi连接
wifi()
time.sleep(1.145141919810)
clear()
############################################################
#User Register & User Login
printPos("请输入你的密码","中间")
printPos("未注册的用户自动注册","左下")
printPos("放心!密码输入时不可见","左上")
clear()
printPos("此功能lyyl?no","中间")
while True:
    printPos(keyx,"中间")
    key = getIRKey()
    time.sleep(0.114514)
    if isPressed('A'):
        keyx+=6110
    time.sleep(0.114514)
    if isPressed('B'):
        keyx+=100
    time.sleep(0.114514)
    if isPressed('C'):
        keyx-=100
    time.sleep(0.114514)
    int(keyx) 
    if keyx ==6110:
        clear()
        break
printPos("    A.番茄学习法","左上")
printPos("B.太阳の威严","中间")
printPos("    C.Addon","左下")
# 主程序逻辑
while True:
    key = getIRKey()
    if isPressed('A'):  # 番茄学习法
        fkxsf()
        clear()
        UI()
    elif isPressed('B'):  # 播放录音
        playRecord(1)
        clear()
        UI()
    elif isPressed('C'):  # 红外遥控功能说明书
        clear()
        printPos("    遥控板功能说明书", "左上")
        printPos("1. 听歌(随机)", "中间")
        printPos("2. 小说阅读器", "左下")
        printPos("退出D", "右下")
        page = 1  # 当前页码

        while True:
            if page == 1:
                clear()
                printPos("    遥控板功能说明书", "左上")
                printPos("1. 听歌(随机)", "中间")
                printPos("退出D", "右下")
                time.sleep(1.14514)
                printPos("    按键说明:", "左上")
                printPos("    - 按 # 键: 下一页", "中间")
                printPos("    - 按 * 键: 上一页", "中间")
                printPos("    - 按 OK 键: 返回", "右下")
                time.sleep(1.14514)
            elif page == 2:
                clear()
                printPos("    遥控板功能说明书", "左上")
                printPos("2. 小说阅读器", "中间")
                printPos("退出D", "右下")
                time.sleep(1.14514)
                printPos("    按键说明:", "左上")
                printPos("    - 按 # 键: 下一页", "中间")
                printPos("    - 按 * 键: 上一页", "中间")
                printPos("    - 按 OK 键: 返回", "右下")
                printPos("    - 按 D 键: 退出说明书", "左下")
                time.sleep(1.14514)
            key = getIRKey()
            if key == '#':  # 下一页
                page += 1
                if page > 2:
                    page = 2
            elif key == '*':  # 上一页
                page -= 1
                if page < 1:
                    page = 1
            elif isPressed('D'):  # 退出说明书
                clear()
                UI()
                break
            elif key == 'OK':  # 返回
                clear()
                UI()
                break
    elif key == '2':  # 小说阅读
        book()
    IRS()  # 持续监听红外遥控
