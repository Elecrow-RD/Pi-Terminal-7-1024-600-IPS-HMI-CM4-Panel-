import smbus
import time
import sys
import os

# 获取I2C总线
bus = smbus.SMBus(1)

# # 获取程序外部参数
# ledVal = int(sys.argv[1])
# buzVal = int(sys.argv[2])
# relVal = int(sys.argv[3])

pin = int(sys.argv[1])
val = int(sys.argv[2])

# PCA9557 I2C地址
PCA9557_ADDRESS = 0x18

# PCA9557寄存器地址
PCA9557_INPUT       = 0x00          #   输入寄存器(只读取，写入没用)
PCA9557_OUTPUT      = 0x01          #   输出寄存器
PCA9557_POLARITY    = 0x02          #   极性寄存器
PCA9557_CONFIG      = 0x03          #   配置寄存器

def bit_set(pin_val, pin):
    """将指定的bit位置1"""
    return pin_val | (1 << pin)

def bit_clear(pin_val, pin):
    """将指定的bit位置0"""
    return pin_val & ~(1 << pin)

def bit_read(pin_val, pin):
    """读取指定的bit位"""
    return (pin_val >> pin) & 0x01

def bit_write(pin, pin_val, val):
    """根据val的值将指定的bit位置1或0"""
    if val:
        return bit_set(pin_val, pin)
    else:
        return bit_clear(pin_val, pin)

# 读取PCA9557输入引脚的值
def pca9557_read():
    return bus.read_byte_data(PCA9557_ADDRESS, PCA9557_OUTPUT)

# 设置PCA9557单独输出引脚的值
def pca9557OnePinWrite(pin, val):
    ##  首先获取pca9557寄存器的值
    value = pca9557_read()
    value = bit_write(pin, value, val)
    bus.write_byte_data(PCA9557_ADDRESS, PCA9557_OUTPUT, value)

# def AllValue():
#     value = pca9557_read()
#     value = bit_write(1, value, ledVal) # 设置LED的值
#     value = bit_write(0, value, buzVal) # 设置BUZZER的值
#     value = bit_write(7, value, relVal) # 设置继电器的值
#     return value

def pca9557WriteValue(value):
    bus.write_byte_data(PCA9557_ADDRESS, PCA9557_OUTPUT, value)

# 主程序
if __name__ == "__main__":
    # 设置输出引脚的值
    pca9557OnePinWrite(pin, val)

