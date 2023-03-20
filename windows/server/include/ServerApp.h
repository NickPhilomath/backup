#pragma once

#undef UNICODE
#define WIN32_LEAN_AND_MEAN
#define _CRT_SECURE_NO_DEPRECATE

#define DEFAULT_BUFLEN 512
#define DEFAULT_PORT "27015"

#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <vector>
#include <thread>
#include <string>
#include <fstream>
#include <filesystem>

// Need to link with Ws2_32.lib, Mswsock.lib, and Advapi32.lib
#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")


class ServerApp {
public:
    int Initialize();
    void Run();
    void Listen();
    void ManageClients();

private:
    std::thread listenThread;
    std::thread clientsThread;

    WSADATA wsaData;
    int iResult;

    std::vector<SOCKET> m_sockets;

    SOCKET ListenSocket = INVALID_SOCKET;
    SOCKET ClientSocket = INVALID_SOCKET;

    struct addrinfo* result = NULL;
    struct addrinfo hints;

    int iSendResult;
    char recvbuf[DEFAULT_BUFLEN];
    int recvbuflen = DEFAULT_BUFLEN;
};