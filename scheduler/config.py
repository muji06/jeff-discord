
FIRST_WEEK = 1682899200

ROTATIONS = [
    ["Braton", "Lato", "Skana", "Paris", "Kunai"],
    ["Bo", "Latron", "Furis", "Furax", "Strun"],
    ["Lex", "Magistar", "Boltor", "Bronco", "Ceramic Dagger"],
    ["Torid", "Dual Toxocyst", "Dual Ichor", "Miter", "Atomos"],
    ["Arc & Brunt", "Soma", "Vasto", "Nami Solo", "Burston"],
    ["Zylok", "Sibear", "Dread", "Despair", "Hate"]
]

DOWNLOAD_URLS = {
    "void:1": "https://wf.snekw.com/void-wiki",
    "weapon:1": "https://wf.snekw.com/weapons-wiki",
    # "arcane:1": "https://wf.snekw.com/arcane-wiki",
    "mod:1": "https://wf.snekw.com/mods-wiki",
}


NEW_DOWNLOAD_URLS = {
    "arcane:2": "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AArcane&content=return%20require(%27Module%3ALuaSerializer%27)._serialize(%27Arcane%2Fdata%27)&question=%3Dp&clear=1",
    "weapon:2": "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AWeapons&content=return%20require(%27Module%3ALuaSerializer%27)._serialize(%27Weapons%2Fdata%27)&question=%3Dp&clear=1",
    "void:2":  "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AVoid&content=return%20require(%27Module%3ALuaSerializer%27)._serialize(%27Void%2Fdata%27)&question=%3Dp&clear=1",
    "mod:2":   "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AMods&content=return%20require(%27Module%3ALuaSerializer%27)._serialize(%27Mods%2Fdata%27)&question=%3Dp&clear=1",
}  

CHECKSUMS = {
    "arcane:2": "arcane:checksum:1",
    "weapon:2": "weapon:checksum:1",
    "mod:2": "mod:checksum:1",
    "void:2": "void:checksum:1",
}