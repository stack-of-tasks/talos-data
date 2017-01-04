CMAKE_MINIMUM_REQUIRED(VERSION 2.8.3)
INCLUDE(cmake/base.cmake)
#include(cmake/ros.cmake)


SET(PROJECT_NAME talos-data)
SET(PROJECT_DESCRIPTION "Talos urdf model, srdf model and other data")
SET(PROJECT_URL "https://redmine.laas.fr/projects/pyrene-talos/repository/talos-data")

SETUP_PROJECT()

# Find xml_reflection
ADD_REQUIRED_DEPENDENCY("urdfdom >= 0.2.9")

FOREACH(dir config gazebo meshes robots urdf srdf)
  INSTALL(DIRECTORY ${CMAKE_SOURCE_DIR}/${dir}
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME})
ENDFOREACH(dir)

SETUP_PROJECT_FINALIZE()