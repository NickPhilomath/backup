#include <iostream>
using namespace std;

int main(int argc, char* argv[]) {
	std::cout << argc << std::endl;
	std::cout << argv << std::endl;
	
	for (int i = 0; i < argc; i++) {
		std::cout << argv[i] << std::endl;
	}
	std::cin.get();
	return 0;
}