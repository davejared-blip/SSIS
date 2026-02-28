COLLEGES = {
    "CCS": {
        "name": "College of Computer Studies",
        "programs": {
            "BSCS": "BS Computer Science",
            "BSIT": "BS Information Technology",
            "BSIS": "BS Information Systems",
            "BSCA": "BS Computer Applications"
        }
        
    },
    "CSM": {
        "name": "College of Science and Mathematics",
        "programs": {
            "BSMarB": "BS Marine Biology",
            "BSBio": "BS Biology",
            "BSChem": "BS Chemistry",
            "BSM": "BS Mathematics",
            "BSPhy": "BS Physics",
            "BSMicB": "BS Microbiology"
        }
    },
    "COE": {
        "name": "College of Engineering",
        "programs": {
            "BSCE": "BS Civil Engineering",
            "BSME": "BS Mechanical Engineering",
            "BSCpE": "BS Computer Engineering",
            "BSECE": "BS Electronics Engineering",
            "BSPetE": "BS Petroleum Engineering"
        }
    },
    "CASS": {
        "name": "College of Arts and Social Sciences",
        "programs": {
            "BAEL": "BA English Language",
            "BAFL": "BA Filipino Language",
            "BSPsy": "BS Psychology",
            "BSHis": "BS History"
        }
    }
}

# Helper function 
def get_college_name(code):
    return COLLEGES.get(code, {}).get("name", "Unknown College")

def get_program_name(code):
    for college in COLLEGES.values():
        if code in college["programs"]:
            return college["programs"][code]
    return "Unknown Program"