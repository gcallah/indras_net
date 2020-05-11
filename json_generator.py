#!/usr/bin/env python3

import sys
import json
import distutils.util
import argparse
"""
    Script to generate a *_model.json file, given *.py
    *.py file must have docstring at the header of the file first
    otherwise, an empty *_model.json file will be generated
"""

"""
    usage / options
    ./json_generator filename
"""

# Docstring format
# the docstring (if there is any) must contain all of these (no more no less)
"""
    name: str,
    run: str,
    props: str,
    doc: str,
    source: str,
    graph: str,
    active: bool
"""

# jsonFields is a list of fields or keys that the parser must know
# "source" should be required as a field at the very least. It is later used by
# json_combiner.py as a way to tell if a model is new or not
jsonFields = set(["name", "run", "props", "doc", "source", "graph", "active"])
script_name = sys.argv[0]
jsonFieldDelimitor = ":"
saw_error = False


def validate_config():  # () -> None
    """
        Checks the configuration of this script
    """
    if(len(jsonFields) == 0):
        script_output("jsonFields should be len greater than 0")
        exit(1)
    if(len(jsonFieldDelimitor) != 1):
        script_output(
            "jsonFieldDelimitor must be len 1")
        exit(1)


def script_output(message, withName=True):  # (str, bool) -> None
    """
        Wrapper for print to include the script's name
    """
    if(withName is True):
        print(script_name + ": " + message)
    else:
        print(message)


def has_docstring_quotes(line):  # (str) -> bool
    """
        Function to check for \"\"\" or \'\'\' in given string
        Used for checking start and end of docstring
    """
    f1, f2 = line.find("\'\'\'"), line.find("\"\"\"")

    if(f1 != -1 or f2 != -1):
        return True
    return False


def validate_docstring(content, filename, withOutput=True):
    """
        Function to validate the contents of a given docstring
        pass in filename for error messages

        params: ([str...], str, bool) -> bool
    """
    global saw_error
    MIN_DOCLEN = 2  # Min len of the docstring should be at least 2 lines
    QUOTE_LEN = 4  # len of a """ or ''' (counting newline)

    if(len(content) < MIN_DOCLEN):
        if(withOutput):
            script_output("docstring too short in " + filename)
            saw_error = True
        return False

    if(len(content[0].strip()) > QUOTE_LEN or
            len(content[len(content)-1].strip()) > QUOTE_LEN):
        if(withOutput):
            script_output("docstring quotes should be in a line by itself")
            script_output("Problem in " + filename, False)
            saw_error = True
        return False

    return True


def validate_model(model_kv, key_set):
    """
        Method to check if docstring we read in is valid
        Things to check for:
        1.) Missing fields
        2.) Any foreign keys
        3.) Duplicate keys

        key_set is the set of unique keys in model_kv
    """
    global saw_error
    # In case, file had a docstring, but it wasn't what we were expecting
    if(len(key_set) == 0):
        script_output("Didn't find any known fields.")
        script_output("Fields should be in the following format:", False)
        script_output("<key>: <value>\n", False)
        script_output(
            "Please make sure your FIRST docstring has all the fields:", False)
        script_output(str(jsonFields), False)
        saw_error = True
        return False

    # Missing fields
    if(len(key_set) != len(jsonFields)):
        script_output("Missing required fields: " + str(jsonFields - key_set))
        script_output(
            "Please make sure to put a space after delimitor", False)
        script_output(
            "Current delimitor: " + repr(jsonFieldDelimitor[0]), False)
        saw_error = True
        return False

    # If for some random reason duplicates were not filtered during parsing
    if(len(model_kv) != len(jsonFields)):
        script_output(
            "script error, model_kv is not the same len as jsonFields")
        saw_error = True
        return False

    return True


def strip_docstring(content):
    """
        function to strip away leading and trailing spaces within docstring
        Returns empty [] if nonvalid
    """
    if(validate_docstring(content, "", False)):
        result = [content[0]]
        startIndex, endIndex = 1, len(content) - 2
        while(startIndex < len(content) - 1 and len(content[startIndex]) == 0):
            startIndex += 1

        while(endIndex > 0 and len(content[endIndex]) == 0):
            endIndex -= 1

        # If there was nothing to strip, skip any work and just return content
        if(startIndex == 1 and endIndex == len(content) - 2):
            return content

        # Grab everything between
        result.extend(content[startIndex:endIndex+1])

        # Add in the ending docstring
        result.append(content[-1])
        return result

    return []


def clean_valString(valString):
    """
        Cleans up the value string that was processed
        removes leading and trailing whitespace and comma
    """
    # strip leading and trailing whitespace
    result = valString.strip()
    # remove trailing comma if any
    if(len(result) > 0 and result[-1] == ","):
        result = result[:len(result)-1]

    return result


def convert_valString(valString):
    """
        Function to attempt to convert the string to its actual type
        I.E, "1" -> 1, "true" -> true
        The catch all type is to string
    """

    if(valString.lower() == "null"):
        return None
    try:
        return int(valString)
    except ValueError:
        try:
            # This returns 0,1 if the string is a bool value
            # bool() then converts it into True or False
            return bool(distutils.util.strtobool(valString))
        except ValueError:
            return valString
    except Exception:
        return valString


def parse_docstring(file_path):
    """
        parses the docstring at the top of every model file
        returns a [] with tuples (KEY, VAL) in the order of the jsonFields
        general expected form: <key>: <value>

        Parsing logic
        1.) Reading in lines between docstring quotes and prestrip
        leading whitespaces
        2.) Checks if docstring is empty or docstring quotes on same line
        (Stops parsing if true)
        3.) loop through lines of docstring we read in. Looking for
        <key>: <value> pattern. If ": " is found, then we got a potential key.
        Else, the line is part of the <value> of the last key detected
        3b.) Stop parsing if we found duplicate keys, or
        we found an unexpected key
        4.) return the result if our result was validated
    """
    global saw_error
    with open(file_path, 'r') as input_stream:
        # Step 1:
        # Read everything from the docstring in first for processing
        docstring_content = []
        num_indicator = 0  # Indicators of docstring quotes
        while(num_indicator < 2):
            line = input_stream.readline()

            if(len(line) == 0):
                return {}

            if(has_docstring_quotes(line)):
                num_indicator += 1

            # We have entered a docstring
            if(num_indicator > 0):
                # Prestrip whitespaces in front of line
                line = line.lstrip()
                docstring_content.append(line)

        # If invalid docstring, return empty
        if(validate_docstring(docstring_content, file_path) is False):
            return {}

        # Remove leading and trailing lines
        docstring_content = strip_docstring(docstring_content)

        # Step 2: Now we process the docstring
        model_kv = {}  # model's key val pair for the json
        delimitorLen = len(jsonFieldDelimitor)
        found_set = set()
        keyString, valueString = "", ""

        for i in range(1, len(docstring_content)-1):
            line = docstring_content[i]
            delimitorIndex = line.find(jsonFieldDelimitor)

            # Found sign of a key
            if(delimitorIndex != -1 and
                delimitorIndex+1 < len(line) and
                    line[delimitorIndex+1].isspace()):
                lineKey = line[:delimitorIndex]

                if(lineKey in found_set):
                    script_output("FOUND DUPLICATE FIELD: " + lineKey)
                    script_output("in " + file_path, False)
                    saw_error = True
                    return {}

                if(lineKey in jsonFields):
                    if(len(valueString) > 0):
                        model_kv[keyString] = \
                            convert_valString(clean_valString(valueString))

                    found_set.add(lineKey)
                    v_start = len(lineKey) + delimitorLen
                    keyString = lineKey
                    valueString = line[v_start:]
                else:
                    # stop parsing since we found a rogue key
                    script_output("UNKNOWN KEY " + repr(lineKey))
                    saw_error = True
                    return {}
            else:
                valueString += line

        # Last key
        model_kv[keyString] = convert_valString(clean_valString(valueString))

        if(validate_model(model_kv, found_set) is False):
            return {}

        # Step 3: return the finished product to our caller
        return model_kv


def generate_json(model_kv):
    """
        Generates json  and prints to stdout
        model_kv is generated by parse_docstring()
        it contains the key value pair of each field
        (dict) -> None
    """
    if(type(model_kv) != dict):
        script_output("generate_json(dict), check function def")
        exit(1)

    print(json.JSONEncoder(sort_keys=True, indent=4).encode(model_kv))


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("filename")

    args = arg_parser.parse_args()

    model_file = args.filename

    validate_config()

    generate_json(parse_docstring(model_file))

    if(saw_error is True):
        exit(1)


if __name__ == "__main__":
    main()
