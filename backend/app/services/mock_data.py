"""
Realistic mock data for development without API keys.
Represents a 2018 Ford Focus with a moderately interesting MOT history.
"""

DVLA_MOCK = {
    "registrationNumber": "BD18SMO",
    "make": "FORD",
    "colour": "GREY",
    "fuelType": "PETROL",
    "engineCapacity": 998,
    "yearOfManufacture": 2018,
    "taxStatus": "Taxed",
    "motStatus": "Valid",
    "co2Emissions": 99,
    "dateOfLastV5CIssued": "2021-06-14",
    "monthOfFirstRegistration": "2018-03",
}

DVSA_MOCK = {
    "registration": "BD18SMO",
    "make": "FORD",
    "model": "FOCUS",
    "firstUsedDate": "2018-03-01",
    "fuelType": "Petrol",
    "primaryColour": "Grey",
    "motTests": [
        {
            "completedDate": "2024-03-15T10:22:00",
            "testResult": "PASSED",
            "expiryDate": "2025-03-14",
            "odometerValue": "62340",
            "odometerUnit": "mi",
            "motTestNumber": "847392018473",
            "rfrAndComments": [
                {
                    "text": "Tyre worn close to legal limit/worn on edge (5.2.3 (e))",
                    "type": "ADVISORY",
                    "dangerous": False,
                },
                {
                    "text": "Front brake disc worn, corroded (3.5.1 (b) (i))",
                    "type": "ADVISORY",
                    "dangerous": False,
                },
            ],
        },
        {
            "completedDate": "2023-03-08T14:05:00",
            "testResult": "PASSED",
            "expiryDate": "2024-03-07",
            "odometerValue": "48120",
            "odometerUnit": "mi",
            "motTestNumber": "738291847362",
            "rfrAndComments": [
                {
                    "text": "Tyre worn close to legal limit/worn on edge (5.2.3 (e))",
                    "type": "ADVISORY",
                    "dangerous": False,
                },
                {
                    "text": "Offside front suspension arm bush deteriorated but not causing excessive movement (5.3.4 (a) (i))",
                    "type": "ADVISORY",
                    "dangerous": False,
                },
                {
                    "text": "Nearside front lower suspension arm has slight play in pivot (5.3.4 (a) (i))",
                    "type": "ADVISORY",
                    "dangerous": False,
                },
            ],
        },
        {
            "completedDate": "2022-03-20T09:45:00",
            "testResult": "FAILED",
            "expiryDate": None,
            "odometerValue": "35890",
            "odometerUnit": "mi",
            "motTestNumber": "629183746251",
            "rfrAndComments": [
                {
                    "text": "Nearside front tyre has a cut in excess of 25mm or 10% of section width to ply or cord (5.2.3 (b))",
                    "type": "FAIL",
                    "dangerous": True,
                },
                {
                    "text": "Exhaust emission CO content at fast idle exceeds manufacturer's specification (8.2.2 (a))",
                    "type": "FAIL",
                    "dangerous": False,
                },
                {
                    "text": "Nearside rear brake pipe corroded, resulting in severe pitting (3.6.1 (a) (i))",
                    "type": "FAIL",
                    "dangerous": False,
                },
            ],
        },
        {
            "completedDate": "2022-03-21T11:30:00",
            "testResult": "PASSED",
            "expiryDate": "2023-03-20",
            "odometerValue": "35912",
            "odometerUnit": "mi",
            "motTestNumber": "629183746299",
            "rfrAndComments": [
                {
                    "text": "Offside rear coil spring has slight corrosion (5.3.6 (a) (i))",
                    "type": "ADVISORY",
                    "dangerous": False,
                },
            ],
        },
        {
            "completedDate": "2021-03-10T13:00:00",
            "testResult": "PASSED",
            "expiryDate": "2022-03-09",
            "odometerValue": "22450",
            "odometerUnit": "mi",
            "motTestNumber": "510928374651",
            "rfrAndComments": [],
        },
    ],
}

VALUATION_MOCK = {
    "webuyanycar": 7200.0,
    "parkers_retail": 9995.0,
    "parkers_private": 8750.0,
    "source_note": "Mock valuations — for development only",
}

RECALLS_MOCK = [
    {
        "make": "FORD",
        "concern": "The front seat belt pre-tensioner may not operate correctly in the event of a collision",
        "remedy": "Dealers will inspect and replace the front seat belt pre-tensioners as necessary, free of charge",
        "launch_date": "2020-11-04",
    }
]
