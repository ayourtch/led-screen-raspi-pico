cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
project(test_project C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()
add_executable(pwmled
    pwmled.c
)

pico_generate_pio_header(pwmled ${CMAKE_CURRENT_LIST_DIR}/ws2812.pio OUTPUT_DIR ${CMAKE_CURRENT_LIST_DIR}/)


pico_enable_stdio_usb(pwmled 1)
pico_enable_stdio_uart(pwmled 0)

pico_add_extra_outputs(pwmled)

target_link_libraries(pwmled pico_stdlib hardware_pwm hardware_pio)
