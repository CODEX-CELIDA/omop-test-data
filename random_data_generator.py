import argparse
import json
import random
from dataclasses import asdict
from typing import Any, Dict

import numpy as np
import psycopg2

SECONDS_PER_DAY = 86400


def insert(table: str, data: Dict) -> Any:
    """
    Insert data into a table
    """
    columns = ", ".join(data.keys())
    value_placeholder = ", ".join(["%s"] * len(data))
    sql = f"INSERT INTO {table} ({columns}) VALUES ({value_placeholder}) RETURNING {table}_id"
    cursor.execute(sql, list(data.values()))

    return cursor.fetchone()[0]


def next_person_id() -> int:
    """
    Return the maximal patient_id in the database
    """
    cursor.execute("SELECT MAX(person_id) FROM person")
    person_id = cursor.fetchone()[0]

    if person_id is None:
        return 0

    return person_id + 1


def connect_db() -> psycopg2.extensions.connection:
    """
    Connect to the database
    """
    settings = json.loads(open(".credentials.json").read())
    schema = settings.pop("schema", "cds_cdm")
    con = psycopg2.connect(**settings, options=f"-c search_path={schema}")

    return con


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate OMOP test data for CODEX+ CELIDA",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "n_person",
        help="Number of persons to generate",
        type=int,
        default=10,
        nargs="?",
    )

    parser.add_argument(
        "--seed", help="Seed for random number generator", type=int, nargs="?"
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)

    # MUST be imported AFTER setting the seed!
    from data_generator.generator import (
        create_drug_exp2,
        create_lab_values_measurements,
        create_prone_positioning_procedure,
        create_vent_params_measurements,
        create_vent_params_procedure,
        create_cond,
        create_obs,
        create_weight_measurements
    )
    from omop.tables import Person, VisitOccurrence

    con = connect_db()
    cursor = con.cursor()

    # get maximal patient_id from DB
    start_patient_id = next_person_id()
    print("Patient start ID for new patient data: ", start_patient_id)

    patient_id_list = range(start_patient_id, start_patient_id + args.n_person)

    # create patients and insert into DB
    for person_id in patient_id_list:
        print("#########################")
        print("Creating data for patient with ID: ", person_id)

        # create person
        person = Person(person_id)

        # create visit
        visit = VisitOccurrence(person_id=person_id)

        # create drugs
        list_of_drugs = create_drug_exp2(person_id, visit, n_administrations=10)

        # create first procedure
        prod = create_vent_params_procedure(person_id, visit)

        # create measurements
        list_of_measurements = create_vent_params_measurements(
            person_id, prod, visit
        )  # REALLY USE THE FIRST PROD HERE??
        list_of_measurements += create_lab_values_measurements(person_id, visit)

        # create rest of procedures
        list_of_procedures = []
        if prod is not None:
            list_of_procedures.append(prod)

        list_of_procedures += create_prone_positioning_procedure(
            person_id, visit, max_occurrences=5
        )

        # create list of condition_occurences
        list_of_conditions = create_cond(person_id, visit, max_occurrences=4)

        # create list of observations
        list_of_observations = create_obs(person_id, visit, max_occurrences=2, probability_threshold=0.5)

        # create measurements for weight and ideal weight
        list_of_measurements += create_weight_measurements(person_id, person, visit)

        # break
        ### INSERT
        print("Loading data into database")

        insert("person", asdict(person))
        con.commit()
        print("- Inserted patient data")

        # insert visit
        insert("visit_occurrence", asdict(visit))
        con.commit()
        print("- Inserted visit data")

        # insert list of drugs
        for d in list_of_drugs:
            insert("drug_exposure", asdict(d))
        con.commit()
        print("- Inserted drug exposure data with ", len(list_of_drugs), " entries")

        # insert procedure
        for prod in list_of_procedures:
            insert("procedure_occurrence", asdict(prod))
        con.commit()
        print(
            "- Inserted procedure occurrence data with ",
            len(list_of_procedures),
            " entries",
        )

        # insert list of measurements
        for m in list_of_measurements:
            insert("measurement", asdict(m))
        con.commit()
        print(
            "- Inserted measurement data with ", len(list_of_measurements), " entries"
        )

        # insert list of conditions
        for c in list_of_conditions:
            insert("condition_occurrence", asdict(c))
        con.commit()
        print("- Inserted condition_occurrence data with ", len(list_of_conditions), " entries")

        # insert list of observations
        for o in list_of_observations:
            insert("observation", asdict(o))
        con.commit()
        print("- Inserted observation data with ", len(list_of_observations), " entries")

    con.close()
