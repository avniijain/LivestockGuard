DISEASE_BASE_PRIORS = {
    "Brucellosis": {"base": 0.12, "milk_multiplier": 2.5, "wound_multiplier": 2.2, "child_multiplier": 1.8},
    "Leptospirosis": {"base": 0.10, "milk_multiplier": 1.2, "wound_multiplier": 3.0, "child_multiplier": 1.5},
    "Bovine_TB": {"base": 0.05, "milk_multiplier": 2.0, "wound_multiplier": 1.5, "child_multiplier": 2.5},
    "Anthrax": {"base": 0.20, "milk_multiplier": 1.5, "wound_multiplier": 4.0, "child_multiplier": 2.0},
    "Q_Fever": {"base": 0.08, "milk_multiplier": 1.8, "wound_multiplier": 1.3, "child_multiplier": 1.6},
    "LSD": {"base": 0.02, "milk_multiplier": 1.0, "wound_multiplier": 1.5, "child_multiplier": 1.2},
    "FMD": {"base": 0.03, "milk_multiplier": 1.3, "wound_multiplier": 2.0, "child_multiplier": 1.4},
    "Ringworm": {"base": 0.30, "milk_multiplier": 1.0, "wound_multiplier": 1.8, "child_multiplier": 1.5},
}

TRANSMISSION_ROUTES = {
    "Brucellosis": {
        "primary": "Raw milk or unpasteurised dairy",
        "secondary": "Contact with birth fluids or aborted fetuses",
    },
    "Leptospirosis": {
        "primary": "Contact with urine-contaminated water or soil",
        "secondary": "Open wound contact with infected tissue",
    },
    "Bovine_TB": {"primary": "Inhaling airborne droplets near infected cow", "secondary": "Drinking raw milk"},
    "Anthrax": {
        "primary": "Skin contact with infected animal tissue or carcass",
        "secondary": "Inhaling spores near a carcass",
    },
    "Q_Fever": {"primary": "Inhaling dust or particles from birth fluids", "secondary": "Raw milk consumption"},
    "LSD": {
        "primary": "Not directly transmissible to humans",
        "secondary": "Insect bite from vector on infected cow (rare)",
    },
    "FMD": {"primary": "Direct contact with blisters or saliva", "secondary": "Raw milk from infected cow"},
    "Ringworm": {
        "primary": "Direct skin contact with infected animal",
        "secondary": "Contact with contaminated bedding or equipment",
    },
}

HOUSEHOLD_RISK_GROUPS = {
    "Brucellosis": ["Pregnant women (risk of miscarriage)", "Children under 10"],
    "Bovine_TB": ["Elderly", "Immunocompromised individuals", "Children under 5"],
    "Anthrax": ["Anyone with open wounds or cuts"],
    "Ringworm": ["Children under 10", "Immunocompromised individuals"],
    "Leptospirosis": ["Anyone with open wounds", "Farmers wading in water"],
    "Q_Fever": ["Pregnant women (risk of miscarriage)", "Elderly"],
    "FMD": ["Immunocompromised individuals"],
    "LSD": [],
}

