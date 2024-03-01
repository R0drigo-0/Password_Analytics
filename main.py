import os
import re
from collections import Counter

n_total = 0
n_num = 0  # numeriques
n_alpha = 0  # alfabeticas
n_alfa = 0  # alfanumericas
n_century = 0  # contiene un año
n_lowercase = 0  # todas minusculas
n_uppercase = 0  # todas mayusculas
n_capitalized = 0  # primera mayuscula

n_most_commons = {}

def isnumber(string):
    try:
        float(string)
        return True
    except:
        return False


def is_alfabethic(string):
    pattern = r"^[a-zA-z]+$"
    match = re.match(pattern, string)
    return bool(match)


def is_alphanumeric(string):
    pattern = r"^[a-zA-z0-9]+$"
    match = re.match(pattern, string)
    return bool(match)


def contains_year(string):
    pattern = r"(?:19|20)\d{2}"
    match = re.search(pattern, string)
    return bool(match)


def all_minus(string):
    pattern = r"[a-z]+(\s[a-z]+)*"
    match = re.search(pattern, string)
    return bool(match)


def all_mayus(string):
    pattern = r"[A-Z]+(\s[A-Z]+)*"
    match = re.search(pattern, string)
    return bool(match)


def first_minus_all_mayus(string):
    pattern = r"[A-Z][a-z]+(\s[A-Z][a-z]+)*"
    match = re.search(pattern, string)
    return bool(match)


folder_path = "pass/"
files = os.listdir(folder_path)
for file in files:
    full_path = os.path.join(folder_path, file)
    with open(full_path, "r", encoding="iso-8859-1") as f:
        lines = f.readlines()

        for line in lines:
            correo = ""
            contraseña = ""

            if ":" in line:
                correo, contraseña = line.split(":", 1)
            elif ";" in line:
                correo, contraseña = line.split(";", 1)
            else:
                print("Password not found")
                break
            
            if contraseña in n_most_commons:
              n_most_commons[contraseña] += 1
            else:
              n_most_commons[contraseña] = 1

            n_total += 1
            if isnumber(contraseña):
                n_num += 1
            if is_alfabethic(contraseña):
                n_alfa += 1
            if is_alphanumeric(contraseña):
                n_alpha += 1
            if contains_year(contraseña):
                n_century += 1
            if all_minus(contraseña):
                n_lowercase += 1
            if all_mayus(contraseña):
                n_uppercase += 1
            if first_minus_all_mayus(contraseña):
                n_capitalized += 1

n_most_commons = dict(sorted(n_most_commons.values(), reverse=True))
print("END SCAN")
print("Total:", n_total)
print("Numerica:", n_num)
print("Alfabetica:", n_alpha)
print("Alfanumericas:", n_alfa)
print("Cotiene un año entre 1900 and 2100:", n_century)
print("Minusculas:", n_lowercase)
print("Mayuscula:", n_uppercase)
print("Primera mayuscula:", n_capitalized)
print()
print("30 contraseñas mas comunes:")
print(n_most_commons[:30])
