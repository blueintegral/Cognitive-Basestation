########################################################################
# Setup dependencies
########################################################################
include(GrBoost)

########################################################################
# Register component
########################################################################
include(GrComponent)

GR_REGISTER_COMPONENT("level" ENABLE_GR_LEVEL
    Boost_FOUND
    ENABLE_GR_CORE
)

GR_SET_GLOBAL(GR_LEVEL_INCLUDE_DIRS
    ${CMAKE_CURRENT_SOURCE_DIR}/lib
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

SET(GR_PKG_LEVEL_EXAMPLES_DIR ${GR_PKG_DATA_DIR}/examples/level)

########################################################################
# Begin conditional configuration
########################################################################
if(ENABLE_GR_LEVEL)

########################################################################
# Setup CPack components
########################################################################
include(GrPackage)
CPACK_SET(CPACK_COMPONENT_GROUP_DIGITAL_DESCRIPTION "GNU Radio Level Blocks")

CPACK_COMPONENT("level_runtime"
    GROUP        "Level"
    DISPLAY_NAME "Runtime"
    DESCRIPTION  "Dynamic link libraries"
    DEPENDS      "core_runtime"
)

CPACK_COMPONENT("level_devel"
    GROUP        "Level"
    DISPLAY_NAME "Development"
    DESCRIPTION  "C++ headers, package config, import libraries"
    DEPENDS      "core_devel"
)

CPACK_COMPONENT("level_python"
    GROUP        "Level"
    DISPLAY_NAME "Python"
    DESCRIPTION  "Python modules for runtime"
    DEPENDS      "core_python;level_runtime"
)

CPACK_COMPONENT("level_examples"
    GROUP        "Level"
    DISPLAY_NAME "Examples"
    DESCRIPTION  "Example programs"
    DEPENDS      "level_runtime"
)

CPACK_COMPONENT("level_swig"
    GROUP        "Level"
    DISPLAY_NAME "SWIG"
    DESCRIPTION  "SWIG development .i files"
    DEPENDS      "core_swig;level_python;level_devel"
)

########################################################################
# Add subdirectories
########################################################################
add_subdirectory(include)
add_subdirectory(lib)
add_subdirectory(doc)
if(ENABLE_PYTHON)
    add_subdirectory(swig)
    add_subdirectory(python)
    add_subdirectory(grc)
    add_subdirectory(examples)
endif(ENABLE_PYTHON)

########################################################################
# Create Pkg Config File
########################################################################
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/gnuradio-level.pc.in
    ${CMAKE_CURRENT_BINARY_DIR}/gnuradio-level.pc
@ONLY)

install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/gnuradio-level.pc
    DESTINATION ${GR_LIBRARY_DIR}/pkgconfig
    COMPONENT "level_devel"
)

endif(ENABLE_GR_LEVEL)