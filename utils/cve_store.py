'''
A script that will query vulners.com/api for cve data related to given operating systems.
The data is returned in a valid json format for use in the cve_scan_v2 module. The json file
is stored at the local directory under <os_name>_<version>.json. Inputs must be in the form
os-version, like 'centos-7' or 'ubuntu-16.04' etc.

usage: # python cve_store.py (<os-version>) [<os-version> ...]
'''
from zipfile import ZipFile
import os
import sys
import requests

def main():
    '''
    Tries to save cve scans for inputs. Specify type and version.
        Ex: # python cve_store.py centos-7 ubuntu-16.04
    '''
    if len(sys.argv) == 1:
        print "No inputs were given."
    for distro in sys.argv[1:]:
        print
        try:
            _save_json(distro)
        except Exception, exc:
            print 'Error saving: %s' % distro
            print exc


def _save_json(distro):
    '''
    Returns json from vulner.com api for specified distro.
    Exceptions thrown are caught by main()
    '''
    split = distro.split('-')
    if len(split) != 2:
        raise Exception('%s is improperly formatted.' % distro)
    version = split[1]
    distro_name = split[0]
    print 'Getting cve\'s for %s version %s' % (distro_name, version)
    url_final = 'http://www.vulners.com/api/v3/archive/distributive/?os=%s&version=%s' \
                                                                % (distro_name, version)
    cve_query = requests.get(url_final)
    # Filenames returned don't contain periods.
    version = version.replace('.', '')
    _zip = '%s_%s.zip' % (distro_name, version)
    _json = '%s_%s.json' % (distro_name, version)
    # Confirm that the request was valid.
    if cve_query.status_code != 200:
        raise Exception('Bad Request for url: %s' % url_final)
    # Save vulners zip attachment in cache location and extract json
    with open(_zip, 'w') as zip_attachment:
        zip_attachment.write(cve_query.content)
    zip_file = ZipFile(_zip)
    zip_file.extractall(os.path.dirname(_zip))
    os.remove(_zip)
    print 'Saved: %s' % _json


main()
