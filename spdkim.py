import argparse
import requests
import json
import datetime
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import os


def genKeys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend()
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    pvtKey = pem.decode()

    public_key = private_key.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    pubKey = pem.decode()

    return pvtKey, pubKey


def storeKeys(outputPath, pvtKey, pubKey):
    with open(outputPath + "/private.key", 'w') as dF:
        dF.write(pvtKey)

    with open(outputPath + "/public.key", 'w') as dF:
        dF.write(pubKey)


def loadKeys(outputPath):
    with open(outputPath + "/private.key", 'r') as dF:
        pvtKey = dF.read()

    with open(outputPath + "/public.key", 'r') as dF:
        pubKey = dF.read()

    return pvtKey, pubKey


def stripKey(key):
    keyArray = key.splitlines()
    keyArrayMod = keyArray[1:-1]
    key = ''.join(keyArrayMod)

    return key


def SPAddDomain(apiKey, domain, selector, pvtKey, pubKey):
    # Modify Keys for API Call
    pvtKey = stripKey(pvtKey)
    pubKey = stripKey(pubKey)

    apiURL = "https://api.sparkpost.com/api/v1/sending-domains"
    apiHeaders = {"Authorization": apiKey, "Content-Type": "application/json"}
    apiData = {
        "domain": domain,
        "dkim": {
            "private": pvtKey,
            "public": pubKey,
            "selector": selector
        }
    }

    response = makeAPICall(apiData, apiURL, apiHeaders)

    return response


def makeAPICall(apiData, apiURL, apiHeaders):
    apiDataJson = json.dumps(apiData)  # Format data
    response = requests.post(apiURL, data=apiDataJson, headers=apiHeaders)  # Make API Call

    return response


def verifyDomain(apiKey, domain):
    """
    DKIM Verifies a Sending Domain in your SparkPost account
    :param apiKey: SparkPost API Key
    :param domain: Sending domain for DKIM verification
    :return: response object
    """
    apiURL = "https://api.sparkpost.com/api/v1/sending-domains/" + domain + "/verify"
    apiHeaders = {"Authorization": apiKey, "Content-Type": "application/json"}
    apiData = {
        "dkim_verify": True
    }

    response = makeAPICall(apiData, apiURL, apiHeaders)

    return response


def addIntermediaryDomain(apiKey, domain, outputPath=None, selector=None):
    """
    Generate DKIM key pair for domain and adds domain to your SparkPost account
    :param apiKey: SparkPost API Key.
    :param domain:  Domain that will be used as Intermediary DKIM domain.
    :param outputPath: (optional) Local path to store DKIM key pair.  Defaults to current working directory.
    :param selector: (optional) Selector to use for DKIM record.  Defaults to "scphMMYY" where MMYY represents the
    current month and year.
    :return: response object
    """
    # Generate Key Pair
    pvtKey, pubKey = genKeys()

    # Store Key Pair
    if outputPath is None:
        outputPath = os.getcwd()
    storeKeys(outputPath, pvtKey, pubKey)

    if selector is None:
        selector = datetime.datetime.now().strftime("scph%m%y")

    # Add Domain to SparkPost
    response = SPAddDomain(apiKey, domain, selector, pvtKey, pubKey)

    return response


def addSendingDomain(apiKey, domain, outputPath=None, selector=None):
    """
    Add customer sending domain to your SparkPost account using the same private and public key pair as the
    intermediary domain.
    :param apiKey: SparkPost API Key
    :param domain: Sending domain that will be added to your SparkPost account
    :param outputPath: (optional) Local path where key pair is stored.  Defaults to current working directory
    :param selector: (optional) Selector to use for DKIM record.  Defaults to "scphMMYY" where MMYY represents the
    current month and year.
    :return:  response object
    """
    # Retrieve Key Pair
    if outputPath is None:
        outputPath = os.getcwd()
    pvtKey, pubKey = loadKeys(outputPath)

    if selector is None:
        selector = datetime.datetime.now().strftime("scph%m%y")

    # Add Domain to SparkPost
    response = SPAddDomain(apiKey, domain, selector, pvtKey, pubKey)

    return response


def clAddDomain(args):
    apiKey = args.apiKey
    domain = args.domain
    outputPath = args.o
    selector = args.s

    if args.intermediary:
        response = addIntermediaryDomain(apiKey, domain, outputPath=outputPath, selector=selector)
    else:
        response = addSendingDomain(apiKey, domain, outputPath=outputPath, selector=selector)

    print(response.reason)


def clVerifyDomain(args):
    apiKey = args.apiKey
    domain = args.domain
    response = verifyDomain(apiKey, domain)

    print(response.reason)


# Import Arguments - Command Line
parser = argparse.ArgumentParser(description="Add and verify intermediary domains and customer domains to your "
                                             "SparkPost account.")
parser.add_argument("apiKey", type=str, help="SparkPost API Key")
subparsers = parser.add_subparsers(help="Action to be taken.  Type [action] -h for more help")
parser_add = subparsers.add_parser("add", help="Add New Domain")
parser_add.add_argument("domain", type=str, help="domain")
parser_add.add_argument("-i", "--intermediary", help="Indicate Domain is Intermediary Domain", action="store_true")
parser_add.add_argument("-o", metavar="Output Location", type=str, help="(optional) Local path where key pair is "
                                                                        "stored.  Defaults to current working "
                                                                        "directory")
parser_add.add_argument("-s", metavar="Selector", type=str,
                        help="(optional) Selector to use for DKIM record.  Defaults to 'scphMMYY' where MMYY "
                             "represents the current month and year")
parser_add.set_defaults(func=clAddDomain)

parser_verify = subparsers.add_parser("verify", help="Verify Domain")
parser_verify.add_argument("domain", type=str, help="Domain to Verify")
parser_verify.set_defaults(func=clVerifyDomain)

args = parser.parse_args()
args.func(args)
