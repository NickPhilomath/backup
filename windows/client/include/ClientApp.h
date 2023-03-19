#pragma once

#define WIN32_LEAN_AND_MEAN

#include <iostream>
#include <fstream>
#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdlib.h>
#include <stdio.h>

#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")


#define DEFAULT_BUFLEN 512
#define DEFAULT_PORT "27015"

class ClientApp {
public:
    int Initialize();
    void Run();

private:
    WSADATA wsaData;
    SOCKET ConnectSocket = INVALID_SOCKET;
    struct addrinfo* result = NULL,
        * ptr = NULL,
        hints;
    char* sendbuf = nullptr;
    const char* address= "127.0.0.1";
    char recvbuf[DEFAULT_BUFLEN];
    int iResult, size;
    int recvbuflen = DEFAULT_BUFLEN;
};