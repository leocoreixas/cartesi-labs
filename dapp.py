from os import environ
import logging
import requests
import sqlite3
import json
import sys

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

con = sqlite3.connect("data.db")


def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
    """
    Encodes a string as a hex string
    """
    return "0x" + str.encode("utf-8").hex()

def post(endpoint, payloadStr, logLevel):
    logger.log(logLevel, f"Adding {endpoint} with payload: {payloadStr}")
    payload = str2hex(payloadStr)
    requests.post(f"{rollup_server}/{endpoint}", json={"payload": payload})
    
def create_tutorial(statement):
    status = "accept"
    try:
        try:
            cur = con.cursor()
        except Exception as e:
            msg = f"Critical error connecting to database: {e}"
            post("exception", msg, logging.ERROR)
            sys.exit(1)

        result = None
        status = "accept"
        try:
            tutorial = statement["tutorial"]
            cur.execute("INSERT INTO tutorial (title, description, author, url, address) VALUES (?, ?, ?, ?, ?)", (tutorial["title"], tutorial["description"], tutorial["author"], tutorial["url"], tutorial["address"]))
            result = cur.fetchall()

        except Exception as e:
            status = "reject"
            msg = f"Error executing statement '{statement}': {e}"
            post("report", msg, logging.ERROR)

        if result:
            payloadJson = json.dumps(result)
            post("notice", payloadJson, logging.INFO)

    except Exception as e:
        status = "reject"
        msg = f"Error processing data {statement})"
        post("report", msg, logging.ERROR)

    return status

def get_tutorials(statement):
    try:
        try:
            cur = con.cursor()
        except Exception as e:
            msg = f"Critical error connecting to database: {e}"
            post("exception", msg, logging.ERROR)
            sys.exit(1)
        result = None
        try:
            cur.execute("SELECT * FROM tutorial")
            result = cur.fetchall()

        except Exception as e:
            msg = f"Error executing statement '{statement}': {e}"
            post("report", msg, logging.ERROR)
            return None

        if result:
            payloadJson = json.dumps(result)
            post("notice", payloadJson, logging.INFO)

    except Exception as e:
        msg = f"Error processing data {statement})"
        post("report", msg, logging.ERROR)
        return None

    return result

def get_tutorial_by_address(statement):
    try:
        try:
            cur = con.cursor()
        except Exception as e:
            msg = f"Critical error connecting to database: {e}"
            post("exception", msg, logging.ERROR)
            sys.exit(1)
        result = None
        try:
            address = statement["address"]
            cur.execute("SELECT * FROM tutorial WHERE address = ?", (address,))
            result = cur.fetchall()

        except Exception as e:
            msg = f"Error executing statement '{statement}': {e}"
            post("report", msg, logging.ERROR)
            return None

        if result:
            payloadJson = json.dumps(result)
            post("notice", payloadJson, logging.INFO)

    except Exception as e:
        msg = f"Error processing data {statement})"
        post("report", msg, logging.ERROR)
        return None

    return result

def get_tutorial_liked_by_address(statement):
    try:
        try:
            cur = con.cursor()
        except Exception as e:
            msg = f"Critical error connecting to database: {e}"
            post("exception", msg, logging.ERROR)
            sys.exit(1)
        result = None
        try:
            address = statement["address"]
            cur.execute("SELECT * FROM tutorial_liked WHERE address = ?", (address,))
            result = cur.fetchall()

        except Exception as e:
            msg = f"Error executing statement '{statement}': {e}"
            post("report", msg, logging.ERROR)
            return None

        if result:
            payloadJson = json.dumps(result)
            post("notice", payloadJson, logging.INFO)

    except Exception as e:
        msg = f"Error processing data {statement})"
        post("report", msg, logging.ERROR)
        return None

    return result

def create_like_Tutorial(statement):
    try:
        try:
            cur = con.cursor()
        except Exception as e:
            msg = f"Critical error connecting to database: {e}"
            post("exception", msg, logging.ERROR)
            sys.exit(1)
        result = None
        try:
            address = statement["address"]
            tutorial_id = statement["tutorial_id"]
            cur.execute("INSERT INTO tutorial_liked (address, likes, tutorial_id) VALUES (?, 1, ?) ON CONFLICT(address) DO UPDATE SET likes = tutorial_liked.likes + 1", (address, tutorial_id))
            result = cur.fetchall()
            
            cur.execute("SELECT * FROM tutorial_liked WHERE address = ?", (address,))
            tutorial_liked = cur.fetchall()
            
            prizeExists = cur.execute("SELECT * FROM prize WHERE tutorial_id = ?", (tutorial_id,)).fetchall()
            if tutorial_liked[0][1] % 10 == 0:
                if prizeExists:
                    cur.execute("UPDATE prize SET prize = prize + 1 WHERE tutorial_id = ?", (tutorial_id,))
                else:
                    cur.execute("INSERT INTO prize (tutorial_id, prize) VALUES (?, 1)", (tutorial_id,))
            
            

        except Exception as e:
            msg = f"Error executing statement '{statement}': {e}"
            post("report", msg, logging.ERROR)
            return None

        if result:
            payloadJson = json.dumps(result)
            post("notice", payloadJson, logging.INFO)

    except Exception as e:
        msg = f"Error processing data {statement})"
        post("report", msg, logging.ERROR)
        return None

    return result

def handle_functions_advance(payload):
    function_id = int(payload["function_id"])
    function_map = {
        1: lambda: create_tutorial(payload),
        2: lambda: create_like_Tutorial(payload)
    }

    function = function_map.get(function_id)
    if function:
        return function()
    else:
        return "reject"


def handle_functions_inspect(payload):
    function_id = int(payload["function_id"])
    function_map = {
        1 : lambda: get_tutorials(payload),
        2 : lambda: get_tutorial_by_address(payload),
        3 : lambda: get_tutorial_liked_by_address(payload)
    }
    function = function_map.get(function_id)
    if function:
        result = function()
        return result
    else:
        return "reject"
    


def handle_advance(data):
    statement = hex2str(data["payload"])
    payload = json.loads(statement) 
    response = handle_functions_advance(payload)
    
    return response


def handle_inspect(data):
    statement = hex2str(data["payload"])
    payload = json.loads(statement)
    response = handle_functions_inspect(payload)
    return "accept"


handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
