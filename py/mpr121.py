import Adafruit_GPIO.I2C
import Adafruit_MPR121.MPR121

class MPR121:
	def __init__(self, switch=None):
		self.switch = switch

		if self.switch is not None:
			self._bus = Adafruit_GPIO.I2C.get_i2c_device(busnum=self.switch[0], address=self.switch[1])

		self.mpr121 = Adafruit_MPR121.MPR121.MPR121()

	def begin(self, *args, **kwargs):
		if self.switch is not None:
			self._bus.writeRaw8(self.switch[2])
		return self.mpr121.begin(*args, **kwargs)

	def touched(self):
		if self.switch is not None:
			self._bus.writeRaw8(self.switch[2])
		return self.mpr121.touched()
