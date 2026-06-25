"""
Universal Mapper
Позволяет загрузить Excel
с любыми названиями колонок.

Например

Profession

Name

Job Title

Все это станет title
"""


COLUMN_MAPPING = {

    "Profession": "title",
    "Job Title": "title",
    "Name": "title",
    "Описание": "description",
    "Description": "description",
    "Category": "category",
    "Категория": "category"
}