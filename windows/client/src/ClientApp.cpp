#include "ClientApp.h"

void ClientApp::Run() {
    if (Initialize() == EXIT_FAILURE)
        return;

    if (Connect() == EXIT_FAILURE)
        return;

    m_sendSize = 5;
    m_sendbuf = new char[m_sendSize];
    m_sendbuf = (char*)"hello";

    while (true) {
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        
        Send();
        Receive();
    }

    Shutdown();

    closesocket(m_ConnectSocket);
    WSACleanup();
}

int ClientApp::Initialize() {
    // Initialize Winsock
    m_result = WSAStartup(MAKEWORD(2, 2), &m_wsaData);
    if (m_result != 0) {
        printf("WSAStartup failed with error: %d\n", m_result);
        return EXIT_FAILURE;
    }

    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    return EXIT_SUCCESS;
}

int ClientApp::Connect() {
    // Resolve the server address and port
    m_result = getaddrinfo(m_address, DEFAULT_PORT, &hints, &m_ConnectResult);
    if (m_result != 0) {
        printf("getaddrinfo failed with error: %d\n", m_result);
        WSACleanup();
        return EXIT_FAILURE;
    }

    // Attempt to connect to an address until one succeeds
    for (ptr = m_ConnectResult; ptr != NULL; ptr = ptr->ai_next) {

        // Create a SOCKET for connecting to server
        m_ConnectSocket = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol);
        if (m_ConnectSocket == INVALID_SOCKET) {
            printf("socket failed with error: %ld\n", WSAGetLastError());
            WSACleanup();
            return EXIT_FAILURE;
        }

        // Connect to server.
        m_result = connect(m_ConnectSocket, ptr->ai_addr, (int)ptr->ai_addrlen);
        if (m_result == SOCKET_ERROR) {
            closesocket(m_ConnectSocket);
            m_ConnectSocket = INVALID_SOCKET;
            continue;
        }
        break;
    }

    freeaddrinfo(m_ConnectResult);

    if (m_ConnectSocket == INVALID_SOCKET) {
        printf("Unable to connect to server!\n");
        WSACleanup();
        return EXIT_FAILURE;
    }
    std::cout << "connected to server: " << m_address << " port: " << DEFAULT_PORT << "\n";
}

void ClientApp::Send() {
    // Send an initial buffer
    m_result = send(m_ConnectSocket, m_sendbuf, m_sendSize, 0); //(int)strlen(sendbuf)
    if (m_result == SOCKET_ERROR) {
        printf("send failed with error: %d\n", WSAGetLastError());
        closesocket(m_ConnectSocket);
        WSACleanup();
        return;
    }

    printf("Bytes Sent: %ld\n", m_result);
}

void ClientApp::Shutdown() {
    // shutdown the connection since no more data will be sent
    m_result = shutdown(m_ConnectSocket, SD_SEND);
    if (m_result == SOCKET_ERROR) {
        printf("shutdown failed with error: %d\n", WSAGetLastError());
        closesocket(m_ConnectSocket);
        WSACleanup();
        return;
    }
}

void ClientApp::Receive() {
    // Receive until the peer closes the connection
    do {

        m_result = recv(m_ConnectSocket, m_recvbuf, m_recvbuflen, 0);
        if (m_result > 0) {
            printf("Bytes received: %d\n", m_result);
            for (int i = 0; i < m_result; i++) {
                std::cout << m_recvbuf[i];
            }
            std::cout << "\n";
        }
        else if (m_result == 0)
            printf("Connection closed\n");
        else
            printf("recv failed with error: %d\n", WSAGetLastError());

    } while (m_result > 0);
}

void ClientApp::CheckChanges() {
    std::string path = "C:/Dev/backup-windows";
    for (const auto& entry : std::filesystem::recursive_directory_iterator(path)) {
        std::cout << entry.path() << " " << entry.is_directory() << std::endl;
    }
}