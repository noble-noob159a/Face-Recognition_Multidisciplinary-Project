from lib.mqtt import *
from yolobit import *
button_a.on_pressed = None
button_b.on_pressed = None
button_a.on_pressed_ab = button_b.on_pressed_ab = -1
from machine import RTC
from lib.ntp_helper import set_time_from_ntp, get_time, get_time_str
import time
from lib.event_manager_ohstem import event_manager
from homebit3_lcd1602 import LCD1602
event_manager.reset()
lcd1602 = LCD1602()

WIFI_SSID = 'ABC'
WIFI_PASSWORD = 'ABCDEFG'

def on_mqtt_message_receive_callback__V1_(name):
  # global th_C3_B4ng_tin, Chu_E1_BB_97i_AI, Th_E1_BB_9Di_gian, RT, RH, L_E1_BB_87nh_AI, SM, LUX
  lcd1602.clear()
  if name != 'UNKNOWN':
    lcd1602.move_to(0, 0)
    lcd1602.putstr('Valid:')
  else:
    # lcd1602.clear()
    lcd1602.move_to(0, 0)
    lcd1602.putstr('Invalid:')
  lcd1602.move_to(0, 1)
  lcd1602.putstr(name)
  # display.scroll(name)

def init_mqtt():
  global name
  mqtt.on_receive_message('V1', on_mqtt_message_receive_callback__V1_)

if True:
  lcd1602.clear()
  lcd1602.move_to(0, 0)
  lcd1602.putstr('GloryMU Started')
  mqtt.connect_wifi(WIFI_SSID, WIFI_PASSWORD) 
  mqtt.connect_broker(server='mqtt.ohstem.vn', port=1883, username='gloryml4u', password='')
  init_mqtt()
  # set_time_from_ntp()
  display.scroll('OK')

while True:
  mqtt.check_message()
  event_manager.run()
  # time.sleep_ms(10)
  time.sleep_ms(100)