import socket
import random
import threading

# Server address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def handle_client(client_socket, address):
    print(f"New connection from: {address}")
    
    # Generate a random number
    secret_number = random.randint(0, 100)
    print(f"Secret number is {secret_number}")  # Debug için

    attempts = 10  # Number of attempts

    # Send welcome message
    client_socket.send("Welcome to the Number Guessing Game!\n".encode("utf-8"))
    client_socket.send(f"Guess a number between 0 and 100. You have {attempts} attempts left.\n".encode("utf-8"))

    while attempts > 0:
        # Send a prompt to the client for their guess
        try:
            client_socket.send("Enter your guess: ".encode("utf-8"))
        except Exception as e:
            print(f"Failed to send data to {address}: {e}")
            break

        # Receive the guess from the client
        try:
            guess = client_socket.recv(1024).decode("utf-8").strip()
        except Exception as e:
            print(f"Connection with {address} lost: {e}")
            break

        # Check if input is a valid number
        if not guess.isdigit():
            try:
                client_socket.send("Please enter a valid number.\n".encode("utf-8"))
            except Exception as e:
                print(f"Failed to send data to {address}: {e}")
                break
            continue  # If input is not a number, ask again
        
        guess = int(guess)  # Convert the input to an integer

        # Check if the guess is within the valid range
        if not (0 <= guess <= 100):  # Combine range check into a single condition
            try:
                client_socket.send("Please enter a number between 0 and 100.\n".encode("utf-8"))
            except Exception as e:
                print(f"Failed to send data to {address}: {e}")
                break
            continue  # Ask for another guess

        # Check the guess
        if guess == secret_number:
            try:
                client_socket.send(f"Congratulations! You guessed the correct number: {secret_number}\n".encode("utf-8"))
                client_socket.send("Correct answer!\n".encode("utf-8"))
            except Exception as e:
                print(f"Failed to send data to {address}: {e}")
            break  # End the game for this client
        elif guess < secret_number:
            attempts -= 1
            try:
                client_socket.send(f"Too low! You have {attempts} attempts left.\n".encode("utf-8"))
            except Exception as e:
                print(f"Failed to send data to {address}: {e}")
                break
        elif guess > secret_number:
            attempts -= 1
            try:
                client_socket.send(f"Too high! You have {attempts} attempts left.\n".encode("utf-8"))
            except Exception as e:
                print(f"Failed to send data to {address}: {e}")
                break

    # When attempts run out
    if attempts == 0:
        try:
            client_socket.send(f"You ran out of attempts! The correct number was: {secret_number}.\n".encode("utf-8"))
        except Exception as e:
            print(f"Failed to send data to {address}: {e}")
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
