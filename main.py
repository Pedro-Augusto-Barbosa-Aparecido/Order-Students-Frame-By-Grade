import re
import pandas as pd

from typing import List

from utils.normalize import remove_accents


def extract_grades_from_students_dataframe(student_dataframe: pd.DataFrame, pattern: re.Pattern):
    return student_dataframe.loc[
        student_dataframe["Série Normalized"].str.contains(
            pattern,
            regex=True
        )
    ]


students_df = pd.read_excel(r"files/Alunos 2023-09-16 17_59_45.xlsx")
students_df.sort_values("Série", inplace=True)
students_df.reset_index(drop=True, inplace=True)

students_df["Série Normalized"] = students_df["Série"].transform(remove_accents)

period_pattern = re.compile("periodo", re.IGNORECASE | re.MULTILINE)
maternal_pattern = re.compile("maternal", re.IGNORECASE | re.MULTILINE)
high_school_pattern = re.compile("^[0-9]+.+EM$", re.IGNORECASE | re.MULTILINE)

students_in_period = extract_grades_from_students_dataframe(students_df, period_pattern)
students_in_maternal = extract_grades_from_students_dataframe(students_df, maternal_pattern)
students_in_high_school = extract_grades_from_students_dataframe(students_df, high_school_pattern)
students_in_elementary_school = students_df.drop(
    list(students_in_period.index) +
    list(students_in_maternal.index) +
    list(students_in_high_school.index)
)

students_ordered = pd.concat([
    students_in_maternal,
    students_in_period,
    students_in_elementary_school,
    students_in_high_school
])

dataframes: List[pd.DataFrame] = [
    students_in_maternal,
    students_in_period,
    students_in_elementary_school,
    students_in_high_school,
    students_ordered
]

for dataframe in dataframes:
    dataframe.drop(["Série Normalized"], axis=1, inplace=True)

with pd.ExcelWriter("Ordered Students.xlsx", engine="openpyxl") as writer:
    students_ordered.to_excel(writer, "Ordered Students", index=False)
    students_in_maternal.to_excel(writer, "Students in Maternal", index=False)
    students_in_period.to_excel(writer, "Students in Period", index=False)
    students_in_elementary_school.to_excel(writer, "Students in Elementary School", index=False)
    students_in_high_school.to_excel(writer, "Students in High School", index=False)
