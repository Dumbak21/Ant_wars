# Ant Wars

Pro spuštění hry:
 - Stáhněte/naklonujte projekt na své zařízení
 - Vytvořte environment podle *environment.yml* (`conda create env -f ./environment.yml`)
 - Spusťte: `python *main.py*`

Pro spuštění testů spusťte `python -m pytest`

Pokud se nenahrávají mapy ujistěte se, že v *utils.py* v konstantě **MAP_URL** je správná cesta ke složce map.

*map_creator.py* můžete využít pro tvorbu dalších map.
Pokud budete pokračovat ve vzestupném číslování, můžete je i přidat do složky map a budou se automaticky ve hře nahrávat jako další v pořadí.

Rychlost hry/spawnování/mravenců si můžete změnit v *main.py* v odpovídajících konstantách.