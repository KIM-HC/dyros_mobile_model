cmake_minimum_required(VERSION 3.4)
project(dyros_mobile_model)

find_package(catkin REQUIRED)
catkin_package(CATKIN_DEPENDS xacro)

install(DIRECTORY model
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
