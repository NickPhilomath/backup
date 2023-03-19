#include "ServerApp.h"

void ServerApp::Run() {
    if (Initialize() == EXIT_SUCCESS) {
        listenThread = std::thread(&ServerApp::Listen, this);
        clientsThread = std::thread(&ServerApp::ManageClients, this);

        listenThread.join();
        clientsThread.join();
    }

    WSACleanup();


}

int ServerApp::Initialize() {
    // Initialize Winsock
    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0) {
        printf("WSAStartup failed with error: %d\n", iResult);
        return EXIT_FAILURE;
    }

    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;
    hints.ai_flags = AI_PASSIVE;

    // Resolve the server address and port
    iResult = getaddrinfo(NULL, DEFAULT_PORT, &hints, &result);
    if (iResult != 0) {
        printf("getaddrinfo failed with error: %d\n", iResult);
        return EXIT_FAILURE;
    }

    // Create a SOCKET for the server to listen for client connections.
    ListenSocket = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
    if (ListenSocket == INVALID_SOCKET) {
        printf("socket failed with error: %ld\n", WSAGetLastError());
        freeaddrinfo(result);
        return EXIT_FAILURE;
    }

    // Setup the TCP listening socket
    iResult = bind(ListenSocket, result->ai_addr, (int)result->ai_addrlen);
    if (iResult == SOCKET_ERROR) {
        printf("bind failed with error: %d\n", WSAGetLastError());
        freeaddrinfo(result);
        closesocket(ListenSocket);
        return EXIT_FAILURE;
    }

    freeaddrinfo(result);

    return EXIT_SUCCESS;
}

void ServerApp::Listen() {
    while (true) {
        iResult = listen(ListenSocket, SOMAXCONN);
        if (iResult == SOCKET_ERROR) {
            printf("listen failed with error: %d\n", WSAGetLastError());
            closesocket(ListenSocket);
            WSACleanup();
            return;
        }

        // Accept a client socket
        SOCKET acceptSocket = accept(ListenSocket, NULL, NULL);
        if (acceptSocket == INVALID_SOCKET) {
            printf("accept failed with error: %d\n", WSAGetLastError());
            closesocket(ListenSocket);
            WSACleanup();
            return;
        }
        else {
            m_sockets.push_back(acceptSocket);
        }
    }

    // No longer need server socket
    closesocket(ListenSocket);
}

void ServerApp::ManageClients() {
    while (true) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        for (auto socket : m_sockets) {

            // Receive until the peer shuts down the connection
            do {
                iResult = recv(socket, recvbuf, recvbuflen, 0);
                if (iResult > 0) {
                    printf("Bytes received: %d\n", iResult);

                    // Echo the buffer back to the sender
                    iSendResult = send(socket, recvbuf, iResult, 0);
                    if (iSendResult == SOCKET_ERROR) {
                        printf("send failed with error: %d\n", WSAGetLastError());
                        closesocket(socket);
                        WSACleanup();
                        return;
                    }
                    printf("Bytes sent: %d\n", iSendResult);
                }
                else if (iResult == 0)
                    printf("Connection closing...");
                else {
                    printf("recv failed with error: %d\n", WSAGetLastError());
                    closesocket(socket);
                    WSACleanup();
                    return;
                }

            } while (iResult > 0);

            // shutdown the connection since we're done
            iResult = shutdown(socket, SD_SEND);
            if (iResult == SOCKET_ERROR) {
                printf("shutdown failed with error: %d\n", WSAGetLastError());
                closesocket(socket);
                WSACleanup();
                return;
            } 

            printf(" done.\n");

            // cleanup
            closesocket(socket);

            m_sockets.erase(m_sockets.begin());
        }
        //std::cout << "sockets: " << m_sockets.size() << std::endl;
    }

}