import requests
import json


def identify_plant(image_file, api_key):
    # API endpoint
    url = "https://my-api.plantnet.org/v2/identify/all"

    # Prepare the files for the POST request
    files = [("images", ("image.jpg", image_file, "image/jpeg"))]

    # Prepare the data for the POST request
    data = {"organs": ["auto"]}

    # Prepare the parameters
    params = {
        "include-related-images": "false",
        "no-reject": "false",
        "lang": "en",
        "api-key": api_key,
    }

    # Make the POST request
    response = requests.post(url, params=params, files=files, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()

        # Extract and return the best match
        if result["results"]:
            best_match = result["results"][0]["species"]["scientificNameWithoutAuthor"]
            score = result["results"][0]["score"]
            return {"best_match": best_match, "score": score}
        else:
            return {"best_match": None, "score": None}
    else:
        return {"best_match": None, "score": None}