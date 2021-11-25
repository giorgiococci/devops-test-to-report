from lxml import etree
import pandas as pd
import ast
from pandas.io.json import json_normalize


def convert_test_result_to_dataframe(filepath, test_type):

    results = []

    with open(filepath, "r") as f:
        xml_string = f.read()

        root = etree.fromstring(xml_string)

        for child in root:
            name = child.attrib["name"]
            failures= child.attrib["failures"]
            for subchild in child:
                result = {}
                result["name"] = name
                result["failures"] = failures

                if test_type == "pylint":
                    if "class" in subchild.attrib:
                        result["class"] = subchild.attrib["class"]
                        for subsubchild in subchild:
                            if subsubchild.tag == "failure":
                                result["category"] = subsubchild.attrib["message"]
                                result["failure"] = subsubchild.text
                            elif subsubchild.tag == "system-out":
                                result["systemout"] = subsubchild.text
                            elif subsubchild.tag == "system-err":
                                result["systemerr"] = subsubchild.text
                elif test_type == "flake8":
                    result["category"] = subchild.attrib["name"]

                results.append(result)

    df = pd.DataFrame(results)
    return df



df_pylint = convert_test_result_to_dataframe("data/test_result/1244/pylint-testresults.xml", "pylint")
df_flake8 = convert_test_result_to_dataframe("data/test_result/1244/flake8-testresults.xml", "flake8")


dfreport_pylint = df_pylint.groupby(["category"]).count()
print(dfreport_pylint["name"])
dfreport_pylint = df_pylint.groupby(["category"]).agg({"failure": "max", "class": "count"})
dfreport_pylint.rename(columns = {'failure':'example', 'class':'nr_occurrences'}, inplace = True)

# Replace new line characters with space in example column
dfreport_pylint["example"] = dfreport_pylint["example"].str.replace("\n", " ")

# Rename column category
df_flake8.rename(columns = {"category": "example"}, inplace = True)

# Add category column as first 4 characters of example column
df_flake8["category"] = df_flake8["example"].str[:4]

dfreport_flake8 = df_flake8.groupby(["category"]).agg({"example": "max", "name": "count" })

# Rename columns for report
dfreport_flake8.rename(columns = {'name':'nr_occurrences'}, inplace = True)

# Export dataframe to csv
dfreport_pylint.to_csv("data/export/1244/pylint_report.csv")
dfreport_flake8.to_csv("data/export/1244/flake8_report.csv")