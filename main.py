# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, render_template, request
import requests
import google.auth

app = Flask(__name__)

AIRTABLE_BASE_ID = "appQDubV8j5rsWjq3"

# This would be in an environment variable in a real application
AIRTABLE_API_KEY = "keykZdyBpsSdLqkFR"

# Authenticates into the airtable
headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

@app.route('/', methods=['GET', 'POST'])
def get_letter_form_post():
    lower = "INVALID"
    upper = "INVALID"
    lang = "INVALID"
    index = "INVALID"
    if request.method == 'POST':
        # Gets values from HTML page
        lang_table = request.form['lang']
        alpha_index = request.form['alpha_index']

        # Check if HTML form values are empty
        if lang_table and alpha_index:
            # Check if index entered by user is in range for selected alphabet
            if (lang_table == 'English' and int(alpha_index) <= 26) or \
                (lang_table == 'Spanish' and int(alpha_index) <= 27) or \
                (lang_table == 'Ijaw' and int(alpha_index) <= 35) or \
                (lang_table == 'Yoruba' and int(alpha_index) <= 25) or \
                (lang_table == 'Igbo' and int(alpha_index) <= 36):
                # Construct URL to get data from airtable
                # See https://codepen.io/airtable/pen/rLKkYB for Airtable URL encoding
                url = "https://api.airtable.com/v0/" + \
                    AIRTABLE_BASE_ID + "/" + \
                    lang_table + \
                    "?fields%5B%5D=Lowercase&fields%5B%5D=Uppercase&filterByFormula=Index%3D" + \
                    alpha_index
                # Gets data from airtable
                r = requests.get(url, headers=headers)

                # Selects lowercase/uppercase letter from record
                lower = r.json()["records"][0]["fields"]["Lowercase"]
                upper = r.json()["records"][0]["fields"]["Uppercase"]

            # Send back user selected index to HTML page (even if index out of range is given)
            index=alpha_index
        
        # Send back user selected language to HTML page (even if no index is given)
        lang=lang_table

        # Render the HTML page
        return render_template("index.html", upper=upper, lower=lower, lang=lang, index=index)
    # If not POST method, just render the HTML page with no arguments
    else:
        return render_template("index.html")


if __name__ == '__main__':
    import os
    app.run(debug=True, threaded=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)))
