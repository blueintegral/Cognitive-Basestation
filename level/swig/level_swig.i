/* -*- c++ -*- */

#define LEVEL_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
//%include "level_doc.i"

%{
#include "level_packet_sink.h"
%}

%include "level_packet_sink.i"
