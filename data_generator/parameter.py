"""
OMOP Vocabulary Concepts
"""
import datetime

import numpy as np

from omop import concepts

BIRTHYEAR_RANGE = range(1920, 2003)

# regarding visits, creating a list of all dates from 2020 and 2021
VISIT_START_DATE = datetime.date(2020, 1, 1)
VISIT_END_DATE = datetime.date(2021, 12, 31)


# regarding person
GENDER_LIST = {
    concepts.GENDER_FEMALE: "Female",
    concepts.GENDER_MALE: "Male",
    concepts.UNKNOWN: "Unknown",
}

# regarding diagnoses and treatment
VENTILATION_BIN = {
    concepts.ARTIFICIAL_RESPIRATION: "Artificial respiration",
    concepts.OXYGEN_THERAPY: "Oxygen therapy",
}
PRONE_BIN = {
    concepts.PRONE_POSITIONING: "Placing subject in prone position",
}

CONDITION_LIST = {
    concepts.COVID19: "COVID-19",
    concepts.VENOUS_THROMBOSIS: "Venous thrombosis",
    concepts.HEPARIN_INDUCED_THROMBOCYTOPENIA_WITH_THROMBOSIS: "Heparin-induced thrombocytopenia with thrombosis",
    concepts.THROMBOCYTOPENIA: "Thrombocytopenic disorder",
    concepts.PULMONARY_EMBOLISM: "Pulmonary embolism",
    concepts.ARDS: "Acute respiratory distress syndrome",
}

OBSERVATION_LIST = {
    concepts.ALLERGY_HEPARIN: "Allergy to heparin",
    concepts.ALLERGY_HEPARINOID: "Allergy to heparinoid",
}

LABORATORY_LIST = {
    concepts.LAB_DDIMER: "Fibrin D-dimer DDU [Mass/volume] in Platelet poor plasma",
    concepts.LAB_APTT: "aPTT in Blood by Coagulation assay",
    concepts.LAB_HOROWITZ: "Horowitz index in Arterial blood",
}

VENTILATION_LIST = {
    concepts.INHALED_OXYGEN_CONCENTRATION: "Inhaled oxygen concentration",
    concepts.TIDAL_VOLUME: "Tidal volume.spontaneous+mechanical/Body weight [Volume/mass] --on ventilator",
    concepts.PRESSURE_MAX: "Pressure max Respiratory system airway --during inspiration",
    concepts.PEEP: "PEEP Respiratory system --on ventilator",
}

DRUG_LIST = {
    concepts.HEPARIN: "heparin",
    concepts.ARGATROBAN: "argatroban",
    concepts.DALTEPARIN: "dalteparin",
    concepts.ENOXAPARIN: "enoxaparin",
    concepts.NADROPARIN: "nadroparin",
    concepts.CERTOPARIN: "certoparin",
    concepts.FONDAPARINUX: "fondaparinux",
}

VISIT_CONCEPTS = {
    concepts.INPATIENT_VISIT: "Inpatient visit",
    concepts.INTENSIVE_CARE: "Intensive care",
}

VENTILATION_PARAMS = {
    concepts.ARTIFICIAL_RESPIRATION: {
        concepts.INHALED_OXYGEN_CONCENTRATION: {
            "unit": concepts.UNIT_PERCENT,
            "value": np.arange(0.2, 1.0, 0.05),
        },
        concepts.TIDAL_VOLUME: {"unit": concepts.UNIT_ML_PER_KG, "value": range(1, 12)},
        concepts.PRESSURE_MAX: {"unit": concepts.UNIT_CM_H2O, "value": range(12, 40)},
        concepts.PEEP: {"unit": concepts.UNIT_CM_H2O, "value": range(12, 40)},
    },
    concepts.OXYGEN_THERAPY: {
        concepts.INHALED_OXYGEN_CONCENTRATION: {
            "unit": concepts.UNIT_PERCENT,
            "value": np.arange(0.2, 0.5, 0.05),
        }
    },
}
