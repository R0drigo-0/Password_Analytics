import os
import pandas as pd
from itertools import  product
from Levenshtein import distance

def password_similarity(pass1, pass2):
    return distance(pass1, pass2)

same_user = {}
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
                print(f"Password not found in line: {line}")
                break

            user = correo.split("@")[0]
            if user not in same_user:
                same_user[user] = set()
            same_user[user].add(contraseña.strip())

related_passwords = []
for user1, passwords1 in same_user.items():
    if len(passwords1) > 1:
        related = set()
        for user2, passwords2 in same_user.items():
            if user1 != user2: 
                for pass1, pass2 in product(passwords1, passwords2):
                    similarity = password_similarity(pass1, pass2)
                    if similarity < 3:
                        related.add(pass1)
                        related.add(pass2)
        if related:
            related_passwords.append((user1, list(related)))

df = pd.DataFrame(related_passwords, columns=['Usuario', 'Contraseñas'])

excel_file = 'password_relations.xlsx'
df.to_excel(excel_file, index=False)

print(f"Se ha guardado la información de las contraseñas relacionadas en el archivo '{excel_file}'.")

total_users = len(same_user)
users_with_related_passwords = len(df)
percentage = (users_with_related_passwords / total_users) * 100

print(f"Porcentaje de usuarios con contraseñas relacionadas: {percentage:.2f}%")
