#pragma once

#define WIN32_LEAN_AND_MEAN

#include <iostream>
#include <fstream>
#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdlib.h>
#include <stdio.h>
#include <filesystem>
#include <thread>

#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")


#define DEFAULT_BUFLEN 512
#define DEFAULT_PORT "27015"

class ClientApp {
public:
    void Run();

private:
    int Initialize();
    int Connect();
    void Send();
    void Shutdown();
    void Receive();
    void CheckChanges();

    WSADATA m_wsaData;
    SOCKET m_ConnectSocket = INVALID_SOCKET;
    struct addrinfo* m_ConnectResult = NULL, * ptr = NULL, hints;
    char* m_sendbuf = nullptr;
    const char* m_address= "127.0.0.1";
    char m_recvbuf[DEFAULT_BUFLEN];
    int m_result, m_sendSize;
    int m_recvbuflen = DEFAULT_BUFLEN;
};