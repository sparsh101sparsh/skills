import os
import sys
import tempfile
import pytest
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from mrz_parser import calculate_check_digit, verify_field, MRZParser
from ela_analyzer import perform_ela

def test_check_digit_calculation():
    # Standard ICAO test vector: "L898902C3" -> 7-3-1 weighting
    # 'L'=21*7=147, '8'=8*3=24, '9'=9*1=9, '8'=8*7=56, '9'=9*3=27, '0'=0*1=0, '2'=2*7=14, 'C'=12*3=36, '3'=3*1=3
    # Total = 147 + 24 + 9 + 56 + 27 + 0 + 14 + 36 + 3 = 316 % 10 = 6
    assert calculate_check_digit("L898902C3") == "6"

def test_td3_passport_parsing():
    # Authentic sample TD3 MRZ
    td3_sample = (
        "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<\n"
        "L898902C36UTO7408122F1204159ZE184226B<<<<<10"
    )
    result = MRZParser.parse(td3_sample)
    assert result["valid"] is True
    assert result["format"] == "TD3"
    assert result["surname"] == "ERIKSSON"
    assert result["given_names"] == "ANNA MARIA"
    assert result["document_number"] == "L898902C3"
    assert result["date_of_birth"] == "740812"
    assert result["expiry_date"] == "120415"
    assert result["nationality"] == "UTO"
    assert result["check_digits"]["document_number"]["valid"] is True
    assert result["check_digits"]["date_of_birth"]["valid"] is True
    assert result["check_digits"]["expiry_date"]["valid"] is True
    assert result["check_digits"]["composite"]["valid"] is True

def test_td3_tampered_dob_detected():
    # Tampering DOB from 740812 to 840812 without updating check digit 2
    td3_tampered = (
        "P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<<<<<<<\n"
        "L898902C36UTO8408122F1204159ZE184226B<<<<<10"
    )
    result = MRZParser.parse(td3_tampered)
    assert result["valid"] is False
    assert result["check_digits"]["date_of_birth"]["valid"] is False

def test_td1_id_card_parsing():
    td1_sample = (
        "I<UTOD231458907<<<<<<<<<<<<<<<\n"
        "7408122F1204159UTO<<<<<<<<<<<6\n"
        "ERIKSSON<<ANNA<MARIA<<<<<<<<<<"
    )
    result = MRZParser.parse(td1_sample)
    assert result["valid"] is True
    assert result["format"] == "TD1"
    assert result["surname"] == "ERIKSSON"
    assert result["given_names"] == "ANNA MARIA"
    assert result["document_number"] == "D23145890"

def test_ela_analyzer():
    # Create temporary clean JPEG
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tf:
        clean_img = Image.new('RGB', (100, 100), color=(200, 200, 200))
        clean_img.save(tf.name, 'JPEG', quality=95)
        tf_path = tf.name

    try:
        ela_res = perform_ela(tf_path, quality=90)
        assert ela_res["success"] is True
        assert "mean_error" in ela_res["metrics"]
        assert ela_res["is_anomalous"] is False
    finally:
        if os.path.exists(tf_path):
            os.remove(tf_path)
