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

## warum?

weils oft pressiert, und man nicht immer auf das handy schauen will!

## was zeigts an?
- Anzeige in Minuten für die nächste Tram
- Rot = Linie 4
- Blau = Linie 2
- Mitte = Wertachbrücke
- Alle Lichter representieren Trams
    - Wandern zur mitte
    - Abstand 5 LEDs = in 5 Minuten fährt die tram an der Wertachbrücke ab

## Selbst anpassen?
Wlan in `settings.toml` auf raspi pico w speichern  
Libraries kopieren  
`color.py`, `code.py` und `settings.py` auf pico copieren    
`settings.py` auf neuen Bedarf anpassen  

## wie geht des?

1. Daten von der Station Wertachbrücke abrufen - kleines PHP Script
2. Raspberry Pico W - ruft das ab
3. Anzeige auf einem 31-Pixel NeoPixel Streifen

## stark inspiriert an:
https://github.com/KidsLabDe/kidslab-tram
Danke @KingBBQ

