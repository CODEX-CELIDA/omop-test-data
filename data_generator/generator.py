import datetime
import random
from typing import List, Optional, cast

import numpy as np

from data_generator import parameter as params
from data_generator.parameter import COND_WEIGHTS, OBS_WEIGHTS
from omop import concepts
from omop.tables import (
    ConditionOccurrence,
    DrugExposure,
    Measurement,
    Observation,
    Person,
    ProcedureOccurrence,
    VisitOccurrence,
    random_datetime,
)

SECONDS_PER_DAY = 86400


def create_drug_exp2(
    person_id: int, visit: VisitOccurrence, n_administrations: int
) -> List[DrugExposure]:
    """
    Create a list of drug exposures for a given visit

    n_administration: number of boluses in case of LWMH/Fondaparinux or
                      number of doserate changes in case of continuous infusions
    """
    list_of_drugs = []
    begin_drug = visit.visit_start_date + datetime.timedelta(
        days=random.choice(range(4))
    )
    end_drug = begin_drug + (random.random() * (visit.visit_end_date - begin_drug))
    #    end_drug = begin_drug + datetime.timedelta(days = random.choice(range(2,30)))
    # create dttm from date, add random number of hours to startdate midnight
    drug_exposure_start_datetime = datetime.datetime.combine(
        begin_drug, datetime.datetime.min.time()
    ) + datetime.timedelta(hours=random.choice(range(12)))

    drug_concept_id = random.choice(list(params.DRUG_LIST))

    # continuous infusion of drugs, quantity referring to [dose] / h
    if drug_concept_id in [concepts.HEPARIN, concepts.ARGATROBAN]:
        drug_exposure_end_datetime = drug_exposure_start_datetime
        for _ in range(n_administrations):
            drug_exposure_start_datetime = (
                drug_exposure_end_datetime
                + datetime.timedelta(hours=random.choice(range(2)))
            )
            drug_exposure_start_date = (
                drug_exposure_start_datetime.date()
            )  # create date from dttm
            if drug_concept_id == concepts.HEPARIN:
                quantity_h = random.choice(range(200, 900, 100))  # heparin in IE/h
            elif drug_concept_id == concepts.ARGATROBAN:
                quantity_h = random.choice(range(5, 10, 1))  # argatroban in mg/h
            drug_exposure_end_datetime = (
                drug_exposure_start_datetime
                + datetime.timedelta(hours=random.choice(range(1, 12)))
            )
            drug_exposure_end_date = drug_exposure_end_datetime.date()
            duration = drug_exposure_end_datetime - drug_exposure_start_datetime
            duration_h = duration.total_seconds() / 3600
            quantity = int(duration_h * quantity_h)

            if drug_exposure_start_date > end_drug:
                break

            list_of_drugs.append(
                DrugExposure(
                    person_id=person_id,
                    drug_concept_id=drug_concept_id,
                    drug_exposure_start_date=drug_exposure_start_date,
                    drug_exposure_start_datetime=drug_exposure_start_datetime,
                    drug_exposure_end_date=drug_exposure_end_date,
                    drug_exposure_end_datetime=drug_exposure_end_datetime,
                    quantity=quantity,
                )
            )
    elif drug_concept_id in [
        concepts.DALTEPARIN,
        concepts.NADROPARIN,
        concepts.CERTOPARIN,
        concepts.ENOXAPARIN,
        concepts.FONDAPARINUX,
    ]:
        for _ in range(n_administrations):
            drug_exposure_start_datetime += datetime.timedelta(
                hours=random.choice(range(4, 20))
            )
            drug_exposure_start_date = (
                drug_exposure_start_datetime.date()
            )  # create date from dttm
            if drug_concept_id in [concepts.DALTEPARIN, concepts.NADROPARIN]:
                quantity = random.choice(range(3000, 15000, 1000))
            elif drug_concept_id == concepts.CERTOPARIN:
                quantity = random.choice(range(1000, 4000, 500))
            elif drug_concept_id == concepts.ENOXAPARIN:
                quantity = random.choice(range(10, 120, 10))
            elif drug_concept_id == concepts.FONDAPARINUX:
                quantity = random.choice(range(1, 4, 1))
            else:
                pass
            drug_exposure_end_date = drug_exposure_start_date
            drug_exposure_end_datetime = drug_exposure_start_datetime
            if drug_exposure_start_date > end_drug:
                break

            list_of_drugs.append(
                DrugExposure(
                    person_id=person_id,
                    drug_concept_id=drug_concept_id,
                    drug_exposure_start_date=drug_exposure_start_date,
                    drug_exposure_start_datetime=drug_exposure_start_datetime,
                    drug_exposure_end_date=drug_exposure_end_date,
                    drug_exposure_end_datetime=drug_exposure_end_datetime,
                    quantity=quantity,
                )
            )
    else:
        raise ValueError(f"Unknown drug concept id {drug_concept_id}")

    return list_of_drugs


def create_vent_params_procedure(
    person_id: int, visit: VisitOccurrence
) -> Optional[ProcedureOccurrence]:
    """
    Create a list of procedures for a given visit

    Create (only one) episode of ventilation or O2 therapy for ICU patients with related parameters.
    Patients not treated on ICU do not have such parameters.
    """
    person_id = person_id

    # procedure_occurence_id = 0  # used for ventilation OR oxygen therapy at the moment
    # set different frequencies (x per day)
    # freq1 = 24  # used for high-frequency generation of ventilated patients
    # freq2 = 2  # used for non-ventilated patients
    # freq3 = 4  # unused

    if visit.visit_concept_id != concepts.INTENSIVE_CARE:
        return None

    print("- patient is treated on ICU")
    # create parameters for ventilated patients

    procedure_concept_id = random.choice(list(params.VENTILATION_BIN))
    print(f"- patient has episode of {params.VENTILATION_BIN[procedure_concept_id]}")

    procedure_type_concept_id = concepts.EHR
    begin_vent = visit.visit_start_date + datetime.timedelta(
        days=random.choice(range(3))
    )
    end_vent = begin_vent + (random.random() * (visit.visit_end_date - begin_vent))
    procedure_date = begin_vent
    procedure_datetime = random_datetime(procedure_date)
    procedure_end_date = end_vent
    procedure_end_datetime = random_datetime(procedure_end_date)

    return ProcedureOccurrence(
        person_id=person_id,
        procedure_concept_id=procedure_concept_id,
        procedure_type_concept_id=procedure_type_concept_id,
        procedure_date=procedure_date,
        procedure_datetime=procedure_datetime,
        procedure_end_date=procedure_end_date,
        procedure_end_datetime=procedure_end_datetime,
    )


def create_vent_params_measurements(
    person_id: int, prod: Optional[ProcedureOccurrence], visit: VisitOccurrence
) -> List[Measurement]:
    """
    Create (only one) episode of ventilation or O2 therapy for ICU patients with related parameters.
    Patients not treated on ICU do not have such parameters
    """
    list_of_measurements: List[Measurement] = []

    if visit.visit_concept_id != concepts.INTENSIVE_CARE:
        # patients not on ICU do not have any ventilation parameters
        # (worth discussing whether patients on normal ward can have oxygen therapy)
        return list_of_measurements

    if prod is None:
        return list_of_measurements

    # set different frequencies (x per day)
    freq = {concepts.ARTIFICIAL_RESPIRATION: 24, concepts.OXYGEN_THERAPY: 2}

    print(
        f"- patient is treated by {params.VENTILATION_BIN[prod.procedure_concept_id]}"
    )
    vent_params = params.VENTILATION_PARAMS[prod.procedure_concept_id]

    begin_vent = prod.procedure_date
    end_vent = begin_vent + (random.random() * (visit.visit_end_date - begin_vent))
    duration_vent = (end_vent - begin_vent).total_seconds() / SECONDS_PER_DAY
    for x in range(int(duration_vent)):
        base_datetime = random_datetime(begin_vent)
        begin_vent += datetime.timedelta(days=1)
        # create FiO2 values
        measurement_datetime = base_datetime  # set measurement_datetime to base

        for _ in range(freq[prod.procedure_concept_id]):
            measurement_date = measurement_datetime.date()
            measurement_datetime += datetime.timedelta(
                hours=24 / freq[prod.procedure_concept_id]
            )
            for measurement_concept_id in vent_params:

                unit_concept_id = vent_params[measurement_concept_id]["unit"]
                value_as_number = random.choice(
                    vent_params[measurement_concept_id]["value"]
                )

                list_of_measurements.append(
                    Measurement(
                        person_id=person_id,
                        measurement_concept_id=measurement_concept_id,
                        measurement_date=measurement_date,
                        measurement_datetime=measurement_datetime,
                        value_as_number=value_as_number,
                        unit_concept_id=unit_concept_id,
                    )
                )

    return list_of_measurements


def create_lab_values_measurements(
    person_id: int, visit: VisitOccurrence
) -> List[Measurement]:
    """
    Create lab values for a patient

    ideally, not done yet: if ARDS or mechanical ventilation is existent, Horowitz Index should be lower,
    because those patients are sicker
    """
    list_of_measurements = []

    # set different frequencies (x per day)
    freq_high = 4  # used for higher-frequency generation of values
    freq_low = 2  # used for less frequent generation
    freq_daily = 1  # once per day

    # set "basetime" to visit_start, i.e. generation of lab values are started up to
    # twelve hours after the start of the visit
    measurement_datetime = random_datetime(visit.visit_start_date, max_hours=12)
    measurement_date = measurement_datetime.date()

    visit_duration = visit.visit_end_date - visit.visit_start_date

    if visit.visit_concept_id == concepts.INTENSIVE_CARE:
        print("- patient is treated on ICU")
        freq = {
            concepts.LAB_HOROWITZ: freq_high,
            concepts.LAB_APTT: freq_daily,
            concepts.LAB_DDIMER: freq_daily,
        }
    elif visit.visit_concept_id == concepts.INPATIENT_VISIT:
        print("- patient is treated on normal ward")
        freq = {
            concepts.LAB_HOROWITZ: freq_low,
            concepts.LAB_APTT: freq_daily,
            concepts.LAB_DDIMER: freq_daily,
        }
    else:
        raise ValueError("visit_concept_id not recognized")

    for x in range(
        int(visit_duration.total_seconds() / SECONDS_PER_DAY)
    ):  # generate per day
        for parameter in list(params.LABORATORY_LIST):
            data = params.LABORATORY_LIST[parameter]
            for _ in range(freq[parameter]):
                measurement_date = measurement_datetime.date()
                measurement_concept_id = parameter
                measurement_type_concept_id = concepts.EHR
                # maybe here introduce if condition_concept_id ARDS/mechanical ventilation is given
                value_as_number = data["sample_func"]()  # type: ignore
                unit_concept_id = cast(int, data["unit"])

                list_of_measurements.append(
                    Measurement(
                        person_id=person_id,
                        measurement_concept_id=measurement_concept_id,
                        measurement_date=measurement_date,
                        measurement_datetime=measurement_datetime,
                        value_as_number=round(value_as_number, 0),
                        unit_concept_id=unit_concept_id,
                        measurement_type_concept_id=measurement_type_concept_id,
                    )
                )

                measurement_datetime += datetime.timedelta(hours=24 / freq[parameter])

    return list_of_measurements


def create_prone_positioning_procedure(
    person_id: int, visit: VisitOccurrence, max_occurrences: int = 5
) -> List[ProcedureOccurrence]:
    """
    Create prone positioning procedure occurrences for a patient

    ideally, not done yet: only patients who have the diagnosis ARDS and/or a Horowitz index of lower
    than 150 at least once should be placed in prone positioning
    """

    list_of_procedures = []

    r = random.random()  # roll the dice if patient is put in prone positioning
    if r >= 0.5:
        print("- patient is placed in prone positioning at least once")
        procedure_date: datetime.date = visit.visit_start_date + datetime.timedelta(
            days=random.choice(range(3))
        )  # beginning of positioning
        procedure_end_date: datetime.date = procedure_date + (
            random.random() * (visit.visit_end_date - procedure_date)
        )
        procedure_datetime = random_datetime(procedure_date)
        procedure_end_datetime = procedure_datetime + datetime.timedelta(
            seconds=random.randint(0, 86400)
        )

        procedure_concept_id = concepts.PRONE_POSITIONING
        procedure_type_concept_id = concepts.EHR

        n_occurrences = random.choice(range(max_occurrences)) + 1

        for i in range(n_occurrences):  # number of times of prone positioning

            list_of_procedures.append(
                ProcedureOccurrence(
                    person_id=person_id,
                    procedure_concept_id=procedure_concept_id,
                    procedure_type_concept_id=procedure_type_concept_id,
                    procedure_date=procedure_date,
                    procedure_datetime=procedure_datetime,
                    procedure_end_date=procedure_end_date,
                    procedure_end_datetime=procedure_end_datetime,
                )
            )

            prone_duration = random.choice(range(10, 20))
            procedure_end_datetime = procedure_datetime + datetime.timedelta(
                hours=prone_duration
            )
            procedure_end_date = procedure_end_datetime.date()

            back_duration = random.choice(range(4, 16))
            procedure_datetime += datetime.timedelta(
                hours=prone_duration + back_duration
            )
            procedure_date = procedure_datetime.date()

    return list_of_procedures


def create_cond(
    person_id: int, visit: VisitOccurrence, max_occurrences: int = 4
) -> List[ConditionOccurrence]:
    """
    create conditions from list 'conditions' (default: max_occurrences = up to four)

    Use condition_ids and weights for weighted random sampling. Taking multiple random samples without replacement requires np.random.choice
    COVID-19, Venous Thrombosis, Heparin-induced thrombocytopenia with thrombosis, Allergy to heparin, Allergy to heparinoid, Thrombocytopenic disorder, Pulmonary embolism, Acute respiratory distress syndrome
    """
    list_of_conditions = []
    r = random.randint(1, max_occurrences)
    diagnoses = np.random.choice(
        list(params.CONDITION_LIST), r, replace=False, p=COND_WEIGHTS
    )
    for diagnosis in diagnoses:
        condition_start_date = visit.visit_start_date
        condition_start_datetime = random_datetime(visit.visit_start_date)
        condition_concept_id = diagnosis
        condition_end_date = condition_start_date
        condition_end_datetime = condition_start_datetime
        list_of_conditions.append(
            ConditionOccurrence(
                person_id=person_id,
                condition_concept_id=condition_concept_id,
                condition_start_date=condition_start_date,
                condition_start_datetime=condition_start_datetime,
                condition_end_date=condition_end_date,
                condition_end_datetime=condition_end_datetime,
            )
        )
    return list_of_conditions


def create_obs(
    person_id: int,
    visit: VisitOccurrence,
    max_occurrences: int = 2,
    probability_threshold: float = 0.05,
) -> List[Observation]:
    """
    with a probability_threshold (default = 0.05), create entries concerning observation(s) from the list 'obs_list' (default: max_occurrences = up to two)

    Use observation_concept_ids and weights for weighted random sampling. Taking multiple random samples without replacement requires np.random.choice

    """

    list_of_observations = []
    ran = random.random()
    if ran > 1 - probability_threshold:
        r = random.randint(1, max_occurrences)
        observations = np.random.choice(
            list(params.OBSERVATION_LIST), r, replace=False, p=OBS_WEIGHTS
        )
        for observation in observations:
            observation_concept_id = observation
            observation_date = visit.visit_start_date
            observation_datetime = random_datetime(visit.visit_start_date)
            list_of_observations.append(
                Observation(
                    person_id=person_id,
                    observation_concept_id=observation_concept_id,
                    observation_date=observation_date,
                    observation_datetime=observation_datetime,
                )
            )
    return list_of_observations


def create_weight_measurements(
    person_id: int, person: Person, visit: VisitOccurrence
) -> List[Measurement]:
    """
    Create Measurements for weight and ideal weight
    """

    list_of_measurements = []

    assert person.gender_concept_id is not None
    param_set = params.WEIGHT[person.gender_concept_id]

    for parameter, data in param_set.items():
        measurement_concept_id = parameter
        measurement_date = visit.visit_start_date
        measurement_datetime = random_datetime(visit.visit_start_date)
        value_as_number = data["sample_func"]()
        unit_concept_id = data["unit"]

        list_of_measurements.append(
            Measurement(
                person_id=person_id,
                measurement_concept_id=measurement_concept_id,
                measurement_date=measurement_date,
                measurement_datetime=measurement_datetime,
                value_as_number=value_as_number,
                unit_concept_id=unit_concept_id,
            )
        )

    return list_of_measurements
