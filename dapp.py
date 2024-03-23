import datetime
from os import environ
import logging
import requests
import sqlite3
import json
import sys

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = 'http://localhost:8080/host-runner'
logger.info(f"HTTP rollup_server url is {rollup_server}")

DB_CREATED = { 'created': True}

con = sqlite3.connect("data.db")

class tutorial:
    def __init__(self, title, description, approximatedTime, steps, address, likes, toolTags, updatedAt, createdAt):
        self.title = title
        self.description = description
        self.approximatedTime = approximatedTime
        self.steps = steps
        self.address = address
        self.likes = likes
        self.toolTags = toolTags
        self.updatedAt = updatedAt
        self.createdAt = createdAt
        
class tutorial_step:
    def __init__(self, title, content, tutorial_id):
        self.title = title
        self.content = content
        self.tutorial_id = tutorial_id
        
class tool_tag:
    def __init__(self, name, tutorial_id, icon):
        self.name = name
        self.tutorial_id = tutorial_id
        self.icon = icon

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
    
def create_tutorial(payload):
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
        statement = payload['data']
        try:
            tutorial = {
                "title": statement["title"],
                "description": statement["description"],
                "approximatedTime": statement["approximatedTime"],
                "address": statement["address"],
                "likes": 0,
                "updatedAt": None,
                "createdAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tutorial_steps = statement["steps"]
            tool_tags = statement["toolTags"]

            # Insert tutorial into the database
            cur.execute("INSERT INTO tutorial (title, description, approximatedTime, address, likes, updatedAt, createdAt) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (tutorial["title"], tutorial["description"], tutorial["approximatedTime"], tutorial["address"], tutorial["likes"], tutorial["updatedAt"], tutorial["createdAt"]))
            tutorial_id = cur.lastrowid

            # Insert tutorial steps into the database
            for step in tutorial_steps:
                cur.execute("INSERT INTO tutorial_step (title, content, tutorial_id) VALUES (?, ?, ?)",
                            (step["title"], step["content"], tutorial_id))

            # Insert tool tags into the database
            for tag in tool_tags:
                cur.execute("INSERT INTO tool_tag (name, tutorial_id, icon) VALUES (?, ?, ?)",
                            (tag["name"], tutorial_id, tag["icon"]))
                
            result = cur.fetchall()

        except Exception as e:
            status = "reject"
            msg = f"Error executing statement '{statement}': {e}"
            post("report", msg, logging.ERROR)

    
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
        result = {}
        try:
            page = statement.get("page", 1)
            limit = statement.get("limit", 10)
            offset = (page - 1) * limit

            cur.execute("SELECT * FROM tutorial LIMIT ? OFFSET ?", (limit, offset))
            tutorial_rows = cur.fetchall()
            cur.execute("SELECT * FROM tutorial_step")
            step_rows = cur.fetchall()
            cur.execute("SELECT * FROM tool_tag")
            tag_rows = cur.fetchall()
            result = sanitize_tutorial({"tutorial": tutorial_rows, "tutorial_step": step_rows, "tool_tag": tag_rows})
            total = cur.execute("SELECT COUNT(*) FROM tutorial").fetchone()[0]
            total_pages = total // limit + 1
            data = {
                "data": result,
                "page": page,
                "limit": limit,
                "totalQuantity": total,
                "totalPages": total_pages
            }

        except Exception as e:
            msg = f"Error executing statement '{statement}': {e}"
            post("report", msg, logging.ERROR)
            return None

    except Exception as e:
        msg = f"Error processing data {statement})"
        post("report", msg, logging.ERROR)
        return None

    return data

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
            tutorial_rows = cur.fetchall()
            cur.execute("SELECT * FROM tutorial_step")
            step_rows = cur.fetchall()
            cur.execute("SELECT * FROM tool_tag")
            tag_rows = cur.fetchall()
            result = sanitize_tutorial({"tutorial": tutorial_rows, "tutorial_step": step_rows, "tool_tag": tag_rows})

        except Exception as e:
            msg = f"Error executing statement '{statement}': {e}"
            post("report", msg, logging.ERROR)
            return None

    except Exception as e:
        msg = f"Error processing data {statement})"
        post("report", msg, logging.ERROR)
        return None

    return result

def get_tutorial_by_id(statement):
    try:
        try:
            cur = con.cursor()
        except Exception as e:
            msg = f"Critical error connecting to database: {e}"
            post("exception", msg, logging.ERROR)
            sys.exit(1)
        result = None
        try:
            id = statement["id"]
            address = statement["address"]
            cur.execute("SELECT * FROM tutorial WHERE id = ?", (id,))
            tutorial_rows = cur.fetchall()
            cur.execute("SELECT * FROM tutorial_step")
            step_rows = cur.fetchall()
            cur.execute("SELECT * FROM tool_tag")
            tag_rows = cur.fetchall()
            result = sanitize_tutorial({"tutorial": tutorial_rows, "tutorial_step": step_rows, "tool_tag": tag_rows})

        except Exception as e:
            msg = f"Error executing statement '{statement}': {e}"
            post("report", msg, logging.ERROR)
            return None

    except Exception as e:
        msg = f"Error processing data {statement})"
        post("report", msg, logging.ERROR)
        return None

    return result

def sanitize_tutorial(data):
    tutorial_rows = data['tutorial']
    step_rows = data['tutorial_step']
    tag_rows = data['tool_tag']
    result = {}    
    for tutorial_row in tutorial_rows:
                tutorial_id = tutorial_row[0]
                result[tutorial_id] = {
                    "id": tutorial_row[0],
                    "title": tutorial_row[1],
                    "description": tutorial_row[2],
                    "approximatedTime": tutorial_row[3],
                    "address": tutorial_row[4],
                    "likes": tutorial_row[5],
                    "updatedAt": tutorial_row[6],
                    "createdAt": tutorial_row[7],
                    "steps": [],
                    "tags": []
                }       
    for step_row in step_rows:
        tutorial_id = step_row[3]
        step = {"id": step_row[0], "title": step_row[1], "content": step_row[2], "tutorial_id": step_row[3]}
        result[tutorial_id]["steps"].append(step)

    for tag_row in tag_rows:
        tutorial_id = tag_row[2]
        tag = {"name": tag_row[1], "tutorial_id": tag_row[2], "icon": tag_row[3]}
        result[tutorial_id]["tags"].append(tag)
                
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
            cur.execute("UPDATE tutorial SET likes = likes + 1 WHERE address = ?", (statement["address"],))
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

def create_tables():
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tutorial (id INTEGER PRIMARY KEY, title TEXT, description TEXT, approximatedTime TEXT, address TEXT, likes INTEGER, updatedAt TEXT, createdAt TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS tutorial_step (id INTEGER PRIMARY KEY, title TEXT, content TEXT, tutorial_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS tool_tag (id INTEGER PRIMARY KEY, name TEXT, tutorial_id INTEGER, icon TEXT)")

    con.commit()

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
        3 : lambda: get_tutorial_by_id(payload)
    }
    function = function_map.get(function_id)
    if function:
        result = function()
        return result
    else:
        return "reject"
    


def handle_advance(data):
    if DB_CREATED.get('created') == True:
        create_tables()
        DB_CREATED['created'] = False
    statement = hex2str(data["payload"])
    payload = json.loads(statement) 
    response = handle_functions_advance(payload)
    
    return response


def handle_inspect(data):
    statement = hex2str(data["payload"])
    payload = json.loads(statement)
    response = handle_functions_inspect(payload)
    if response is None or len(response) == 0:
        return "reject"
    response = json.dumps(response)
    enconde = str2hex(response)
    report = {"payload": enconde}
    requests.post(rollup_server + "/report", json=report)

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
