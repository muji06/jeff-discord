# WORK IN PROGRESS
# I am updating this every week as I get more information

SEASON = {
    "CST_WINTER": "Winter",
    "CST_SPRING": "Spring",
    "CST_SUMMER": "Summer",
    "CST_FALL": "Fall",
}

EVENTS = {
    "CET_CHALLENGE": {
        "name": "TO DO",
        "key": "challenge",
        "mappings": [
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarKillEximusEasy",
                "name": "EX-EXIMUS",
                "description": "Kill 10 Eximus",
            },
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarKillScaldraEnemiesEasy",
                "name": "PUNISH SCALDRA",
                "description": "Kill 250 Scaldra Troops",
            },
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarKillEnemiesWithAbilitiesMedium",
                "name": "DEMONSTRATION OF POWER",
                "description": "Kill 300 Enemies with Abilities",
            },
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarKillScaldraEnemiesWithMeleeMedium",
                "name": "MAKE IT PERSONAL",
                "description": "Kill 300 Scaldra Troops with Melee Weapons",
            },
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarKillTechrotEnemiesHard",
                "name": "PURGE THE INFECTION",
                "description": "Kill 1,000 Techrot",
            },
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarDestroyPropsMedium",
                "name": "STARVE THE BEAST",
                "description": "Destroy 150 Containers",
            },
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarKillTechrotEnemiesWithMeleeMedium",
                "name": "ELECTRONIC WASTE DISPOSAL",
                "description": "Kill 300 Techrot with Melee Weapons",
            },
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarKillScaldraEnemiesWithAbilitiesHard",
                "name": "SHOCK AND AWE",
                "description": "Kill 500 Scaldra Troops with Abilities",
            },
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarDestroyPropsHard",
                "name": "STARVE THE BEAST",
                "description": "Destroy 300 Containers",
            },
            {
                "uniqueName": "/Lotus/Types/Challenges/Calendar1999/CalendarKillTechrotEnemiesEasy",
                "name": "PURGE THE INFECTION",
                "description": "Kill 250 Techrot",
            }
        ]
    },
    "CET_UPGRADE": {
        "name": "OVERRIDE",
        "key": "upgrade",
        "mappings": [
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/MagazineCapacity",
                "name": "Heavy Mags",
                "description": "Increase magazine capacity by 25%",
                "for": "",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/Armor",
                "name": "Thick Skin",
                "description": "Gain +250 Armor",
                "for": "",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/EnergyRestoration",
                "name": "Espresso Shots",
                "description": "Increase energy restoration by 2/s",
                "for": "Lettie",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/CompanionsBuffNearbyPlayer",
                "name": "More the Merrier",
                "description": "Non-Tenno Allies within 20m gain +5% Attack Speed and +20% Fire Rate for each one in range",
                "for": "",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/OrbsDuplicateOnPickup",
                "name": "Targeted Medicine",
                "description": "Shoot Health Orbs to pick them up. 25% chance to duplicate on pickup",
                "for": "",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/FinisherChancePerComboMultiplier",
                "name": "Combo Killer",
                "description": "Increase chance that enemies are open to finishers, 5% per combo",
                "for": "Arthur",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/EnergyOrbToAbilityRange",
                "name": "Broadened Horizons",
                "description": "Increase Ability Range by 10% for 10s after picking up an Energy Orb",
                "for": "Aoi",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/MeleeAttackSpeed",
                "name": "No Quarter",
                "description": "+25 Attack Speed",
                "for": "Arthur",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/CompanionDamage",
                "name": "Got your Back",
                "description": "Specters and Companions gain +250% Damage",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/ElectricStatusDamageAndChance",
                "name": "Bottled Lightning",
                "description": "+25% electric to all weapons. +25% Status Damage",
                "for": "Amir",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/BlastEveryXShots",
                "name": "Have a Blast",
                "description": "Every 10th shot applies 10x Blast stacks",
                "for": "Quincy",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/MagnitizeWithinRangeEveryXCasts",
                "name": "Magnetic Menace",
                "description": "Every 5th ability cast applies magnetic status to an enemy within 50m",
                "for": "Aoi",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/GenerateOmniOrbsOnWeakKill",
                "name": "Involuntary Transfusion",
                "description": "+25% chance to generate universal orb from weakpoint kills",
                "for": "Lettie",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/GasChanceToPrimaryAndSecondary",
                "name": "Toxic Shot",
                "description": "+25% Gas status chance to Primary and Secondary weapons",
                "for": "Quincy",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/AbilityStrength",
                "name": "Power Gains",
                "description": "+25% ability strength",
                "for": "Aoi",
            },
            {
                "uniqueName": "/Lotus/Upgrades/Calendar/MeleeCritChance",
                "name": "Practiced Precision",
                "description": "+20% melee crit chance",
                "for": "Arthur",
            }
        ]
    },
    "CET_REWARD": {
        "name": "BIG PRIZE!",
        "key": "reward",
        "mappings": [
            {
                "uniqueName": "/Lotus/StoreItems/Types/BoosterPacks/CalendarMajorArtifactPack",
                "name": "Arcane Enhancements: Double Pack",
                "description": "Receive 2 random Arcanes",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Types/Gameplay/NarmerSorties/ArchonCrystalGreen",
                "name": "Emerald Archon Shard",
                "description": "Emerald Archon Shard",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Types/Gameplay/NarmerSorties/ArchonCrystalBoreal",
                "name": "Azure Archon Shard",
                "description": "Azure Archon Shard",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Types/Recipes/Components/WeaponUtilityUnlockerBlueprint",
                "name": "Exilus Weapon Adapter Blueprint",
                "description": "Exilus Weapon Adapter Blueprint",
            },
            {
                "uniqueName": "/Lotus/Types/StoreItems/Packages/Calendar/CalendarKuvaBundleSmall",
                "name": "2000 x Kuva",
                "description": "2000 x Kuva",
            },
            {
                "uniqueName": "/Lotus/Types/StoreItems/Boosters/AffinityBooster3DayStoreItem",
                "name": "3 Day Affinity Booster",
                "description": "3 Day Affinity Booster",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Types/BoosterPacks/CalendarArtifactPack",
                "name": "Arcane Enhancements",
                "description": "Receive a random Arcane",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Types/Items/MiscItems/WeaponSecondaryArcaneUnlocker",
                "name": "Secondary Arcane Adapter",
                "description": "Secondary Arcane Adapter",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Upgrades/Mods/FusionBundles/CircuitSilverSteelPathFusionBundle",
                "name": "6000 x Endo",
                "description": "6000 x Endo",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Types/Recipes/Components/OrokinReactorBlueprint",
                "name": "Orokin Reactor Blueprint",
                "description": "Orkin Reactor Blueprint",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Types/Items/MiscItems/WeaponUtilityUnlocker",
                "name": "Exilus Weapon Adapter",
                "description": "Exilus Weapon Adapter",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Types/Items/MiscItems/WeaponMeleeArcaneUnlocker",
                "name": "Melee Arcane Adapter",
                "description": "Melee Arcane Adapter",
            },
            {
                "uniqueName": "/Lotus/StoreItems/Types/Items/MiscItems/Forma",
                "name": "Forma",
                "description": "Forma",
            },
            {
                "uniqueName": "/Lotus/Types/StoreItems/Boosters/ModDropChanceBooster3DayStoreItem",
                "name": "3 Day Mod Drop Chance Booster",
                "description": "3 Day Mod Drop Chance Booster",
            },
            {
                "uniqueName": "/Lotus/Types/StoreItems/Packages/Calendar/CalendarVosforPack",
                "name": "Vosfor Cache",
                "description": "Vosfor Cache (200)",
            }
        ]
    },
    "CET_PLOT": {
        "key": "dialogueName",
        "mappings": [
            {
                "uniqueName": "/Lotus/Types/Gameplay/1999Wf/Dialogue/LettieDialogue_rom.dialogue",
                "name": "BIRTHDAY",
                "description": "Lettie's Birthday",
            },
            {
                "uniqueName": "/Lotus/Types/Gameplay/1999Wf/Dialogue/JabirDialogue_rom.dialogue",
                "name": "BIRTHDAY",
                "description": "Amir's Birthday",
            }
        ]
    },
}