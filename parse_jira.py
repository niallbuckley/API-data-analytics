
import QMetryConst
import requests
import subprocess
import glob
import shutil
import sys


def download_zip(zip_url, id):
    filename = "auto_data_" + id
    subprocess.run(["wget", zip_url, "-O", filename])
    subprocess.run(["unzip", "-o", filename])

def delete_log_files():
    subprocess.run(["rm", "-rf", "logfiles/"])
    source_pattern = "auto_data_*"
    files_to_del = glob.glob(source_pattern)
    for file in files_to_del:
        subprocess.run(["rm", file])


def copy_csv_files():
    source_pattern = "./logfiles/app/stat_with_test_result-*"
    destination_dir = "./results/" 

    matching_files = glob.glob(source_pattern)
    for file_path in matching_files:
        shutil.copy(file_path, destination_dir)


def __get_test_cycle_attachments(key):
    response = requests.get(QMetryConst.ENDP_TEST_CYCLES_BASE + key + '/attachment/', headers=QMetryConst.HEADER)
    if not response.ok:
        print ("ERROR couldn't get attachment for key: ", key, "  ", response.status_code,  " RETRY!!")
        return 1
    
    if response.json()["total"] > 0:
        for objct in response.json()["data"]:
            if objct["name"] == 'logfiles.zip':
                #if seen before. continue
                print (objct["url"], objct["id"])
                download_zip(objct["url"], str(objct["id"]))
    return 0
    


def __get_test_cycle_list(seen_keys):
     pload = {"filter":{"projectId":"10453","folderId":521282}}
     params = '?maxResults=100&startAt=100'
     # &startAt=100
     response = requests.post(QMetryConst.ENDP_TEST_CYCLES_BASE + 'search/' + params,  json=pload, headers=QMetryConst.HEADER)
     if response.ok:
        count = 0
        for key_obj in response.json()["data"]:
            print ("INDEX: ", count, "  KEY: ", key_obj["key"])
            if key_obj["key"] in seen_keys:
                continue
            res = __get_test_cycle_attachments(key_obj["key"])
            if res:
                seen_keys.add(key_obj["key"])
            count += 1

        # Extract all the useful data from the logs
        copy_csv_files()

        # Delete useless logs and auto_data from directory
        delete_log_files()
        return seen_keys

     else:
        print ("Error getting the list of test cycle keys response code: " + str(response.status_code))
        sys.exit(1)


if __name__ == '__main__':
    seen_keys = set()

    try:
        with open('seen_keys.txt', 'r') as file:
            for line in file:
                seen_keys.add(line.strip())
    except FileNotFoundError:
        open('seen_keys.txt', 'w').close()

    updated_seen_keys = __get_test_cycle_list(seen_keys)

    with open('seen_keys.txt', 'w') as file:
        for key in updated_seen_keys:
            file.write(f"{key}\n")
