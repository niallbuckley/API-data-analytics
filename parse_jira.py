import os
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


def copy_csv_file(qmetry_key):
    file_path = "./logfiles/request_stats_new.csv"
    destination_dir = "./results/" 
    # Extract the filename from the file path
    filename = os.path.basename(file_path)

    # Split the filename into basename and extension
    basename, extension = os.path.splitext(filename)

    # Add qmetry key to the end of the basename
    new_basename = basename + "-" + str(qmetry_key)

    # Combine the new basename and extension to create the new filename
    new_filename = new_basename + extension

    # Join the destination directory path and the new filename
    new_file_path = os.path.join(destination_dir, new_filename)

    shutil.copy(file_path, new_file_path)


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
     params = '?maxResults=100'
     # &startAt=100
     response = requests.post(QMetryConst.ENDP_TEST_CYCLES_BASE + 'search/' + params,  json=pload, headers=QMetryConst.HEADER)
     if response.ok:
        count = 0
        for key_obj in response.json()["data"]:
            print ("INDEX: ", count, "  KEY: ", key_obj["key"])
            if key_obj["key"] in seen_keys:
                print (key_obj["key"], " seen before -- SKIPPING")
                continue
            res = __get_test_cycle_attachments(key_obj["key"])
            if res == 0:
                seen_keys.add(key_obj["key"])
		try:
                    # Extract all the useful data from the logs
		    copy_csv_file(key_obj["key"])
		    count += 1
		except Exception as e:
		    print("Error no csv file! ", e)
		print (key_obj["key"], " added to seen keys!")

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
