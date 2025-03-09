import json
from typing import Any
from dataclasses import dataclass

@dataclass
class Slot:
    """What slot the weapon occupies"""
    PRIMARY = "Primary"
    SECONDARY = "Secondary"
    MELEE = "Melee"
    AMP = "Amp"
    # Archguns when used in space
    ARCHGUN = "Archgun"
    # Archguns when summoned
    ARCHGUN_ATMOSPHERE = "Archgun (Atmosphere)"
    ARCHMELEE = "Archmelee"
    # Rampart, used by grineer
    EMPLACEMENT = "Emplacement"
    # Fishing spears
    GEAR = "Gear"
    HOUND = "Hound"
    # Pugil (unarmed)
    NECH_MELEE = "Nech-Melee"
    RAILJACK_ORDNANCE = "Railjack Ordnance"
    RAILJACK_TURRET = "Railjack Turret"
    ROBOTIC = "Robotic"
    # Parazon, Razorflies, Soaktron, Unarmed
    UNIQUE = "Unique"
    # Dargyn
    VEHICLE = "Vehicle"


@dataclass
class ShotType:
    """The type of shot the attack uses"""
    AOE = ("AoE")
    DOT = ("DoT")
    HIT_SCAN = ("Hit-Scan","Hitscan")
    PROJECTILE = ("Projectile")
    THROWN = ("Thrown")


class Damage:
    """Represents damage attributes of an attack"""
    emote ={
        #TODO: Add the actual emotes
        "impact": "<:Impact:891464869494646036>",
        "puncture": "<:Puncture:891464869494646036>",
        "slash": "<:Slash:891464869494646036>",
        "heat": "<:Heat:891464869494646036>",
        "cold": "<:Cold:891464869494646036>",
        "electricity": "<:Electricity:891464869494646036>",
        "toxin": "<:Toxin:891464869494646036>",
        "blast": "<:Blast:891464869494646036>",
        "corrosive": "<:Corrosive:891464869494646036>",
        "gas": "<:Gas:891464869494646036>",
        "magnetic": "<:Magnetic:891464869494646036>",
        "radiation": "<:Radiation:891464869494646036>",
        "viral": "<:Viral:891464869494646036>",
        "void": "<:Void:891464869494646036>"
    }
    
    def __init__(self, damage_data: dict[str, float]):
        # Physical types
        self.impact = damage_data.get("Impact")
        self.puncture = damage_data.get("Puncture")
        self.slash = damage_data.get("Slash")

        # Single element types
        self.heat = damage_data.get("Heat")
        self.cold = damage_data.get("Cold")
        self.electricity = damage_data.get("Electricity")
        self.toxin = damage_data.get("Toxin")

        # Combined element types
        self.blast = damage_data.get("Blast")
        self.corrosive = damage_data.get("Corrosive")
        self.gas = damage_data.get("Gas")
        self.magnetic = damage_data.get("Magnetic")
        self.radiation = damage_data.get("Radiation")
        self.viral = damage_data.get("Viral")

        # Special damage types
        self.void = damage_data.get("Void")

    @property
    def used(self) -> dict[str, float]:
        """Return the damage types used in the attack"""
        return {key:value for key, value in self.__dict__.items() if value is not None}
    
    @property
    def total(self) -> float:
        """Calculate the total damage of an attack"""
        return sum(self.used.values())
    
    @property
    def most_used(self) -> tuple[str, float]:
        """Return the most used damage type in the attack and its percentage

        Returns:
            tuple[str, float]: The most used damage type and its percentage
        """
        if not self.used:
            raise ValueError("No damage types found")
        damage_type = max(self.used, key=self.used.get)
        percentage = self.used[damage_type]/self.total * 100
        return damage_type, percentage
    
    def __str__(self) -> str:
        damage_text = ""
        damage_text += "- " + "\n- ".join([f"{key.capitalize()}: {value}" for key, value in self.used.items()])

        most_used_type, most_used_percent = self.most_used
        damage_text += f"\n\nTotal: {round(self.total,2)} ({round(most_used_percent,2)}%{most_used_type.capitalize()})"
        return damage_text


class Attack:
    """Represents a weapon attack with its properties"""
    
    def __init__(self, attack_data: dict[str, Any]):
        # Common attack properties
        self.attack_name = attack_data.get("AttackName", "Normal Attack")
        self.crit_chance = attack_data.get("CritChance")
        self.crit_multiplier = attack_data.get("CritMultiplier")
        self.damage = Damage(attack_data.get("Damage", {}))
        self.fire_rate = attack_data.get("FireRate")
        self.is_silent = attack_data.get("IsSilent", False)
        self.status_chance = attack_data.get("StatusChance")
        self.multishot = attack_data.get("Multishot")
        
        # Ranged attack properties
        self.ammo_cost = attack_data.get("AmmoCost")
        self.punch_through = attack_data.get("PunchThrough")
        self.shot_type = attack_data.get("ShotType")
        self.shot_speed = attack_data.get("ShotSpeed")
        self.max_spread = attack_data.get("MaxSpread")
        self.min_spread = attack_data.get("MinSpread")
        self.accuracy = attack_data.get("Accuracy")
        
        # AoE properties
        self.range = attack_data.get("Range")
        self.falloff = attack_data.get("Falloff")
        
        # Special properties
        self.forced_procs = attack_data.get("ForcedProcs", [])
        self.charge_time = attack_data.get("ChargeTime")
        self.trigger = attack_data.get("Trigger")
    
    def __repr__(self):
        return f"<Attack: {self.attack_name}-{self.shot_type}>"
    
    @property
    def parsed_falloff(self) -> str:
        """Return the parsed falloff range"""
        if self.falloff:
            if 'Reduction' in self.falloff:
                return f"{str(round(self.falloff['Reduction'] * 100))}% ({self.falloff['StartRange']} - {self.falloff['EndRange']}m)"
        return None
    
    @property
    def important_properties(self) -> dict[str, Any]:
        """Return the important properties of the attack"""
        dictionary = {}
        dictionary["Crit Chance"]= f"{self.crit_chance * 100}%"
        dictionary["Crit Multiplier"]= f"{self.crit_multiplier}x"
        dictionary["Status Chance"]= f"{round(self.status_chance * 100, 2)}%"

        if self.shot_type != "Normal Attack":
            dictionary["Multishot"]= self.multishot
            dictionary["Fire Rate"]= self.fire_rate

        if self.range:
            if self.shot_type == "AoE":
                dictionary["AoE Radius"]= f"{self.range}m"
            else:
                dictionary["Range"]= f"{self.range}m"

        if self.parsed_falloff:
            dictionary["Falloff"]= self.parsed_falloff,
        dictionary["**Damage**"] = f"\n{str(self.damage)}"

        return dictionary

    @property
    def title(self):
        text = f"***Attack Mode***: {self.attack_name}"
        if self.shot_type:
            text += f"\n***Type***: {self.shot_type}"
        return text
    
    def __str__(self):
        text = ""
        for key, value in self.important_properties.items():
            if value is not None:
                text += f"{key}: {value}\n"
        return text
    

class Weapon:
    """Base class for all weapons"""
    
    def __init__(self, name: str, weapon_data: dict[str, Any]):
        # Basic identification
        self.name = name
        self.internal_name = weapon_data.get("InternalName")
        self.link = weapon_data.get("Link")
        self.image = weapon_data.get("Image")
        
        # Common attributes
        self.slot = weapon_data.get("Slot")
        self.class_ = weapon_data.get("Class")
        self.family = weapon_data.get("Family")
        self.mastery = weapon_data.get("Mastery")
        self.max_rank = weapon_data.get("MaxRank", 30)
        self.disposition = self.parse_disposition(weapon_data.get("Disposition", 0.5))
        self.sell_price = weapon_data.get("SellPrice")
        self.introduced = weapon_data.get("Introduced")
        self.conclave = weapon_data.get("Conclave", False)
        self.traits = weapon_data.get("Traits", [])
        self.polarities = weapon_data.get("Polarities", [])
        
        # Process attacks
        self.attacks = [Attack(attack) for attack in weapon_data.get("Attacks", [])]
        
    def __str__(self) -> str:
        return f"{self.name} ({self.class_})"
    
    def parse_disposition(self, disposition: float) -> str:
        """Parse disposition value to a string"""
        if disposition >= 0.5 and disposition <=0.69:
            return '●○○○○'
        elif disposition >= 0.7 and disposition <=0.89:
            return '●●○○○'
        elif disposition >= 0.9 and disposition <=1.1:
            return '●●●○○'
        elif disposition >= 1.11 and disposition <=1.3:
            return '●●●●○'
        elif disposition >= 1.31 and disposition <=1.55:
            return '●●●●●'

    @classmethod
    def from_dict(cls, name:str, data: dict[str, Any]) -> 'Weapon':
        """Create weapon objects from dict data"""
        weapon_slot = data.get("Slot", "")
        if weapon_slot == Slot.PRIMARY or weapon_slot == Slot.SECONDARY:
            return RangedWeapon(name, data)
        elif weapon_slot == Slot.MELEE:
            return MeleeWeapon(name, data)
        else:
            return Weapon(name, data)

    def get_description(self) -> str:
        """Returns a formatted description of the weapon"""
        description = ""
        # Common weapon information
        description += f"Class: {self.slot}\n"
        description += f"Type: {self.class_}\n"
        description += f"Mastery: {self.mastery if self.mastery is not None else '-'}\n"
        description += f"Disposition: {self.disposition}\n"

        return description
    
    
class RangedWeapon(Weapon):
    """Class for ranged weapons (Primary and Secondary)"""
    
    def __init__(self, name: str, weapon_data: dict[str, Any]):
        super().__init__(name, weapon_data)
        
        # Ranged weapon specific attributes
        self.accuracy = weapon_data.get("Accuracy")
        self.ammo_max = weapon_data.get("AmmoMax")
        self.ammo_pickup = weapon_data.get("AmmoPickup")
        self.ammo_type = weapon_data.get("AmmoType")
        self.magazine = weapon_data.get("Magazine")
        self.reload = weapon_data.get("Reload")
        self.trigger = weapon_data.get("Trigger")
        self.exilus_polarity = weapon_data.get("ExilusPolarity")
        self.tradable = weapon_data.get("Tradable")

    def get_description(self) -> str:
        """Returns a formatted description of the ranged weapon"""
        description = super().get_description()
        
        # Add ranged weapon specific info
        description += f"Ammo: {self.ammo_max if self.ammo_max is not None else '∞'}\n"
        if self.ammo_pickup is not None:
            description += f"Ammo Pickup: {self.ammo_pickup}\n"
        description += f"Magazine: {self.magazine}\n"
        description += f"Reload: {self.reload}\n"
        description += f"Trigger: {self.trigger}\n"
        
        # Handle zoom options if present
        if hasattr(self, 'zoom') and self.zoom:
            description += "**Zoom**:\n- "
            description += '\n- '.join([str(zoom_option) for zoom_option in self.zoom])
            description += '\n'
            
        return description


class MeleeWeapon(Weapon):
    """Class for melee weapons"""
    
    def __init__(self, name: str, weapon_data: dict[str, Any]):
        super().__init__(name, weapon_data)
        
        # Melee weapon specific attributes
        self.block_angle = weapon_data.get("BlockAngle")
        self.combo_dur = weapon_data.get("ComboDur", "∞")
        self.follow_through = weapon_data.get("FollowThrough")
        self.melee_range = weapon_data.get("MeleeRange")
        self.stance_polarity = weapon_data.get("StancePolarity")
        self.sweep_radius = weapon_data.get("SweepRadius")
        self.wind_up = weapon_data.get("WindUp")

        # Derived from attack
        self.attack_speed = self.attacks[0].fire_rate
        
        # Special attacks
        self.heavy_attack = weapon_data.get("HeavyAttack")
        self.slam_attack = weapon_data.get("SlamAttack")
        self.heavy_slam_attack = weapon_data.get("HeavySlamAttack")
        self.slide_attack = weapon_data.get("SlideAttack")
        
        # Special attack properties
        self.slam_element = weapon_data.get("SlamElement")
        self.slam_radius = weapon_data.get("SlamRadius")
        self.slam_forced_procs = weapon_data.get("SlamForcedProcs", [])
        self.heavy_slam_element = weapon_data.get("HeavySlamElement")
        self.heavy_slam_radius = weapon_data.get("HeavySlamRadius")
        self.heavy_slam_forced_procs = weapon_data.get("HeavySlamForcedProcs", [])


    def get_description(self) -> str:
        """Returns a formatted description of the melee weapon"""
        description = super().get_description()
        
        # Add melee weapon specific info
        if self.block_angle is not None:
            description += f"Block Angle: {self.block_angle}\n"
        description += f"Combo Duration: {self.combo_dur}\n"
        description += f"Follow Through: {self.follow_through}\n"
        description += f"Attack Speed: {self.attack_speed}\n"
        description += f"Range: {self.melee_range}m\n"
        
        return description