########################################################################
# Setup swig generation
########################################################################
include(GrPython)
include(GrSwig)

set(GR_SWIG_INCLUDE_DIRS
    ${GR_LEVEL_INCLUDE_DIRS}
    ${GNURADIO_CORE_SWIG_INCLUDE_DIRS}
)

set(GR_SWIG_DOC_FILE ${CMAKE_CURRENT_BINARY_DIR}/level_swig_doc.i)
set(GR_SWIG_DOC_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/../include)

set(GR_SWIG_LIBRARIES gnuradio-level)

GR_SWIG_MAKE(level_swig level_swig.i)

GR_SWIG_INSTALL(
    TARGETS level_swig
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/level
    COMPONENT "level_python"
)

install(
    FILES
    level_swig.i
    level_packet_sink.i
    ${CMAKE_CURRENT_BINARY_DIR}/level_swig_doc.i
    DESTINATION ${GR_INCLUDE_DIR}/gnuradio/swig
    COMPONENT "level_swig"
)
