import RPi.GPIO as GPIO
from time import sleep
from PIL import Image, ImageDraw, ImageFont
from ST7789 import ST7789  # Adaptez selon votre bibliothèque ST7789

# Configuration des GPIO pour les boutons
buttons = {'UP': 5, 'DOWN': 6, 'ENTER': 13, 'BACK': 19}
GPIO.setmode(GPIO.BCM)
for btn, pin in buttons.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialisation de l'écran
screen = ST7789(width=240, height=280, rotation=90, spi_bus=0, spi_device=0)
screen.init()

# Police pour le texte
font = ImageFont.load_default()

# Définir les pages de menu
pages = [
    {"name": "Notifications", "action": "show_notifications"},
    {"name": "Config Réseau", "action": "show_network"},
    {"name": "Redémarrer RPi", "action": "restart_rpi"},
    {"name": "Éteindre RPi", "action": "shutdown_rpi"},
    {"name": "Redémarrer ESP32", "action": "restart_esp32"}
]
current_page = 0

# Fonction pour dessiner une page
def display_page(index):
    image = Image.new("RGB", (240, 280), "black")
    draw = ImageDraw.Draw(image)
    draw.text((20, 120), pages[index]["name"], font=font, fill="white")
    screen.display(image)

display_page(current_page)

# Actions des menus
def execute_action(action):
    if action == "show_notifications":
        show_notifications()
    elif action == "show_network":
        show_network_config()
    elif action == "restart_rpi":
        restart_rpi()
    elif action == "shutdown_rpi":
        shutdown_rpi()
    elif action == "restart_esp32":
        restart_esp32()

# Fonctions spécifiques aux actions
def show_notifications():
    print("Affichage des notifications...")

def show_network_config():
    print("Affichage de la configuration réseau...")

def restart_rpi():
    print("Redémarrage du Raspberry Pi...")
    os.system("sudo reboot")

def shutdown_rpi():
    print("Extinction du Raspberry Pi...")
    os.system("sudo poweroff")

def restart_esp32():
    print("Redémarrage des ESP32...")
    # Ajoutez des appels à l'API Home Assistant pour redémarrer les ESP32

# Gestion des boutons
def navigate(button):
    global current_page
    if button == "UP":
        current_page = (current_page - 1) % len(pages)
    elif button == "DOWN":
        current_page = (current_page + 1) % len(pages)
    elif button == "ENTER":
        execute_action(pages[current_page]["action"])
    display_page(current_page)

def button_callback(channel):
    for btn, pin in buttons.items():
        if channel == pin:
            navigate(btn)

for pin in buttons.values():
    GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback, bouncetime=200)

# Boucle principale
try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()