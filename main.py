import os
import re
import time
from statistics import median
from collections import Counter


start_time = time.perf_counter()

"""
Format file:
email:password
email;password

The lines that are:
email
are not counted
"""
n_total = 0
n_num = 0  # numeriques
n_alpha = 0  # alfabeticas
n_alfa = 0  # alfanumericas
n_century = 0  # contiene un año
n_lowercase = 0  # todas minusculas
n_uppercase = 0  # todas mayusculas
n_capitalized = 0  # primera mayuscula

most_commons_pass = {}
length_pass = {}
digit_counter = {}


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

            most_commons_pass[contraseña] = most_commons_pass.get(contraseña, 0) + 1
            length_pass[len(contraseña)] = length_pass.get(len(contraseña), 0) + 1
            for d in contraseña:
                if isnumber(d):
                    digit_counter[d] = digit_counter.get(d,0) + 1

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
                elapsed_time = time.perf_counter() - start_time

most_commons_pass = sorted(most_commons_pass.items(), key=lambda x: x[1], reverse=True)
most_commons_pass = most_commons_pass[:30]

length_pass = sorted(length_pass.items(), key=lambda x: x[1], reverse=True)
min_length_pass = min(length_pass, key=lambda x: x[0])[0]
max_length_pass = max(length_pass, key=lambda x: x[0])[0]

total_length_pass = sum(x[0] * x[1] for x in length_pass)
total_passwords_pass = sum(x[1] for x in length_pass)
average_length_pass = total_length_pass / total_passwords_pass

second_element_length_pass = [x[1] for x in length_pass]
second_element_length_pass = {length for length in second_element_length_pass}
median_pass = median(second_element_length_pass)

digit_counter = sorted(digit_counter.items(), key=lambda x: x[0], reverse=False)


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
print(most_commons_pass)
print()
print("Longitud contraseñas:")
print(length_pass)
print(f"Contraseña mas corta: {min_length_pass}")
print(f"Contraseña mas larga: {max_length_pass}")
print(f"Contraseña media: {average_length_pass}")
print(f"Contraseña mediana: {median_pass}")
print()
print("Numero de apariciones digito:")
print(digit_counter)
print()

