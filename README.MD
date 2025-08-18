Weiterentwickelt auf GitLab.
Bei interesse meld dich gerne bei mir privat oder per issue


```
 _____                            _                  _            
|_   _| __ __ _ _ __ ___         / \   _ __  _______(_) __ _  ___ 
  | || '__/ _` | '_ ` _ \ _____ / _ \ | '_ \|_  / _ \ |/ _` |/ _ \
  | || | | (_| | | | | | |_____/ ___ \| | | |/ /  __/ | (_| |  __/
  |_||_|  \__,_|_| |_| |_|    /_/   \_\_| |_/___\___|_|\__, |\___|
                                                       |___/      
```
# Wann fährt die nächste Tram?

![](TramAnzeige.jpg)

## Warum?

Weil's oft pressiert, und man nicht immer auf das Handy schauen will!

## Was zeigt's an?
- Anzeige in Minuten für die nächste Tram
- Rot = Linie 4
- Blau = Linie 2
- Mitte = Wertachbrücke
- Alle Lichter representieren Trams
    - Wandern zur Mitte
    - Abstand 5 LEDs = in 5 Minuten fährt die Tram an der Wertachbrücke ab

## Benötigte Hardware
- Raspberry Pi Pico W (recommended)
- LED-Streifen, einzel addressierbar (WS2812b)
- n paar Käbelchen zum anlöten
- micro usb Kabel
- Stromquelle

### Alternative Hardware:
- **ESP32-C3**: Possible alternative to Pico W, but requires code adaptation
  - See [ESP32-C3 Troubleshooting Guide](ESP32-C3-TROUBLESHOOTING.md) for connectivity issues
  - Would need porting from CircuitPython to Arduino/MicroPython

### zum Basteln
- Lötkolben
- PC

## Installation
- Circuit Python auf Pico W installieren: [circuitpython Downloadseite](https://circuitpython.org/board/raspberry_pi_pico_w/)
- dateien von `pi-pico-w/` auf `CIRCUITPY` kopieren
  - Wlan SSID + Passwort in `settings.toml` auf Pico W speichern (Siehe [settings.toml.sample](pi-pico-w/settings.toml.sample))
  - [Libraries](pi-pico-w/lib) kopieren
  - [`color.py`](pi-pico-w/color.py), [`code.py`](pi-pico-w/code.py) und [`settings.py`](pi-pico-w/settings.py) auf Pico W kopieren    
  - [`settings.py`](pi-pico-w/settings.py) auf neuen Bedarf anpassen
    - um deine STOP_ID herauszufinden kannst du [`what-is-my-stop-id.sh`](what-is-my-stop-id.sh) verwenden  
    ``` sh
    ./what-is-my-stop-id.sh Wertachbrücke
    ```

## Trouble shooting:

### Hardware Issues:
- **ESP32-C3 not showing as ttyACM* device?** See [ESP32-C3 Troubleshooting Guide](ESP32-C3-TROUBLESHOOTING.md)
- **Raspberry Pi Pico W not detected?** Try different USB cable or port, check for driver issues

### Error Codes (LED Patterns):
- Gelb, blink Rot, Gelb
  => Konnte nicht mit WLAN verbinden
- Rot blinkende stations LED
  => Fehler, bald Reset + Neustart

### Common Issues:
- **No WiFi connection**: Check `settings.toml` for correct SSID/password
- **LED strip not working**: Verify pin connections and power supply
- **Wrong tram data**: Adjust `STOP_ID` in `settings.py` using `what-is-my-stop-id.sh`

### Selbst anpassen?
Normal sollte alles Notwendige in [`settings.py`](pi-pico-w/settings.py) und `settings.toml` anpassbar sein.  
Gerne auch in [`code.py`](pi-pico-w/code.py) vorbeischauen, oder Farben in [`colors.py`](pi-pico-w/colors.py) anpassen ;) 

## wie geht des?

1. Daten von der Station z.B. Wertachbrücke abrufen - kleines PHP Script
2. Raspberry Pico W - ruft das ab
3. Anzeige auf einem NeoPixel Streifen

## stark inspiriert an:
https://github.com/KidsLabDe/kidslab-tram  
Danke @KingBBQ

## TODOs:
- api key?