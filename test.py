
import QMetryConst
import requests
import Response
import QMetryExecutionResult
import json
import subprocess

def __get_linked_test_cases_of_test_cycle(id):
    pload={"filter": {"folderId":-1}}
    response = requests.post(QMetryConst.ENDP_TEST_CYCLES_BASE+id+QMetryConst.ENDP_GET_LINKED_TEST_CASES_OF_TEST_CYCLE, json=pload, headers=QMetryConst.HEADER)
    print ("response: ", response)
    Response.check_response(response)
    found_test_cases=len(response.json()["data"])
    if found_test_cases > 0:
        test_cases = response.json()["data"]
    else:
        print("Test Cycle contain no Test Cases. Please double check Test Cycle in QMetry.")
        exit()

    return test_cases

def __get_test_cycle_id(key):
        pload = {"filter":{"projectId": QMetryConst.PROJECT_ID,"key": key}}
        response = requests.post(QMetryConst.ENDP_TEST_CYCLES_BASE+QMetryConst.ENDP_TEST_CYCLES_SEARCH, json=pload, headers=QMetryConst.HEADER)
        Response.check_response(response)
        found_test_cycles=len(response.json()["data"])
        if found_test_cycles == 1:
            id = response.json()["data"][0]["id"]
        elif found_test_cycles == 0:
            print("Test Cycle {} not found in QMetry. Please make sure that Test Cycle already exist in QMetry project.".format(key))
            exit()
        else:
            print("Something went wrong during searching Test Cycle in QMetry. Found {} Test Cycles. Please check response:\n{}".format(found_test_cycles,response.json()))
            exit()

        return str(id)

def download_zip(zip_url):
    #filename = "./csv/" + zip_url + ".zip"
    filename = "auto_data_" + id
    subprocess.run(["wget", zip_url])



def __get_test_cycle_attachments(key):
    response = requests.get(QMetryConst.ENDP_TEST_CYCLES_BASE + key + '/attachment/', headers=QMetryConst.HEADER)
    #print (response.json())
    if response.json()["total"] > 0:
        for objct in response.json()["data"]:
            if objct["name"] == 'logfiles.zip':
                #if seen before. continue
                print (objct["url"])
                download_zip(objct["url"])


     

# curl  -i 'https://qtmcloud.qmetry.com/rest/api/latest/testcycles/search/' -H 'Content-Type: application/json' 
def __get_test_cycle_list():
     pload = {"filter":{"projectId":"10453","folderId":521282}}
     response = requests.post(QMetryConst.ENDP_TEST_CYCLES_BASE + 'search/', json=pload, headers=QMetryConst.HEADER)
     if response.ok:
        for key_obj in response.json()["data"]:
            #print (key_obj["key"])
            __get_test_cycle_attachments(key_obj["key"])
            break
     else:
        print ("Error getting the list of test cycle keys response code: " + str(response.status_code))


if __name__ == '__main__':
    #linked = __get_linked_test_cases_of_test_cycle("EEPD-TR-43388")
    #print (linked)
    pp = __get_test_cycle_list()
    #print (pp)
    

