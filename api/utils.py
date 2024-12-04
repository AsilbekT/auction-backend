from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
import re
import usaddress



ordinal_map = {
    "First": "1st",
    "Second": "2nd",
    "Third": "3rd",
    "Fourth": "4th",
    "Fifth": "5th",
    "Sixth": "6th",
    "Seventh": "7th",
    "Eighth": "8th",
    "Ninth": "9th",
    "Tenth": "10th",
    "Eleventh": "11th",
    "Twelfth": "12th",
    "Thirteenth": "13th",
    "Fourteenth": "14th",
    "Fifteenth": "15th",
    "Sixteenth": "16th",
    "Seventeenth": "17th",
    "Eighteenth": "18th",
    "Nineteenth": "19th",
    "Twentieth": "20th",
}

numbers = {
    'One': '1',
    'Two': '2',
    'Three': '3',
    'Four': '4',
    'Five': '5',
    'Six': '6',
    'Seven': '7',
    'Eight': '8',
    'Nine': '9',
    'Ten': '10',
    'Eleven': '11',
    'Twelve': '12',
    'Thirteen': '13',
    'Fourteen': '14',
    'Fifteen': '15',
    'Sixteen': '16',
    'Seventeen': '17',
    'Eighteen': '18',
    'Nineteen': '19',
    'Twenty': '20'
}

street_abbreviations = {
    "Street": "St",
    "Road": "Rd",
    "Avenue": "Ave",
    "Lane": "Ln",
    "Drive": "Dr",
    "Circle": "Cir",
    "Court": "Ct",
    "Way": "Way",
    "Place": "Pl",
    "Terrace": "Terr",
    "Boulevard": "Blvd",
    "Parkway": "Pkwy",
    "Estates": "Est",
    "Square": "Sq",
    "Highway": "Hwy",
    "North": "N",
    "South": "S",
    "West": "W",
    "East": "E",
    "Trail": "Trl",
    "Plaza": "Plz",
    "Ridge": "Rdg",
    "Boardwalk": "Bdwl",
    "Alley": "Aly",
    "Driveway": "Drvwy",
    "Route": "Rte",
    "Av" : "Ave"
}

us_state_abbreviations = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

def standardize_address(address):
    if not address:
        return None

    try:
        address = convert_types(address, numbers)
        parsed_address, address_type = usaddress.tag(address)

        components = {
            'AddressNumber': parsed_address.get('AddressNumber', '').split("-")[0],
            'StreetNamePreDirectional': convert_types(parsed_address.get('StreetNamePreDirectional', ''), street_abbreviations).title(),
            'StreetName': convert_types(parsed_address.get('StreetName', ''), ordinal_map).title(),
            'StreetNamePostType': convert_types(parsed_address.get('StreetNamePostType', ''), street_abbreviations).title(),
            'StreetNamePostDirectional': parsed_address.get('StreetNamePostDirectional', '').title(),
            'PlaceName': convert_types(parsed_address.get('PlaceName', ''), ordinal_map).title(),
            'StateName': convert_types(parsed_address.get('StateName', ''), us_state_abbreviations).upper(),
            'ZipCode': parsed_address.get('ZipCode', '').split("-")[0],
            'OccupancyIdentifier': convert_types(parsed_address.get('OccupancyIdentifier', ''), ordinal_map).replace("No","").title(),
            'SubaddressIdentifier': parsed_address.get('SubaddressIdentifier', '').title(),
            'SubaddressType': parsed_address.get('SubaddressType', '').title(),
        }

        standardized_address = " ".join(filter(None, components.values())).strip()
        standardized_address = re.sub(r'\b(Ste|Unit|Floor)\b', '', standardized_address, re.IGNORECASE)
        standardized_address = re.sub(r'[.#,]', '', standardized_address, re.IGNORECASE)
        standardized_address = re.sub(r'\s+', ' ', standardized_address).strip()
        return remove_suffix(standardized_address)

    except usaddress.RepeatedLabelError as e:
        print(f"Failed to parse address '{address}' with error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in standardize_address with address '{address}': {e}")
        return None


def convert_types(address, abbreviations):
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, abbreviations.keys())) + r')\b', re.IGNORECASE)
    
    def replace_match(match):
        full_name = match.group(0)
        return abbreviations.get(full_name.title(), full_name)

    return pattern.sub(replace_match, address)

def remove_suffix(text):
    pattern = r'\b(\d+)(st|nd|rd|th)\b'
    result = re.sub(pattern, r'\1', text, flags=re.IGNORECASE)
    return result


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'error': False,
            'message': 'Data fetched successfully',
            'data': {
                'results': data,
                'pagination': {
                    'count': self.page.paginator.count,
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                }
            }
        })


def response_success(message, data):
    return Response({
        'error': False,
        'message': message,
        'data': data
    }, status=status.HTTP_200_OK)

def response_error(message, errors, http_status):
    return Response({
        'error': True,
        'message': message,
        'details': errors
    }, status=http_status)


def check_priority(new_source_name, existing_obj, is_new_auction):
    priority_names = {
        "fl": 9, "asap": 8, "njcourt": 7, "salesweb": 6, "xome": 5, 
        "realtybid": 4, "foreclosure.com": 3, "auction.com": 2, "bids": 1
        }

    # Higher number means higher priority
    if not existing_obj:
        return False, "No existing object provided."

    if not is_new_auction and not existing_obj.is_auction:
        return False, "Neither is an auction."

    existing_priority = priority_names.get(existing_obj.source_name.lower(), 0)
    new_priority = priority_names.get(new_source_name.lower(), 0)


    if new_priority == existing_priority:
        if is_new_auction != existing_obj.is_auction:
            return True, "The priority is the same, but it is a surplus"
    elif new_priority > existing_priority:
        if is_new_auction == existing_obj.is_auction:
            return True, "The address exists, but the new source has a higher priority."
        
    return False, "The new object was not created"
    

