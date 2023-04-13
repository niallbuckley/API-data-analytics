import os

try:
    OPEN_API_KEY = os.environ['QMETRY_OPEN_API_KEY']
except:
    print("Couldn't find env variable - QMETRY_OPEN_API_KEY.")
    exit()

PROJECT_ID="10300"

XML_ROBOT_OUTPUT_DEFAULT_PATH="app/logfiles/output.xml"

HEADER={"Content-Type": "application/json","apiKey": OPEN_API_KEY}

ENDP_TEST_CYCLES_BASE="https://qtmcloud.qmetry.com/rest/api/latest/testcycles/"
ENDP_TEST_CYCLES_SEARCH="search/"
ENDP_GET_LINKED_TEST_CASES_OF_TEST_CYCLE="/testcases/search/?fields=id%2C%20key%2C%20summary%2C%20description%2C%20executionResult%2C%20status%2C%20priority%2Cenvironment%2C%20tcWithDefects%2CestimatedTime%2CactualTime%2CcreatedOn%2CupdatedOn%2Csprint%2CseqNo%2ClatestTcExecutionId&maxResults=100"

ENDP_START_NEW_EXECUTION_TEST_CASE="/testcases/"
ENDP_START_NEW_EXECUTION_EXECUTION="/executions"


ENDP_PROJECTS_BASE="https://qtmcloud.qmetry.com/rest/api/latest/projects/"
ENDP_GET_EXECUTION_RESULTS="/execution-results"


ENDP_UPDATE_TEST_CASE_EXECUTION="/testcase-executions/"