#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IQ MAXX (by dk) - Wi-Fi Security Audit & Password Analyzer
Calculates entropy, analyzes encryption weaknesses, and detects default/weak router credentials.
"""

import math
import re
from typing import Dict, Any, List

# Common weak Wi-Fi patterns & defaults
COMMON_WEAK_PASSWORDS = {
    "12345678", "123456789", "1234567890", "password", "password123",
    "admin123", "admin1234", "qwertyuiop", "qwerty123", "welcome123",
    "wifipassword", "internet123", "0123456789", "11111111", "00000000",
    "88888888", "12344321", "pass1234", "letmein123", "supersecret",
    "linksys123", "netgear123", "dlink1234", "tp-link12", "cisco123"
}

class PasswordAuditResult:
    def __init__(self, password: str):
        self.password = password
        self.length = len(password)
        self.entropy = self._calculate_entropy(password)
        self.has_upper = bool(re.search(r'[A-Z]', password))
        self.has_lower = bool(re.search(r'[a-z]', password))
        self.has_digit = bool(re.search(r'[0-9]', password))
        self.has_special = bool(re.search(r'[^A-Za-z0-9]', password))
        self.is_common = password.lower() in COMMON_WEAK_PASSWORDS
        self.score, self.level, self.color_badge = self._compute_score()
        self.recommendations = self._generate_recommendations()

    @staticmethod
    def _calculate_entropy(pwd: str) -> float:
        if not pwd:
            return 0.0
        pool_size = 0
        if re.search(r'[a-z]', pwd):
            pool_size += 26
        if re.search(r'[A-Z]', pwd):
            pool_size += 26
        if re.search(r'[0-9]', pwd):
            pool_size += 10
        if re.search(r'[^A-Za-z0-9]', pwd):
            pool_size += 32
        
        if pool_size == 0:
            return 0.0
        
        entropy = len(pwd) * math.log2(pool_size)
        return round(entropy, 2)

    def _compute_score(self):
        # Base score on length and character sets
        score = 0
        if self.length >= 8:
            score += 25
        if self.length >= 12:
            score += 20
        if self.length >= 16:
            score += 15

        char_variety = sum([self.has_upper, self.has_lower, self.has_digit, self.has_special])
        score += char_variety * 10

        if self.is_common:
            score = 10

        if self.password.startswith("[") and self.password.endswith("]"):
            # Placeholder or special tag
            return 0, "N/A", "GRAY"

        if score >= 80 and self.entropy >= 65:
            return score, "EXCELLENT", "GREEN_BRIGHT"
        elif score >= 60 and self.entropy >= 45:
            return score, "STRONG", "GREEN"
        elif score >= 40:
            return score, "MODERATE", "YELLOW"
        else:
            return score, "CRITICAL WEAK", "RED"

    def _generate_recommendations(self) -> List[str]:
        recs = []
        if self.password.startswith("["):
            return recs
        if self.length < 12:
            recs.append("Increase Wi-Fi passphrase length to at least 14+ characters.")
        if not (self.has_upper and self.has_lower and self.has_digit and self.has_special):
            recs.append("Combine uppercase, lowercase, numbers, and special symbols (!@#$%^&*).")
        if self.is_common:
            recs.append("CRITICAL: Passphrase matches common dictionary wordlist; change immediately!")
        if self.entropy < 40:
            recs.append("Low entropy detected; avoid predictable repeating sequences or phone numbers.")
        return recs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "password": self.password,
            "length": self.length,
            "entropy": self.entropy,
            "score": self.score,
            "level": self.level,
            "is_common": self.is_common,
            "recommendations": self.recommendations
        }

class SecurityAuditor:
    """Evaluates network security posture, encryption algorithms, and credentials."""

    @staticmethod
    def audit_password(password: str) -> PasswordAuditResult:
        return PasswordAuditResult(password)

    @staticmethod
    def audit_network_security(auth: str, cipher: str) -> Dict[str, Any]:
        auth_upper = auth.upper()
        ciph_upper = cipher.upper()

        if "OPEN" in auth_upper or "NONE" in auth_upper:
            return {
                "grade": "F (UNSECURED)",
                "risk": "CRITICAL",
                "verdict": "Open Wi-Fi transmits all data unencrypted over the air."
            }
        elif "WEP" in auth_upper:
            return {
                "grade": "F (OBSOLETE)",
                "risk": "CRITICAL",
                "verdict": "WEP uses broken RC4 stream cipher, trivially crackable in under 3 minutes."
            }
        elif "WPA" in auth_upper and "WPA2" not in auth_upper and "WPA3" not in auth_upper:
            return {
                "grade": "D (DEPRECATED)",
                "risk": "HIGH",
                "verdict": "Legacy WPA1 protocol is outdated and susceptible to offline dictionary attacks."
            }
        elif "TKIP" in ciph_upper:
            return {
                "grade": "C (WEAK CIPHER)",
                "risk": "MEDIUM",
                "verdict": "TKIP cipher is deprecated. Switch router to AES-CCMP or GCMP."
            }
        elif "WPA3" in auth_upper:
            return {
                "grade": "A+ (NEXT-GEN)",
                "risk": "SAFE",
                "verdict": "WPA3 Simultaneous Authentication of Equals (SAE) provides robust security and forward secrecy."
            }
        else:
            return {
                "grade": "A (SECURE)",
                "risk": "LOW",
                "verdict": "WPA2-PSK with AES-CCMP encryption is industry-standard when paired with a strong passphrase."
            }
