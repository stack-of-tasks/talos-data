CMAKE_MINIMUM_REQUIRED(VERSION 2.8.3)

SET(PROJECT_ORG pyrene-dev)
SET(PROJECT_NAME talos_data)
SET(PROJECT_DESCRIPTION "Talos urdf model, srdf model and other data")
SET(PROJECT_URL "https://gepgitlab.laas.fr/${PROJECT_ORG}/${PROJECT_NAME}")

#include(cmake/ros.cmake)
INCLUDE(cmake/base.cmake)

set(CXX_DISABLE_WERROR True)

COMPUTE_PROJECT_ARGS(PROJECT_ARGS LANGUAGES CXX)
PROJECT(${PROJECT_NAME} ${PROJECT_ARGS})

find_package(catkin REQUIRED)

catkin_package(
  #  INCLUDE_DIRS include
  #  LIBRARIES talos_description
  #  CATKIN_DEPENDS other_catkin_pkg
  #  DEPENDS system_lib
  )

# Find xml_reflection
ADD_REQUIRED_DEPENDENCY("urdfdom >= 0.2.9")
ADD_REQUIRED_DEPENDENCY("gazebo >= 7.0.0")
ADD_REQUIRED_DEPENDENCY(roscpp)

ADD_LIBRARY(SpringPlugin
  SHARED
  src/SpringPlugin.cc
  )

INSTALL(TARGETS
  SpringPlugin
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  )
PKG_CONFIG_USE_DEPENDENCY(SpringPlugin roscpp)
PKG_CONFIG_USE_DEPENDENCY(SpringPlugin gazebo)

FOREACH(dir config gazebo meshes robots urdf srdf launch)
  INSTALL(DIRECTORY ${dir}/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
ENDFOREACH(dir)
