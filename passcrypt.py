from colorama import Fore, Back, Style, init
import pyfiglet
from tabulate import tabulate
from cryptography.fernet import Fernet
import os
import random
import string

# Initialize colorama
init(autoreset=True)

# Generate a key and save it (Run this part ONCE to create a key file)
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the key
def load_key():
    if not os.path.exists("key.key"):
        print(Fore.RED + "Key file not found! Run generate_key() first.")
        exit()
    with open("key.key", "rb") as key_file:
        return key_file.read()

# Encrypt data
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Decrypt data
def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()

# Save password to file
def save_password(service, username, password, key):
    encrypted_password = encrypt_data(password, key)
    with open("passwords.txt", "a") as file:
        file.write(f"{service},{username},{encrypted_password.decode()}\n")
    print(Fore.GREEN + f"Password for {service} saved successfully!")

# Retrieve password from file
def retrieve_password(service, key):
    if not os.path.exists("passwords.txt"):
        print(Fore.RED + "No passwords saved yet!")
        return
    with open("passwords.txt", "r") as file:
        for line in file:
            saved_service, username, encrypted_password = line.strip().split(",")
            if saved_service == service:
                password = decrypt_data(encrypted_password.encode(), key)
                table = [
                    ["Service", service],
                    ["Username", username],
                    ["Password", password]
                ]
                print(Fore.YELLOW + tabulate(table, headers=["Field", "Details"], tablefmt="fancy_grid"))
                return
    print(Fore.RED + f"No password found for {service}!")

# Generate a strong password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Banner
def print_banner():
    ascii_art = pyfiglet.figlet_format("PassCrypt", font="slant")
    colored_banner = ""
    for line in ascii_art.splitlines():
        for char in line:
            if char == "P":  # Make 'P' red
                colored_banner += Fore.RED + char
            else:  # All other letters in light blue
                colored_banner += Fore.LIGHTBLUE_EX + char
        colored_banner += "\n"  # Preserve line breaks
    print(colored_banner)

# Main Menu
def main():
    print_banner()
    key = load_key()
    while True:
        print(Fore.MAGENTA + "\n=== PassCrypt ===")
        print(Fore.BLUE + "1. Add a new password")
        print(Fore.BLUE + "2. Retrieve a password")
        print(Fore.BLUE + "3. Generate a strong password")
        print(Fore.RED + "4. Exit")
        choice = input(Fore.CYAN + "Enter your choice: ")

        if choice == "1":
            service = input(Fore.YELLOW + "Enter the service name: ")  # Green color for service input
            username = input(Fore.YELLOW + "Enter the username: ")  # Yellow color for username input
            password = input(Fore.CYAN + "Enter the password (leave blank to generate one): ")  # Cyan color for password input
            if not password:
                password = generate_password()
                print(Fore.BLUE + f"Generated Password: {password}")
            save_password(service, username, password, key)

        elif choice == "2":
            service = input(Fore.GREEN + "Enter the service name to retrieve: ")
            retrieve_password(service, key)

        elif choice == "3":
            try:
                length = int(input(Fore.GREEN + "Enter the length of the password: "))  # Check if the input is an integer
                print(Fore.BLUE + f"Generated Password: {generate_password(length)}")
            except ValueError:
                print(Fore.RED + "Invalid input! Please enter a valid number for password length.")  # Display an error message

        elif choice == "4":
            print(Fore.RED + "Exiting PassCrypt. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    if not os.path.exists("key.key"):
        print(Fore.YELLOW + "Generating encryption key...")
        generate_key()
    main()
