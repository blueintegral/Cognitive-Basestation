########################################################################
# Setup the include and linker paths
########################################################################
include_directories(
    ${GNURADIO_CORE_INCLUDE_DIRS}
    ${GR_LEVEL_INCLUDE_DIRS}
)

include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})


########################################################################
# Setup library
########################################################################
list(APPEND level_sources
    cc430_crc.c
    level_packet_sink.cc
)

list(APPEND level_libs
    gnuradio-core
    ${Boost_LIBRARIES}
)

add_library(gnuradio-level SHARED ${level_sources})
target_link_libraries(gnuradio-level ${level_libs})
GR_LIBRARY_FOO(gnuradio-level RUNTIME_COMPONENT "level_runtime" DEVEL_COMPONENT "level_devel")
