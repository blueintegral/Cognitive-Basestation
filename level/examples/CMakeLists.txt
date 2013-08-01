include(GrPython)

GR_PYTHON_INSTALL(
    PROGRAMS
    hn_demo.py
    fsk_demod_dev.py
    msk_demod_dev.py
	test_receive.py
	test_transmit.py
    DESTINATION ${GR_PKG_LEVEL_EXAMPLES_DIR}
    COMPONENT "level_examples"
)