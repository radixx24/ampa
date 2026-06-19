// Sonda de portabilidad de AMPA (C++17, solo biblioteca estándar).
//
// Demuestra dos cosas que el proyecto necesita:
//   1. Detección de sistema operativo portable, mediante macros del preprocesador.
//   2. Aleatoriedad REPRODUCIBLE: el motor std::mt19937_64 produce, para una
//      misma semilla, exactamente la misma secuencia en cualquier SO/compilador.
//
// Sin dependencias externas: se compila con g++, clang o MSVC.
#include <cstdint>
#include <iostream>
#include <random>
#include <string>

static std::string detect_os() {
#if defined(_WIN32)
    return "windows";
#elif defined(__APPLE__)
    return "macos";
#elif defined(__linux__)
    return "linux";
#else
    return "unknown";
#endif
}

int main(int argc, char** argv) {
    std::uint64_t seed = 42;  // semilla por defecto (reproducible)
    if (argc > 1) {
        seed = std::stoull(argv[1]);
    }

    // El valor crudo del motor es idéntico en todas las plataformas para una
    // misma semilla (lo garantiza el estándar de C++ para mt19937_64).
    std::mt19937_64 rng(seed);
    const std::uint64_t draw = rng();

    std::cout << "AMPA probe (C++)\n";
    std::cout << "  sistema    : " << detect_os() << "\n";
    std::cout << "  estandar   : C++" << (__cplusplus / 100 % 100) << "\n";
    std::cout << "  semilla    : " << seed << "\n";
    std::cout << "  aleatorio  : " << (draw % 1000000ULL)
              << "  (identico en cualquier SO con la misma semilla)\n";
    return 0;
}
