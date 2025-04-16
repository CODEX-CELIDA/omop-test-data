"""
Parameter configuration for data generation.
"""
import datetime
from typing import Callable, Final, TypedDict

import numpy as np

from omop import concepts

BIRTHYEAR_RANGE = range(1920, 2003)

# regarding visits, creating a list of all dates from 2020 and 2021
VISIT_START_DATE = datetime.datetime.today() - datetime.timedelta(
    days=7
)  # datetime.date(2020, 1, 1)
VISIT_END_DATE = datetime.datetime.today()  # datetime.date(2021, 12, 31)


# regarding person
GENDER_LIST = {
    concepts.GENDER_FEMALE: "Female",
    concepts.GENDER_MALE: "Male",
}


class ParameterGenerator(TypedDict):
    """
    Helper class for type hinting a dictionary that contains
    name, unit and a function to generate a random value.
    """

    name: str
    unit: int
    sample_func: Callable


WEIGHT: dict[int, dict[int, ParameterGenerator]] = {
    concepts.GENDER_MALE: {
        concepts.WEIGHT: {
            "name": "Weight",
            "unit": concepts.UNIT_KG,
            "sample_func": lambda: np.random.normal(loc=100, scale=15),
        },
        concepts.IDEAL_BODY_WEIGHT: {
            "name": "Ideal Body Weight",
            "unit": concepts.UNIT_KG,
            "sample_func": lambda: np.random.normal(loc=80, scale=5),
        },
    },
    concepts.GENDER_FEMALE: {
        concepts.WEIGHT: {
            "name": "Weight",
            "unit": concepts.UNIT_KG,
            "sample_func": lambda: np.random.normal(loc=80, scale=15),
        },
        concepts.IDEAL_BODY_WEIGHT: {
            "name": "Ideal Body Weight",
            "unit": concepts.UNIT_KG,
            "sample_func": lambda: np.random.normal(loc=60, scale=5),
        },
    },
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
    concepts.LAB_DDIMER: {
        "name": "Fibrin D-dimer DDU [Mass/volume] in Platelet poor plasma",
        "unit": concepts.UNIT_UG_PER_L,
        "sample_func": lambda: np.random.binomial(40, 0.45) / 10,
    },
    concepts.LAB_APTT: {
        "name": "aPTT in Blood by Coagulation assay",
        "unit": concepts.UNIT_SECOND,
        "sample_func": lambda: np.random.normal(loc=50, scale=10),
    },
    concepts.LAB_HOROWITZ: {
        "name": "Horowitz index in Arterial blood",
        "unit": concepts.UNIT_MM_HG,
        "sample_func": lambda: np.random.normal(loc=200, scale=50),
    },
}


VENTILATION_LIST = {
    concepts.INHALED_OXYGEN_CONCENTRATION: "Inhaled oxygen concentration",
    concepts.TIDAL_VOLUME: "Tidal volume Ventilator --on ventilator",
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
            "value": np.arange(20.0, 100.0, 5.0),
        },
        concepts.TIDAL_VOLUME: {"unit": concepts.UNIT_ML, "value": range(200, 1200)},
        concepts.PRESSURE_MAX: {"unit": concepts.UNIT_CM_H2O, "value": range(12, 40)},
        concepts.PEEP: {"unit": concepts.UNIT_CM_H2O, "value": range(12, 40)},
    },
    concepts.OXYGEN_THERAPY: {
        concepts.INHALED_OXYGEN_CONCENTRATION: {
            "unit": concepts.UNIT_PERCENT,
            "value": np.arange(20.0, 50.0, 5.0),
        }
    },
}
COND_WEIGHTS: Final = [0.3, 0.1, 0.05, 0.15, 0.15, 0.25]
OBS_WEIGHTS: Final = [0.7, 0.3]
