import smbus
import time
import sys
import os

# 获取I2C总线
bus = smbus.SMBus(1)

# PCA9557 I2C地址
PCA9557_ADDRESS = 0x18

# PCA9557寄存器地址
PCA9557_INPUT       = 0x00          #   输入寄存器(只读取，写入没用)
PCA9557_OUTPUT      = 0x01          #   输出寄存器
PCA9557_POLARITY    = 0x02          #   极性寄存器
PCA9557_CONFIG      = 0x03          #   配置寄存器


# 初始化PCA9557
# 引脚                               7   6   5     4   3   2   1    0
# 0x03寄存器 0: 输出模式 1: 输入模式  RE  DO1 DO2  PORT DI2 DI1 LED BEEP
# 配置寄存器0x03写0x0c--->            0   0   0    0    1   1   0   0
# 设置输出寄存器初始值，写0x01输出寄存器0x02,让LED灯灭
def pca9557_init():
    # 配置所有引脚为输出
    bus.write_byte_data(PCA9557_ADDRESS, PCA9557_CONFIG, 0x0c)
    # 初始化输出值
    bus.write_byte_data(PCA9557_ADDRESS, PCA9557_OUTPUT, 0x01)

# 主程序
if __name__ == "__main__":
    pca9557_init()
