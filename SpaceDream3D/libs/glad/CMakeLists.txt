cmake_minimum_required(VERSION 3.11)

add_library(glad src/glad.c include/glad/glad.h ../../include/rg/Cubemap2D.h)

target_include_directories(glad PUBLIC include/)