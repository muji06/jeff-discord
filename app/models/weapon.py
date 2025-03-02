import json
from typing import dict, List, Any, Optional, Union

class Attack:
    """Represents a weapon attack with its properties"""
    
    def __init__(self, attack_data: dict[str, Any]):
        # Common attack properties
        self.attack_name = attack_data.get("AttackName")
        self.crit_chance = attack_data.get("CritChance")
        self.crit_multiplier = attack_data.get("CritMultiplier")
        self.damage = attack_data.get("Damage", {})
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
        
    def __str__(self) -> str:
        return f"{self.attack_name} (Crit: {self.crit_chance}, Status: {self.status_chance})"


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
        self.disposition = weapon_data.get("Disposition")
        self.sell_price = weapon_data.get("SellPrice")
        self.introduced = weapon_data.get("Introduced")
        self.conclave = weapon_data.get("Conclave", False)
        self.traits = weapon_data.get("Traits", [])
        self.polarities = weapon_data.get("Polarities", [])
        
        # Process attacks
        self.attacks = [Attack(attack) for attack in weapon_data.get("Attacks", [])]
        
    def __str__(self) -> str:
        return f"{self.name} ({self.class_})"
    
    @classmethod
    def from_dict(cls, name:str, data: dict[str, Any]) -> dict[str, 'Weapon']:
        """Create weapon objects from dict data"""
        weapon_slot = data.get("Slot", "")
        if weapon_slot == "Primary" or weapon_slot == "Secondary":
            return RangedWeapon(name, data)
        elif weapon_slot == "Melee":
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
            description += "**Zoom**:\n"
            description += '\n'.join([str(zoom_option) for zoom_option in self.zoom])
            description += '\n'
            
        return description

class MeleeWeapon(Weapon):
    """Class for melee weapons"""
    
    def __init__(self, name: str, weapon_data: dict[str, Any]):
        super().__init__(name, weapon_data)
        
        # Melee weapon specific attributes
        self.block_angle = weapon_data.get("BlockAngle")
        self.combo_dur = weapon_data.get("ComboDur")
        self.follow_through = weapon_data.get("FollowThrough")
        self.melee_range = weapon_data.get("MeleeRange")
        self.stance_polarity = weapon_data.get("StancePolarity")
        self.sweep_radius = weapon_data.get("SweepRadius")
        self.wind_up = weapon_data.get("WindUp")
        
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
        description += f"Range: {self.melee_range}\n"
        
        return description