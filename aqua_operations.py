import requests
import os
import urllib3
import time
import json
import csv
import sys
from datetime import date
import urllib.parse
from urllib.parse import urlparse

# Disables the SSL Insecure Warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# sets date for file output later
today = date.today()


##### SCRIPT ENHANCMENTS #############
# Colors to enhance text.
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Leading animation, just for fun.
def loading_animation_lol():
    bar = [
        " [=     ]",
        " [ =    ]",
        " [  =   ]",
        " [   =  ]",
        " [    = ]",
        " [     =]",
        " [    = ]",
        " [   =  ]",
        " [  =   ]",
        " [ =    ]",
    ]
    i = 0

    while True:
        print(bar[i % len(bar)], end="\r")
        time.sleep(.2)
        i += 1
        if i == 10:
            break


# Validation of user input
def check_user_input_is_num(choice):
    while True:
        try:
            # Convert it into integer
            val = int(choice)
            return (True)
        except ValueError:
            return (False)


def clean_screen():
    os.system('cls' if os.name == 'nt' else "clear")


def check_dir(file_name):
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        print("Setting Up Directory for Report...")
        os.makedirs(directory)
        time.sleep(0)
        print(f"Directory Setup: {Color.OKGREEN}SUCCESS{Color.ENDC}\n")


#### CORE VALUES TO CHANGE #######
class AquaValues:
    registries = ("")
    registries_count = len(registries)
    username = ""
    password = ""
    headers = {
        "Accept": "application/json",
    }
    urls = {"Prod": "https://{URL}.com/api/v2",
            "Preprod": "https://{URL}.com/api/v2"
            }


class ProgramOptions:
    current_options = (f"See Registered Images - {Color.FAIL}NOT FUNCTIONING{Color.ENDC}",
                       f"Register a New Image - {Color.FAIL}NOT FUNCTIONING{Color.ENDC}",
                       f"See Image Information - {Color.FAIL}NOT FUNCTIONING{Color.ENDC}",
                       f"Get Image Vulnerabilities",
                       )
    current_options_count = len(current_options)


class urls:
    PROD = "https://{URL}
    .com/api/v2"
    PREPROD = "https://{URL}.com/api/v2"


################# TEST get with predefined endpoint ###################
def get_image_vulnerabilities_test():
    url = "https://URL.com/api/v2/images/{REGISTRY}/{REPO}/{IMAGE}/vulnerabilities"
    try:
        response = requests.request("GET", url, headers=AquaValues.headers, verify=False,
                                    auth=(AquaValues.username, AquaValues.password))
    except:
        print(f"{Color.FAIL}ERROR{Color.ENDC}: Request is formatted bad, check code.")
        sys.exit()
    status = response.status_code
    response_status = response_handler(status)
    if response_status == True:
        process_vulnerabilities(response)
    else:
        get_image_vulnerabilities_test(url)


############## CORE COMPONENTS ###############

def url_parse(url):
    global repo
    global tag
    global cleaned_url

    parsed_url = urlparse(url)
    base = parsed_url.netloc
    path_list = parsed_url.fragment.split("/")
    registry = urllib.parse.unquote(path_list[2])
    repo_tag = urllib.parse.unquote(path_list[3])
    repo_tag = repo_tag.split(":")
    repo = repo_tag[0]
    tag = repo_tag[1]
    print(f"URL Parsing: {Color.OKGREEN}SUCCESS{Color.ENDC}\n")
    cleaned_url = f"https://{base}/api/v2/images/{registry}/{repo}/{tag}/vulnerabilities"
    print("Checking URL Validity...")
    print(f"Registry: {registry}\n Repo: {repo}\n Tag: {tag}")
    print(cleaned_url)
    time.sleep(0)
    if registry in AquaValues.registries:
        print(f"Registry Check: {Color.OKGREEN}SUCCESS{Color.ENDC}\n")
    else:
        print(f"Registry Check: {Color.FAIL}FAILED{Color.ENDC}\n")
        print("You appear to trying an invalid URL. For more information, reference the URL section in the README.")
        sys.exit()


def system_arg_processor(args):
    print(f"================ WELCOME TO THE BETTER {Color.OKBLUE}AQUA{Color.ENDC}! ================ \n")
    print("Attempting to Read Arguments...")
    print(f"Reading Arguments: {Color.OKGREEN}SUCCESS{Color.ENDC}\n")

    time.sleep(0)
    if args[1].lower() == '-t':
        clean_screen()
        get_image_vulnerabilities_test()
    elif args[1].lower() == '-u':
        print("Attempting to Parse URL...")
        url = args[2]
        url_parse(url)
    else:
        print("Invalid Arguments. Exiting....")
        sys.exit()


# Registry selection that depends on hardcoded values (Eventually should be a pull)
def registry_selector():
    iteration = 0
    print("Select a Registry")
    for x in AquaValues.registries:
        print(f"[{iteration}] - {x}")
        iteration += 1
    while True:
        choice = input("Input: ")
        input_check = check_user_input_is_num(choice)
        if input_check == True:
            if int(choice) in range(0, AquaValues.registries_count):
                registry = AquaValues.registries[int(choice)]
                return (registry)
            else:
                print(f"\nThat was not a valid choice.. Select 0 - {AquaValues.registries_count - 1}\n")
                continue
        else:
            print(f"\nThat was not a valid choice.. Select 0 - {AquaValues.registries_count - 1}\n")
            continue


def acknowledge_vulnerabilities(vuln_file_path):
    print("TIME TO ADD EXCEPTION?")
    print(vuln_file_path)


def process_vulnerabilities(response):
    global repo
    global tag

    if len(args) > 3:
        if args[3] == "-csv":
            choice = "2"
        elif args[3] == "-json":
            choice = "1"
        else:
            pass
    else:
        while True:
            print(
                "What would you like to do? \n[1] Output Vulnerabilities to JSON file\n[2] Output Vulnerabilities to CSV ")
            choice = input("Input: ")
            while True:
                input_check = check_user_input_is_num(choice)
                if input_check == True:
                    break
                else:
                    print("That is not a valid choice. Try again.")
                    continue
            if choice == "2" or "1":
                break
            else:
                print("Bad input")
                continue
    if choice == "2":
        try:
            repo = repo.split("/")[-1]
            filename = f"{repo}_{tag}_{today.strftime('%m-%d-%y')}"
            output_path = f"./Aqua Vulnerability Reports/{repo}/{filename}"
            check_dir(output_path)

        except:
            filename = "test"
            output_path = f"./Aqua Vulnerability Reports/{filename}"

        json_data = response.json()
        vulnerabilities_json = json_data['result']
        csv_file = open(f"{output_path}.csv", 'w+', newline='')
        csv_writer = csv.writer(csv_file)
        count = 0
        for item in vulnerabilities_json:
            if count == 0:
                header_csv = item.keys()
                csv_writer.writerow(header_csv)
                count += 1
            csv_writer.writerow(item.values())
        csv_file.close()
        print("Saving Vulnerability CSV....")
        loading_animation_lol()
        loading_animation_lol()
        print(f"Report Saved: {Color.OKGREEN}SUCCESS{Color.ENDC}\n")
        acknowledge_vulnerabilities(output_path)
    elif choice == "1":
        try:
            repo = repo.replace("/", "-")
            filename = f"{tag} - {today.strftime('%m-%d-%y')}"
            output_path = f"./Aqua Vulnerability Reports/{repo}/{filename}"
            check_dir(output_path)
        except:
            output_path = f"./Aqua Vulnerability Reports/report"
            check_dir(output_path)
        json_response = response.json()
        with open(f"{output_path}.json", 'w') as json_file:
            json.dump(json_response, json_file)
            print("Saving Vulnerability JSON File....")
            loading_animation_lol()
            loading_animation_lol()
            print(f"Report Saved: {Color.OKGREEN}SUCCESS{Color.ENDC}\n")
        acknowledge_vulnerabilities(output_path)
    else:
        sys.exit()


def response_handler(status, url):
    if status == 200:
        print(f"Received {Color.OKGREEN}OK{Color.ENDC}\n")
        time.sleep(0)
        return (True)
    else:
        print(
            f"Received {Color.FAIL}FAILURE{Color.ENDC} Code - \nCheck credential permissions and ensure repository and image tag are spelled correctly.\n")
        print(status)
        print(url)


def get_image_vulnerabilities_interactive(url):
    clean_screen()
    registry = registry_selector()
    clean_screen()
    print(
        f"ENDPOINT: {url}" + f"/images/{registry}\n\nNOTE: Be aware all operations are currently case sensitive and require accurate spelling.\n")
    repo = input("What repository?: ")
    tag = input("What is the image tag?: ")
    url = url + "/images" + "/" + registry + "/" + repo + "/" + tag + "/vulnerabilities"
    print("\nAttempting to pull vulnerability data for....")
    print(f"Registry: {registry}")
    print(f"Repository: {repo}")
    print(f"Image Tag: {tag}\n")
    loading_animation_lol()
    try:
        response = requests.request("GET", url, headers=AquaValues.headers, verify=False,
                                    auth=(AquaValues.username, AquaValues.password))
    except:
        print(f"{Color.FAIL}ERROR{Color.ENDC}: Request is formatted bad, check code.")
        sys.exit()
    status = response.status_code
    response_status = response_handler(status)
    process_vulnerabilities(response)


def get_image_vulnerabilities_quick(url):
    print("Sending GET Request to URL...")
    try:
        response = requests.request("GET", url, headers=AquaValues.headers, verify=False,
                                    auth=(AquaValues.username, AquaValues.password))
    except:
        print(f"{Color.FAIL}ERROR{Color.ENDC}: Request is formatted bad, check code.")
        sys.exit()
    status = response.status_code
    response_status = response_handler(status, url)
    process_vulnerabilities(response)


def operation_selector(url):
    clean_screen()
    print(f"ENDPOINT: {url}")
    print("\nWhat would you like to do?")
    iteration = 0
    for x in ProgramOptions.current_options:
        print(f"[{iteration}] - {x}")
        iteration += 1
    while True:
        choice = input("\nInput: ")
        input_check = check_user_input_is_num(choice)
        if input_check == True:
            if int(choice) in range(0, ProgramOptions.current_options_count):
                break
            else:
                print(f"\nThat was not a valid choice.. Enter 0 - {ProgramOptions.current_options_count - 1}")
                continue
            break
        else:
            print(f"\nThat was not a valid choice.. Enter 0 - {ProgramOptions.current_options_count - 1}")
            continue

    if int(choice) == 3:
        get_image_vulnerabilities_interactive(url)

    else:
        print("That option isn't working")
        time.sleep(0)
        clean_screen()
        operation_selector(url)


def initial_prompt():
    print("\nWhat environment are you trying to use?\n[1] Production\n[2] Pre-production\n")
    env = input("Input: ")
    if env == "Production" or env == "Prod" or env == "1":
        print(
            f"\nAre you intending to view {Color.OKBLUE}Production{Color.ENDC} data? ({Color.OKGREEN}Y{Color.ENDC}/{Color.FAIL}N{Color.ENDC}) \n")
        env_validate = input("Input: ")
        if env_validate == "y" or env_validate == "Y":
            url = urls.PROD
            operation_selector(url)
        else:
            clean_screen()
            initial_prompt()
    elif env == "Pre-production" or env == "Preprod" or env == "2":
        print(
            f"\nAre you intending to view {Color.OKBLUE}Pre-production{Color.ENDC} data? ({Color.OKGREEN}Y{Color.ENDC}/{Color.FAIL}N{Color.ENDC}) \n")
        env_validate = input("Input: ")
        if env_validate == "y" or env_validate == "Y":
            url = urls.PREPROD
            operation_selector(url)
        else:
            clean_screen()
            initial_prompt()
    else:
        print("Thats not a valid option...... Try again")
        time.sleep(0)
        clean_screen()
        initial_prompt()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv
        args = sys.argv
        system_arg_processor(args)
        get_image_vulnerabilities_quick(cleaned_url)
        print(f"{Color.OKCYAN}ALL ACTIONS COMPLETED!{Color.ENDC}")
    else:
        print("\n============= Welcome to the better Aqua! =============")
        time.sleep(0)
        initial_prompt()
