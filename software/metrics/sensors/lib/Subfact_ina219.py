#!/usr/bin/python

import time
import smbus
from Adafruit_I2C import Adafruit_I2C

# ===========================================================================
# INA219 Class
# ===========================================================================

class INA219:
	i2c = None

# ===========================================================================
#   I2C ADDRESS/BITS
# ==========================================================================
	__INA219_ADDRESS                         = 0x40    # 1000000 (A0+A1=GND)
	__INA219_READ                            = 0x01
# ===========================================================================

# ===========================================================================
#    CONFIG REGISTER (R/W)
# ===========================================================================
	__INA219_REG_CONFIG                      = 0x00
# ===========================================================================
	__INA219_CONFIG_RESET                    = 0x8000  # Reset Bit
	__INA219_CONFIG_BVOLTAGERANGE_MASK       = 0x2000  # Bus Voltage Range Mask
	__INA219_CONFIG_BVOLTAGERANGE_16V        = 0x0000  # 0-16V Range
	__INA219_CONFIG_BVOLTAGERANGE_32V        = 0x2000  # 0-32V Range

	__INA219_CONFIG_GAIN_MASK                = 0x1800  # Gain Mask
	__INA219_CONFIG_GAIN_1_40MV              = 0x0000  # Gain 1, 40mV Range
	__INA219_CONFIG_GAIN_2_80MV              = 0x0800  # Gain 2, 80mV Range
	__INA219_CONFIG_GAIN_4_160MV             = 0x1000  # Gain 4, 160mV Range
	__INA219_CONFIG_GAIN_8_320MV             = 0x1800  # Gain 8, 320mV Range

	__INA219_CONFIG_BADCRES_MASK             = 0x0780  # Bus ADC Resolution Mask
	__INA219_CONFIG_BADCRES_9BIT             = 0x0080  # 9-bit bus res = 0..511
	__INA219_CONFIG_BADCRES_10BIT            = 0x0100  # 10-bit bus res = 0..1023
	__INA219_CONFIG_BADCRES_11BIT            = 0x0200  # 11-bit bus res = 0..2047
	__INA219_CONFIG_BADCRES_12BIT            = 0x0400  # 12-bit bus res = 0..4097

	__INA219_CONFIG_SADCRES_MASK             = 0x0078  # Shunt ADC Resolution and Averaging Mask
	__INA219_CONFIG_SADCRES_9BIT_1S_84US     = 0x0000  # 1 x 9-bit shunt sample
	__INA219_CONFIG_SADCRES_10BIT_1S_148US   = 0x0008  # 1 x 10-bit shunt sample
	__INA219_CONFIG_SADCRES_11BIT_1S_276US   = 0x0010  # 1 x 11-bit shunt sample
	__INA219_CONFIG_SADCRES_12BIT_1S_532US   = 0x0018  # 1 x 12-bit shunt sample
	__INA219_CONFIG_SADCRES_12BIT_2S_1060US  = 0x0048  # 2 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_4S_2130US  = 0x0050  # 4 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_8S_4260US  = 0x0058  # 8 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_16S_8510US = 0x0060  # 16 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_32S_17MS   = 0x0068  # 32 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_64S_34MS   = 0x0070  # 64 x 12-bit shunt samples averaged together
	__INA219_CONFIG_SADCRES_12BIT_128S_69MS  = 0x0078  # 128 x 12-bit shunt samples averaged together

	__INA219_CONFIG_MODE_MASK                = 0x0007  # Operating Mode Mask
	__INA219_CONFIG_MODE_POWERDOWN           = 0x0000
	__INA219_CONFIG_MODE_SVOLT_TRIGGERED     = 0x0001
	__INA219_CONFIG_MODE_BVOLT_TRIGGERED     = 0x0002
	__INA219_CONFIG_MODE_SANDBVOLT_TRIGGERED = 0x0003
	__INA219_CONFIG_MODE_ADCOFF              = 0x0004
	__INA219_CONFIG_MODE_SVOLT_CONTINUOUS    = 0x0005
	__INA219_CONFIG_MODE_BVOLT_CONTINUOUS    = 0x0006
	__INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS = 0x0007
# ===========================================================================

# ===========================================================================
#   SHUNT VOLTAGE REGISTER (R)
# ===========================================================================
	__INA219_REG_SHUNTVOLTAGE                = 0x01
# ===========================================================================

# ===========================================================================
#   BUS VOLTAGE REGISTER (R)
# ===========================================================================
	__INA219_REG_BUSVOLTAGE                  = 0x02
# ===========================================================================

# ===========================================================================
#   POWER REGISTER (R)
# ===========================================================================
	__INA219_REG_POWER                       = 0x03
# ===========================================================================

# ==========================================================================
#    CURRENT REGISTER (R)
# ===========================================================================
	__INA219_REG_CURRENT                     = 0x04
# ===========================================================================

# ===========================================================================
#    CALIBRATION REGISTER (R/W)
# ===========================================================================
	__INA219_REG_CALIBRATION                 = 0x05
# ===========================================================================

	# Constructor
	def __init__(self, address=0x40, debug=False):
		self.i2c = Adafruit_I2C(address, debug=False)
		self.address = address
		self.debug = debug

		self.ina219SetCalibration_32V_2A()

	def ina219SetCalibration_32V_2A(self):
		self.ina219_currentDivider_mA = 10  # Current LSB = 100uA per bit (1000/100 = 10)
		self.ina219_powerDivider_mW = 2     # Power LSB = 1mW per bit (2/1)

		# Set Calibration register to 'Cal' calculated above	
		bytes = [(0x1000 >> 8) & 0xFF, 0x1000 & 0xFF]
		self.i2c.writeList(self.__INA219_REG_CALIBRATION, bytes)

		# Set Config register to take into account the settings above
		config = self.__INA219_CONFIG_BVOLTAGERANGE_32V | \
		         self.__INA219_CONFIG_GAIN_8_320MV | \
		         self.__INA219_CONFIG_BADCRES_12BIT | \
		         self.__INA219_CONFIG_SADCRES_12BIT_1S_532US | \
		         self.__INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS

		bytes = [(config >> 8) & 0xFF, config & 0xFF]
		self.i2c.writeList(self.__INA219_REG_CONFIG, bytes)

	def getBusVoltage_raw(self):
		result = self.i2c.readU16(self.__INA219_REG_BUSVOLTAGE)

		# Shift to the right 3 to drop CNVR and OVF and multiply by LSB
		return (result >> 3) * 4

	def getShuntVoltage_raw(self):
		result = self.i2c.readList(self.__INA219_REG_SHUNTVOLTAGE,2)
		if (result[0] >> 7 == 1):
			value = ((result[0] & 0xF0) | ( result[1])) - 1
			return ~ value
		else:
			return (result[0] << 8) | (result[1])

	def getCurrent_raw(self):
		result = self.i2c.readList(self.__INA219_REG_CURRENT,2)
		if (result[0] >> 7 == 1):
			value = ((result[0] & 0xF0) | ( result[1])) - 1
			return ~ value
		else:
			return (result[0] << 8) | (result[1])

	def getPower_raw(self):
		result = self.i2c.readList(self.__INA219_REG_POWER,2)
		if (result[0] >> 7 == 1):
			value = ((result[0] & 0xF0) | ( result[1])) - 1
			return ~ value
		else:
			return (result[0] << 8) | (result[1])

	def getShuntVoltage_mV(self):
		value = self.getShuntVoltage_raw()
		return value * 0.01

	def getBusVoltage_V(self):
		value = self.getBusVoltage_raw()
		return value * 0.001

	def getCurrent_mA(self):
		valueDec = self.getCurrent_raw()
		valueDec /= self.ina219_currentDivider_mA
		return valueDec
	def getPower_mW(self):
		valueDec = self.getPower_raw()
		valueDec /= self.ina219_powerDivider_mW
		return valueDec
