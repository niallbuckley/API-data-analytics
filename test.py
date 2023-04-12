
import QMetryConst
import requests
import subprocess
import glob
import shutil


def download_zip(zip_url, id):
    filename = "auto_data_" + id
    subprocess.run(["wget", zip_url, "-O", filename])
    subprocess.run(["unzip", "-y", filename])

def copy_csv_files():
    source_pattern = "./logfiles/app/stat_with_test_result-*"
    destination_dir = "./results/" 

    matching_files = glob.glob(source_pattern)
    for file_path in matching_files:
        shutil.copy(file_path, destination_dir)


def __get_test_cycle_attachments(key):
    response = requests.get(QMetryConst.ENDP_TEST_CYCLES_BASE + key + '/attachment/', headers=QMetryConst.HEADER)
    #print (response.json())
    if response.json()["total"] > 0:
        for objct in response.json()["data"]:
            if objct["name"] == 'logfiles.zip':
                #if seen before. continue
                print (objct["url"], objct["id"])
                download_zip(objct["url"], str(objct["id"]))


# curl  -i 'https://qtmcloud.qmetry.com/rest/api/latest/testcycles/search/' -H 'Content-Type: application/json' 
def __get_test_cycle_list():
     pload = {"filter":{"projectId":"10453","folderId":521282}}
     response = requests.post(QMetryConst.ENDP_TEST_CYCLES_BASE + 'search/', json=pload, headers=QMetryConst.HEADER)
     if response.ok:
        for key_obj in response.json()["data"]:
            __get_test_cycle_attachments(key_obj["key"])
        # Clean up 
        # Extract all the useful data from the logs
        copy_csv_files()
        # Delete Logs and auto_data from directory

     else:
        print ("Error getting the list of test cycle keys response code: " + str(response.status_code))


if __name__ == '__main__':
    #linked = __get_linked_test_cases_of_test_cycle("EEPD-TR-43388")
    #print (linked)
    pp = __get_test_cycle_list()
    #print (pp)
    

