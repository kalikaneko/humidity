# graph.py

import rrdtool

class Graph(object):

	def options(self):
		return [
			'--width', '750',
			'--height', '400',
			'--imgformat', 'PNG',
			'--lazy',
			'--disable-rrdtool-tag',
			'--upper-limit', '100',
			'--lower-limit', '0',
			'--slope-mode',
			'--right-axis', '0.333:0',
			'--end', 'now',
			'--vertical-label', 'humidity %',
			'--right-axis-label', 'temperature (C)',
			'--color', 'GRID#ffffff00',
			'--color',  'MGRID#ffffff00',
			'--color', 'SHADEA#000000',
			'--color', 'SHADEB#000000',
			'--font', 'DEFAULT:10:/DejaVuSansMono',
			'--font', 'WATERMARK:4:/DejaVuSansMono',
			'--font', 'TITLE:10:DejaVuSansMono',
			'--font', 'AXIS:10',
			'DEF:rawtemp=%s.rrd:temperature:AVERAGE' % self._sensor.name,
			'DEF:rawtempmin=%s.rrd:temperature:MIN' % self._sensor.name,
			'DEF:rawtempmax=%s.rrd:temperature:MAX' % self._sensor.name,
			'DEF:humidity=%s.rrd:humidity:AVERAGE' % self._sensor.name,
			'DEF:humiditymin=%s.rrd:humidity:MIN' % self._sensor.name,
			'DEF:humiditymax=%s.rrd:humidity:MAX' % self._sensor.name,
			'DEF:state=%s.rrd:state:MAX' % self._sensor.name,
			'CDEF:output=state,10,*',
			'CDEF:humidityrange=humiditymax,humiditymin,-',
			'CDEF:temp=rawtemp,3,*',
			'CDEF:tempmin=rawtempmin,3,*',
			'CDEF:tempmax=rawtempmax,3,*',
			'CDEF:temprange=tempmax,tempmin,-',
		]

	def __init__(self, path, sensor):
		self._sensor = sensor
		self._path = path

	def draw(self):

		rrdtool.graph( [ '%s/%s-1-hour.png' % (self._path, self._sensor.name)] +
			self.options() + [
				'--title', '%s (1 Hour)' % self._sensor.name,
				'--start', '-3600',
				'AREA:humidity#3C2DE0:Humidity',
				'AREA:temp#D60909:Temperature',
				'LINE2:temp#ffffffff',
				'LINE2:humidity#000000ff',
				'AREA:output#00000055:Output On/Off'
			]
		)

		rrdtool.graph( [ '%s/%s-24-hours.png' % (self._path, self._sensor.name)] +
			self.options() + [
				'--title', '%s (24 Hours)' % self._sensor.name,
				'--start', '-86400',
				'LINE1:tempmin#ff0000',
				'AREA:temprange#ff000088::STACK',
				'LINE1:tempmax#ff0000',
				'LINE1:humiditymin#0000ff',
				'AREA:humidityrange#0000ff88::STACK',
				'LINE1:humiditymax#0000ff'
			]
		)

		rrdtool.graph( [ '%s/%s-7-days.png' % (self._path, self._sensor.name)] +
			self.options() + [
				'--title', '%s (7 Days)' % self._sensor.name,
				'--start', '-604800',
				'LINE1:tempmin#ff0000',
				'AREA:temprange#ff000088::STACK',
				'LINE1:tempmax#ff0000',
				'LINE1:humiditymin#0000ff',
				'AREA:humidityrange#0000ff88::STACK',
				'LINE1:humiditymax#0000ff',
				'LINE2:temp#ff0000',
				'LINE2:humidity#0000ff'
			]
		)

