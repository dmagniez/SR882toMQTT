import serial
import json
import paho.mqtt.client as mqtt
import time

# Configuration du port série
port = "/dev/ttyUSB0"
baudrate = 4800
Mqtt_target = "192.168.1.40"

# Envoi de la commande
commande = bytes.fromhex("0103000000101400")

MqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"Solar")
MqttClient.connect(Mqtt_target,1883)
MqttClient.loop_start()

# Ouvrir le port série

def to_int(value):
	x = int(value,16)
	return x
def to_bin(value):
	x = to_int(value)
	x = format(x, '08b')
	return x


while True:
	with serial.Serial(port, baudrate, timeout=1) as ser:
		ser.write(commande)  # Envoi de la commande
		response = ser.read(35)  # Lecture de la réponse (ajuster si besoin)

	# Convertir la réponse en hexadécimal lisible
	response_hex = response.hex().upper()

	# Ignorer les 4 premiers caractères (01 03) → Données utiles à partir de l'index 4
	data_hex = response_hex[2:]

	decoded_values = {
	"T0" : to_int(data_hex[6:8]), #0H
	"T1" : to_int(data_hex[8:10]), #0L
	"T2" : to_int(data_hex[10:12]), #1H
	"T3" : to_int(data_hex[12:14]), #1L
	"T4" : to_int(data_hex[14:16]), #2H
	"T5" : to_int(data_hex[16:18]), #2L
	"T6" : to_int(data_hex[18:20]), #3H
	"T7" : to_int(data_hex[20:22]), #3L
	#index 4 vide
	"pump_time" : to_int(data_hex[24:28]), #5H
	"daily_thermal_output" : to_int(data_hex[28:32]), #6
	"accumulated_thermal_output_kw" : to_int(data_hex[32:36]), #7
	"accumulated_thermal_output_mw" : to_int(data_hex[36:40]), #8
	"speed_adjustable_percent_pump1" : to_int(data_hex[40:42]), #9H
	"speed_adjustable_percent_pump2" : to_int(data_hex[42:44]), #9L
	"P1 settings" : to_bin(data_hex[44:46])[0],
	"P2 settings" : to_bin(data_hex[44:46])[1],
	"P3 settings" : to_bin(data_hex[44:46])[2],
	"P4 settings" : to_bin(data_hex[44:46])[3],
	"H1 settings" : to_bin(data_hex[44:46])[4],
	"register change flag" : to_int(data_hex[46:48]),
	"dry heat protection function" : to_bin(data_hex[48:50])[6],
	"emergency closing function of tank" : to_bin(data_hex[48:50])[5],
	"high temperature protection function of tank" : to_bin(data_hex[48:50])[4],
	"re-cooling function of collector" : to_bin(data_hex[48:50])[3],
	"anti-frost protection of collector" : to_bin(data_hex[48:50])[2],
	"low temperature protection function of collector" : to_bin(data_hex[48:50])[1],
	"emergency closing function of collector" : to_bin(data_hex[48:50])[0],
	"system operation status" : to_bin(data_hex[56:58])[0],
	"manual heating function" : to_bin(data_hex[56:58])[1],
	"holiday function" : to_bin(data_hex[56:58])[2],
	"by-pass function" : to_bin(data_hex[56:58])[3],
	"anti-legionaries function" : to_bin(data_hex[56:58])[4],
	"thermal energy measuring function" : to_bin(data_hex[56:58])[5],
	"setting of fahrenheit temperature unit" : to_bin(data_hex[56:58])[6],
	"hot water pipe circuit function" : to_bin(data_hex[56:58])[7],
	}

	MqttClient.publish("solar/Temp_Panneaux", decoded_values['T0'])
	MqttClient.publish("solar/Temp_Ballon_bas", decoded_values['T1'])
	MqttClient.publish("solar/Temp_Ballon_haut", decoded_values['T2'])
	MqttClient.publish("solar/Temp_circuit_depart", decoded_values['T4'])
	MqttClient.publish("solar/Temp_circuit_retour", decoded_values['T5'])
	MqttClient.publish("solar/puissance_totale", decoded_values['accumulated_thermal_output_kw'])
	MqttClient.publish("solar/puissance_jour", decoded_values['daily_thermal_output'])
	MqttClient.publish("solar/speed_pump_percent", decoded_values['speed_adjustable_percent_pump1'])

	time.sleep(5)

