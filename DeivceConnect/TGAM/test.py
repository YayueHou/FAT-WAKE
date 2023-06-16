
import serial
import serial.tools.list_ports
import time
# 获取所有串口设备实例。
# 如果没找到串口设备，则输出：“无串口设备。”
# 如果找到串口设备，则依次输出每个设备对应的串口号和描述信息。
ports_list = list(serial.tools.list_ports.comports())
if len(ports_list) <= 0:
    print("无串口设备。")
else:
    print("可用的串口设备如下：")
    for comport in ports_list:
        print(list(comport)[0], list(comport)[1])


 
ser = serial.Serial("COM20", 57600)    # 打开COM17，将波特率配置为115200，其余参数使用默认值
if ser.isOpen():                        # 判断串口是否成功打开
    print("打开串口成功。")
    print(ser.name)    # 输出串口号
else:
    print("打开串口失败。")

while True:
    a=ser.readline()
   
    print(int(a.decode()))
    with open("FRO_FAT_WAK.txt", "a") as file: 
        file.write(str(a))
        
    
   # if b[0] == 170 and b[1] == 170 and b[2] == 4:
     #   b=b+ser.read(5)
     #   while 1:
       #     a=ser.read(8)
       #    print(a)

 
ser.close()