#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import urllib2
import xml.etree.ElementTree as ET

"""
Really simple OAI client. Returns a list of ElementTree Element objects that contain
the metadata element for each harvested record. Clients are to keep calling harvest() until
is_done return True.
"""

RESUMPTION_TOKEN_FILE = "resumption_token"

class OaiClient:
    def __init__(self, url, from_date=None):
        self.baseUrl = url
        self.resumption_token = None
        self.is_initial_request = True
        self.from_date = from_date

    def harvest(self, set, metadataPrefix):
        url = self.baseUrl + "?verb=ListRecords"
        if self.resumption_token != None:
            url = url + "&resumptionToken=" + self.resumption_token
        else:
            url = url + "&set=" + set + "&metadataPrefix=" + metadataPrefix
            if self.from_date:
                url = url + "&from=" + self.from_date
	print(url)
        f = urllib2.urlopen(url)
        response = f.read()
        f.close()
        [records, resumption_token] = parseResponse(response)
        if resumption_token == '':
            self.resumption_token = None
        elif resumption_token != None:
            self.resumption_token = resumption_token
            persist_resumption_token(resumption_token)

        self.is_initial_request = False

        if len(records) > 0:
            return records
        else:
            return None


    def is_done(self):
        return (not self.is_initial_request and self.resumption_token == None)


# write rs to a file so we can resume harvesting after the script gets killed.
def persist_resumption_token(resumption_token):
    rs_file = open(RESUMPTION_TOKEN_FILE, 'w')
    rs_file.write(resumption_token)
    rs_file.close()


def parseResponse(response):

    root = ET.fromstring(response)

    records = []
    resumption_token = None
    for m in root.iter('{http://www.openarchives.org/OAI/2.0/}metadata'):
        records.append(m)
    for r in root.iter('{http://www.openarchives.org/OAI/2.0/}resumptionToken'):
        if len(r.text) > 0:
            resumption_token = r.text
            break

    return [records, resumption_token]


