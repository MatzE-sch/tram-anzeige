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
    - Wandern zur mitte
    - Abstand 5 LEDs = in 5 Minuten fährt die tram an der Wertachbrücke ab

## Benötigte Hardware
- Raspberry Pi Pico W
- LED-Streifen, einzel addressierbar (WS2812b)
- n paar käbelchen zum anlöten
- micro usb Kabel
- Stromquelle
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
- switch colors when trams overlap in same pixel
- add daylightsensor ;)
- better boot animation?
- richtung über gleis bestimmen
