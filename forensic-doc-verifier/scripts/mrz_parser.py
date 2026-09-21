#!/usr/bin/env python3
"""
ICAO Doc 9303 Machine Readable Zone (MRZ) Parser & Check Digit Validator.
Supports TD1 (3x30), TD2 (2x36), and TD3 (2x44) formats.
Zero external dependencies.
"""

from __future__ import annotations
import json
import re
import sys
from typing import Dict, List, Optional, Tuple, Any

WEIGHTS = [7, 3, 1]

def char_to_val(c: str) -> int:
    """Map MRZ character to numeric value according to ICAO Doc 9303."""
    c = c.upper()
    if c == '<':
        return 0
    if c.isdigit():
        return int(c)
    if 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 10
    raise ValueError(f"Invalid MRZ character: '{c}'")

def calculate_check_digit(data: str) -> str:
    """Compute 7-3-1 modulus 10 check digit for a string."""
    total = 0
    for i, char in enumerate(data):
        val = char_to_val(char)
        weight = WEIGHTS[i % 3]
        total += val * weight
    return str(total % 10)

def verify_field(field_data: str, expected_digit: str) -> bool:
    """Verify field against provided check digit."""
    if not expected_digit.isdigit():
        return False
    return calculate_check_digit(field_data) == expected_digit

class MRZParser:
    """Parser for ICAO 9303 Machine Readable Zones."""

    @staticmethod
    def clean_mrz(raw_text: str) -> List[str]:
        """Normalize and filter raw text into uppercase MRZ lines."""
        lines = [line.strip().upper() for line in raw_text.strip().splitlines() if line.strip()]
        cleaned = []
        for line in lines:
            # Filter out extraneous symbols, keep only A-Z, 0-9, and <
            filtered = re.sub(r'[^A-Z0-9<]', '', line)
            if filtered:
                cleaned.append(filtered)
        return cleaned

    @classmethod
    def parse(cls, raw_text: str) -> Dict[str, Any]:
        lines = cls.clean_mrz(raw_text)
        if not lines:
            return {"valid": False, "error": "Empty or unreadable MRZ content"}

        if len(lines) == 2:
            len1, len2 = len(lines[0]), len(lines[1])
            if len1 == 44 and len2 == 44:
                return cls._parse_td3(lines[0], lines[1])
            elif len1 == 36 and len2 == 36:
                return cls._parse_td2(lines[0], lines[1])
            else:
                return {"valid": False, "error": f"Invalid 2-line MRZ lengths: {len1}, {len2}"}
        elif len(lines) == 3:
            lens = [len(l) for l in lines]
            if lens == [30, 30, 30]:
                return cls._parse_td1(lines[0], lines[1], lines[2])
            else:
                return {"valid": False, "error": f"Invalid 3-line TD1 MRZ lengths: {lens}"}
        else:
            return {"valid": False, "error": f"Unexpected line count: {len(lines)} (expected 2 or 3)"}

    @staticmethod
    def _parse_td3(line1: str, line2: str) -> Dict[str, Any]:
        """Parse TD3 (Passport) format (2 lines x 44 chars)."""
        doc_code = line1[0:2].replace('<', '')
        issuing_country = line1[2:5].replace('<', '')
        name_field = line1[5:44]

        # Extract names
        names = name_field.split('<<', 1)
        surname = names[0].replace('<', ' ').strip()
        given_names = names[1].replace('<', ' ').strip() if len(names) > 1 else ""

        # Line 2 fields
        doc_num_raw = line2[0:9]
        doc_num = doc_num_raw.replace('<', '')
        doc_num_cd = line2[9]
        nationality = line2[10:13].replace('<', '')
        dob_raw = line2[13:19]
        dob_cd = line2[19]
        sex = line2[20].replace('<', 'X')
        expiry_raw = line2[21:27]
        expiry_cd = line2[27]
        optional_raw = line2[28:42]
        optional_cd = line2[42]
        composite_cd = line2[43]

        # Check digits
        doc_num_valid = verify_field(doc_num_raw, doc_num_cd)
        dob_valid = verify_field(dob_raw, dob_cd)
        expiry_valid = verify_field(expiry_raw, expiry_cd)
        
        # Optional check digit (valid if digit checks out or both are filler)
        optional_valid = True
        if optional_cd.isdigit():
            optional_valid = verify_field(optional_raw, optional_cd)

        # Composite check digit calculation: Line 2 chars 1-10 + 14-20 + 22-43 (indices 0:10, 13:20, 21:43)
        composite_data = line2[0:10] + line2[13:20] + line2[21:43]
        composite_valid = verify_field(composite_data, composite_cd)

        all_valid = doc_num_valid and dob_valid and expiry_valid and optional_valid and composite_valid

        return {
            "valid": all_valid,
            "format": "TD3",
            "document_code": doc_code,
            "issuing_state": issuing_country,
            "surname": surname,
            "given_names": given_names,
            "document_number": doc_num,
            "nationality": nationality,
            "date_of_birth": dob_raw,
            "sex": sex,
            "expiry_date": expiry_raw,
            "optional_data": optional_raw.replace('<', ''),
            "check_digits": {
                "document_number": {"expected": doc_num_cd, "computed": calculate_check_digit(doc_num_raw), "valid": doc_num_valid},
                "date_of_birth": {"expected": dob_cd, "computed": calculate_check_digit(dob_raw), "valid": dob_valid},
                "expiry_date": {"expected": expiry_cd, "computed": calculate_check_digit(expiry_raw), "valid": expiry_valid},
                "composite": {"expected": composite_cd, "computed": calculate_check_digit(composite_data), "valid": composite_valid}
            }
        }

    @staticmethod
    def _parse_td1(line1: str, line2: str, line3: str) -> Dict[str, Any]:
        """Parse TD1 (ID Card) format (3 lines x 30 chars)."""
        doc_code = line1[0:2].replace('<', '')
        issuing_country = line1[2:5].replace('<', '')
        doc_num_raw = line1[5:14]
        doc_num = doc_num_raw.replace('<', '')
        doc_num_cd = line1[14]
        optional_1 = line1[15:30]

        dob_raw = line2[0:6]
        dob_cd = line2[6]
        sex = line2[7].replace('<', 'X')
        expiry_raw = line2[8:14]
        expiry_cd = line2[14]
        nationality = line2[15:18].replace('<', '')
        optional_2 = line2[18:29]
        composite_cd = line2[29]

        names = line3.split('<<', 1)
        surname = names[0].replace('<', ' ').strip()
        given_names = names[1].replace('<', ' ').strip() if len(names) > 1 else ""

        doc_num_valid = verify_field(doc_num_raw, doc_num_cd)
        dob_valid = verify_field(dob_raw, dob_cd)
        expiry_valid = verify_field(expiry_raw, expiry_cd)

        # Composite data: line1[5:30] + line2[0:7] + line2[8:15] + line2[18:29]
        composite_data = line1[5:30] + line2[0:7] + line2[8:15] + line2[18:29]
        composite_valid = verify_field(composite_data, composite_cd)

        all_valid = doc_num_valid and dob_valid and expiry_valid and composite_valid

        return {
            "valid": all_valid,
            "format": "TD1",
            "document_code": doc_code,
            "issuing_state": issuing_country,
            "surname": surname,
            "given_names": given_names,
            "document_number": doc_num,
            "nationality": nationality,
            "date_of_birth": dob_raw,
            "sex": sex,
            "expiry_date": expiry_raw,
            "check_digits": {
                "document_number": {"expected": doc_num_cd, "computed": calculate_check_digit(doc_num_raw), "valid": doc_num_valid},
                "date_of_birth": {"expected": dob_cd, "computed": calculate_check_digit(dob_raw), "valid": dob_valid},
                "expiry_date": {"expected": expiry_cd, "computed": calculate_check_digit(expiry_raw), "valid": expiry_valid},
                "composite": {"expected": composite_cd, "computed": calculate_check_digit(composite_data), "valid": composite_valid}
            }
        }

    @staticmethod
    def _parse_td2(line1: str, line2: str) -> Dict[str, Any]:
        """Parse TD2 format (2 lines x 36 chars)."""
        doc_code = line1[0:2].replace('<', '')
        issuing_country = line1[2:5].replace('<', '')
        name_field = line1[5:36]
        names = name_field.split('<<', 1)
        surname = names[0].replace('<', ' ').strip()
        given_names = names[1].replace('<', ' ').strip() if len(names) > 1 else ""

        doc_num_raw = line2[0:9]
        doc_num = doc_num_raw.replace('<', '')
        doc_num_cd = line2[9]
        nationality = line2[10:13].replace('<', '')
        dob_raw = line2[13:19]
        dob_cd = line2[19]
        sex = line2[20].replace('<', 'X')
        expiry_raw = line2[21:27]
        expiry_cd = line2[27]
        optional_raw = line2[28:35]
        composite_cd = line2[35]

        doc_num_valid = verify_field(doc_num_raw, doc_num_cd)
        dob_valid = verify_field(dob_raw, dob_cd)
        expiry_valid = verify_field(expiry_raw, expiry_cd)

        # Composite data: line2[0:10] + line2[13:20] + line2[21:35]
        composite_data = line2[0:10] + line2[13:20] + line2[21:35]
        composite_valid = verify_field(composite_data, composite_cd)

        all_valid = doc_num_valid and dob_valid and expiry_valid and composite_valid

        return {
            "valid": all_valid,
            "format": "TD2",
            "document_code": doc_code,
            "issuing_state": issuing_country,
            "surname": surname,
            "given_names": given_names,
            "document_number": doc_num,
            "nationality": nationality,
            "date_of_birth": dob_raw,
            "sex": sex,
            "expiry_date": expiry_raw,
            "check_digits": {
                "document_number": {"expected": doc_num_cd, "computed": calculate_check_digit(doc_num_raw), "valid": doc_num_valid},
                "date_of_birth": {"expected": dob_cd, "computed": calculate_check_digit(dob_raw), "valid": dob_valid},
                "expiry_date": {"expected": expiry_cd, "computed": calculate_check_digit(expiry_raw), "valid": expiry_valid},
                "composite": {"expected": composite_cd, "computed": calculate_check_digit(composite_data), "valid": composite_valid}
            }
        }

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    result = MRZParser.parse(content)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("valid") else 1)
