cmake_minimum_required(VERSION 3.1)

# Project properties
set(PROJECT_ORG stack-of-tasks)
set(PROJECT_NAME talos_data)
set(PROJECT_DESCRIPTION "Talos urdf model, srdf model and other data")
set(PROJECT_URL "https://github.com/${PROJECT_ORG}/${PROJECT_NAME}")

# Project configuration
set(PROJECT_USE_CMAKE_EXPORT TRUE)

# JRL-cmakemodule setup
include(cmake/base.cmake)

# Project definition
compute_project_args(PROJECT_ARGS LANGUAGES CXX C)
project(${PROJECT_NAME} ${PROJECT_ARGS})

# Main Library
add_library(${PROJECT_NAME} INTERFACE)
install(
  TARGETS ${PROJECT_NAME}
  EXPORT ${TARGETS_EXPORT_NAME}
  DESTINATION lib)

foreach(
  dir
  config
  gazebo
  meshes
  robots
  urdf
  srdf
  launch)
  install(DIRECTORY ${dir} DESTINATION share/${PROJECT_NAME})
endforeach(dir)

install(FILES package.xml DESTINATION share/${PROJECT_NAME})
set(PACKAGE_EXTRA_MACROS "set(TALOS_DATA_PREFIX ${CMAKE_INSTALL_PREFIX})")
