#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>  // Windows network library

#pragma comment(lib, "ws2_32.lib")  // Linker dependency for winsock

int main() {
    WSADATA wsa;
    SOCKET sock;
    struct sockaddr_in server;
    char message[1024], server_reply[1024];

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        printf("Failed to initialize Winsock. Error code: %d\n", WSAGetLastError());
        return 1;
    }

    printf("Winsock initialized.\n");

    // Create a socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        printf("Socket creation failed. Error code: %d\n", WSAGetLastError());
        return 1;
    }

    printf("Socket created.\n");

    // Set up server details
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_family = AF_INET;
    server.sin_port = htons(12345);

    // Connect to the server
    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
        printf("Connection failed.\n");
        return 1;
    }

    printf("Connected to server. Please make your guess:\n");

    // Receive the first message from the server
    if (recv(sock, server_reply, sizeof(server_reply), 0) < 0) {
        printf("Failed to receive server response.\n");
        return 1;
    }
    server_reply[strlen(server_reply)] = '\0';  // Null-terminate the string
    printf("%s", server_reply);  // Print the server message

    // Game loop
    while (1) {
        // Get user input
        printf("> ");
        fgets(message, sizeof(message), stdin);

        // Remove newline character at the end of the input
        message[strcspn(message, "\n")] = 0;

        // Prevent sending empty messages
        if (strlen(message) == 0) {
            printf("Please enter a valid guess.\n");
            continue;
        }

        // Send the guess to the server
        if (send(sock, message, strlen(message), 0) < 0) {
            printf("Message sending failed.\n");
            break;
        }

        // Receive the server response
        int recv_size = recv(sock, server_reply, sizeof(server_reply) - 1, 0);
        if (recv_size < 0) {
            printf("Failed to receive response.\n");
            break;
        }
        server_reply[recv_size] = '\0';  // Null-terminate the string
        printf("Server: %s\n", server_reply);

        // Check if the correct answer was guessed or game over
        if (strstr(server_reply, "Congratulations") || strstr(server_reply, "Correct answer!")) {
            printf("Correct answer!\n");
            break;
        }

        if (strstr(server_reply, "You ran out of attempts")) {
            break;
        }

        // After receiving the response, wait for the next input
        if (strstr(server_reply, "Guess a number between 0 and 100") != NULL) {
        }
    }

    // Clean up
    closesocket(sock);
    WSACleanup();

    return 0;
}

