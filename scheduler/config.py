
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

# Pulled from warframe wiki fandom page
NEW_DOWNLOAD_URLS = {
    "ability:2" : "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AAbility&content=return%20require(%27Module%3ALuaSerializer%27)._serialize(%27Ability%2Fdata%27)&question=%3Dp&clear=1",
    "arcane:2": "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AArcane&content=return%20require(%27Module%3ALuaSerializer%27)._serialize(%27Arcane%2Fdata%27)&question=%3Dp&clear=1",
    "blueprint:2" : "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3ABlueprints&content=return%20require('Module%3ALuaSerializer')._serialize('Blueprints%2Fdata')&question=%3Dp&clear=1",
    "companion:2" : "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3ACompanions&content=return%20require('Module%3ALuaSerializer')._serialize('Companions%2Fdata')&question=%3Dp&clear=1",
    "enemy:2" : "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AEnemies&content=return%20require('Module%3ALuaSerializer')._serialize('Enemies%2Fdata')&question=%3Dp&clear=1",
    "mod:2":   "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AMods&content=return%20require(%27Module%3ALuaSerializer%27)._serialize(%27Mods%2Fdata%27)&question=%3Dp&clear=1",
    "tennogen:2" : "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3ATennoGen&content=return%20require('Module%3ALuaSerializer')._serialize('TennoGen%2Fdata')&question=%3Dp&clear=1",
    "void:2":  "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AVoid&content=return%20require(%27Module%3ALuaSerializer%27)._serialize(%27Void%2Fdata%27)&question=%3Dp&clear=1",
    "warframe:2" : "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AWarframes&content=return%20require('Module%3ALuaSerializer')._serialize('Warframes%2Fdata')&question=%3Dp&clear=1",
    "weapon:2": "https://warframe.fandom.com/api.php?action=scribunto-console&format=json&title=Module%3AWeapons&content=return%20require(%27Module%3ALuaSerializer%27)._serialize(%27Weapons%2Fdata%27)&question=%3Dp&clear=1",
}  

NEW_WIKI_URL_BASE = "https://wiki.warframe.com/api.php"
NEW_WIKI_MODULE_URLS = {
    "ability:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Ability",
        "content": "return require('Module:Ability/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
    "arcane:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Arcane",
        "content": "return require('Module:Arcane/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
    "blueprint:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Blueprints",
        "content": "return require('Module:Blueprints/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
    "companion:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Companions",
        "content": "return require('Module:Companions/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
    "enemy:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Enemies",
        "content": "return require('Module:Enemies/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
    "mod:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Mods",
        "content": "return require('Module:Mods/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
    "tennogen:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:TennoGen",
        "content": "return require('Module:TennoGen/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
    "void:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Void",
        "content": "return require('Module:Void/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
    "warframe:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Warframes",
        "content": "return require('Module:Warframes/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
    "weapon:3": {
        "action": "scribunto-console",
        "format": "json",
        "title": "Module:Weapons",
        "content": "return require('Module:Weapons/data')",
        "question": "=p",
        "clear": 1,
        "token": "+\\",
        "formatversion": "2"
    },
}
# Pulled from community developer github repo
WFCD = {
    "skins:2" : "https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/Skins.json",
}

CHECKSUMS = {
    "ability:2": "ability:checksum:1",
    "arcane:2": "arcane:checksum:1",
    "blueprint:2": "blueprint:checksum:1",
    "companion:2": "companion:checksum:1",
    "enemy:2": "enemy:checksum:1",
    "mod:2": "mod:checksum:1",
    "skins:2": "skins:checksum:1",
    "tennogen:2": "tennogen:checksum:1",
    "void:2": "void:checksum:1",
    "warframe:2": "warframe:checksum:1",
    "weapon:2": "weapon:checksum:1",
}