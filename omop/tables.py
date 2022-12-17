"""
DATA CLASSES

This module contains the data classes used in the OMOP CDM.
"""
import datetime
import random

pass

from pydantic.dataclasses import dataclass

from data_generator import parameter as params
from omop import concepts

# DUMMY_* values are used as default values for the data classes,
# in order to use required fields without having to provide a value.
# The value will then be set in the __post_init__ function of the
# respective data class.
DUMMY_DATE = datetime.date(1900, 1, 1)
DUMMY_DATETIME = datetime.datetime(1900, 1, 1, 0, 0, 0)
DUMMY_INT = -1
DUMMY_CONCEPT_ID = concepts.UNKNOWN


def random_date(start_date: datetime.date, end_date: datetime.date) -> datetime.date:
    """Generate a random datetime between `start_date` and `end_date`"""
    return start_date + datetime.timedelta(
        days=random.randint(0, (end_date - start_date).days),
    )


def random_datetime(date: datetime.date) -> datetime.datetime:
    """Generate a random datetime between `date` and `date` + 1 day"""
    return datetime.datetime.combine(
        date,
        datetime.time(
            random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)
        ),
    )


@dataclass
class Person:
    """
    Person data class from OMOP CDM v5.4.
    """

    person_id: int
    # All further values will be overwritten in __post_init__
    gender_concept_id: int = DUMMY_CONCEPT_ID
    year_of_birth: int = DUMMY_INT
    month_of_birth: int = DUMMY_INT
    day_of_birth: int = DUMMY_INT
    race_concept_id: int = DUMMY_CONCEPT_ID
    ethnicity_concept_id: int = DUMMY_CONCEPT_ID

    def __post_init__(self) -> None:
        """
        Set the default values for the person.
        """
        self.gender_concept_id = random.choice(list(params.GENDER_LIST))
        date_of_birth = random_date(
            datetime.date(1920, 1, 1), datetime.date(2003, 12, 31)
        )

        self.year_of_birth = date_of_birth.year
        self.month_of_birth = date_of_birth.month
        self.day_of_birth = date_of_birth.day

        self.race_concept_id = concepts.UNKNOWN  # always set to zero / unknown
        self.ethnicity_concept_id = concepts.UNKNOWN  # always set to zero / unknown


@dataclass
class VisitOccurrence:
    """
    VisitOccurrence data class from OMOP CDM v5.4.
    """

    person_id: int
    # All following values will be overwritten in __post_init__
    visit_concept_id: int = DUMMY_CONCEPT_ID
    visit_start_date: datetime.date = DUMMY_DATE
    visit_start_datetime: datetime.datetime = DUMMY_DATETIME
    visit_end_date: datetime.date = DUMMY_DATE
    visit_end_datetime: datetime.datetime = DUMMY_DATETIME
    visit_type_concept_id: int = DUMMY_CONCEPT_ID

    def __post_init__(self) -> None:
        """
        Set the default values for the visit occurrence.
        """
        self.visit_concept_id = random.choice(list(params.VISIT_CONCEPTS))
        self.visit_start_date = random_date(
            start_date=params.VISIT_START_DATE, end_date=params.VISIT_END_DATE
        )
        self.visit_start_datetime = random_datetime(self.visit_start_date)
        self.visit_end_date = self.visit_start_date + datetime.timedelta(
            days=random.choice(range(3, 60))
        )
        self.visit_end_datetime = random_datetime(self.visit_start_date)
        self.visit_type_concept_id = concepts.VISIT_TYPE_STILL_PATIENT


@dataclass
class ProcedureOccurrence:
    """
    ProcedureOccurrence data class from OMOP CDM v5.4.
    """

    person_id: int
    procedure_concept_id: int
    procedure_type_concept_id: int
    procedure_date: datetime.date
    procedure_datetime: datetime.datetime
    procedure_end_date: datetime.date
    procedure_end_datetime: datetime.datetime


@dataclass
class DrugExposure:
    """
    DrugExposure data class from OMOP CDM v5.4.
    """

    person_id: int
    drug_concept_id: int
    drug_exposure_start_date: datetime.date
    drug_exposure_start_datetime: datetime.datetime
    drug_exposure_end_date: datetime.date
    drug_exposure_end_datetime: datetime.datetime
    quantity: int
    drug_type_concept_id: int = DUMMY_CONCEPT_ID

    def __post_init__(self) -> None:
        """
        Set the drug_type_concept_id to EHR
        """
        self.drug_type_concept_id = concepts.EHR


@dataclass
class Measurement:
    """
    Measurement data class (OMOP CDM v5.4)
    """

    person_id: int
    measurement_concept_id: int
    measurement_date: datetime.date
    measurement_datetime: datetime.datetime
    value_as_number: float
    unit_concept_id: int
    measurement_type_concept_id: int = DUMMY_CONCEPT_ID

    def __post_init__(self) -> None:
        """
        Set measurement_type_concept_id to EHR
        """
        self.measurement_type_concept_id = concepts.EHR


@dataclass
class ConditionOccurrence:
    """
    ConditionOccurrence data class (OMOP CDM v5.4)
    """

    person_id: int
    condition_concept_id: int
    condition_start_date: datetime.date
    condition_start_datetime: datetime.datetime
    condition_end_date: datetime.date
    condition_end_datetime: datetime.datetime
    condition_type_concept_id: int = DUMMY_CONCEPT_ID

    def __post_init__(self) -> None:
        """
        Set condition_type_concept_id to EHR
        """
        self.condition_type_concept_id = concepts.EHR


@dataclass
class Observation:
    """
    Observation data class (OMOP CDM v5.4)
    """

    person_id: int
    observation_concept_id: int
    observation_date: datetime.date
    observation_datetime: datetime.datetime
    observation_type_concept_id: int = DUMMY_CONCEPT_ID

    def __post_init__(self) -> None:
        """
        Set observation_type_concept_id to EHR
        """
        self.observation_type_concept_id = concepts.EHR
