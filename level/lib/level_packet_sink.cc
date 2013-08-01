#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <level_packet_sink.h>
#include <gr_io_signature.h>
#include <cstdio>
#include <stdint.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdexcept>
#include <cstring>
#include <gr_count_bits.h>

#define VERBOSE 1

// just for debug printing
char tmp[FMT_BUF_SIZE];

inline void
level_packet_sink::enter_search()
{
  //if (VERBOSE)
  //  fprintf(stderr, "@ enter_search\n");

  d_state = STATE_PREAMBLE_SEARCH;
  d_preamble_reg = 0;
}
    
inline void
level_packet_sink::enter_sync_search()
{
  if (VERBOSE)
    fprintf(stderr, "@ enter_sync_search\n");

  d_state = STATE_SYNC_SEARCH;
  d_sync_reg = 0;
  d_sync_len_index = 0;
}

inline void
level_packet_sink::enter_midamble()
{
  if (VERBOSE)
    fprintf(stderr, "@ decode payload length\n");

  d_state = STATE_LENGTH_BYTE;
  d_mid_reg = 0;
  d_midamble_count = 0;
}

inline void
level_packet_sink::enter_decode_packet()
{
  if (VERBOSE)
    fprintf(stderr, "@ enter_decode_packet\n");

  d_state = STATE_DECODE_PACKET;
  d_payload_cnt = 0;
  d_packet_byte = 0;
  d_packetlen_cnt = 0;
}

level_packet_sink_sptr
level_make_packet_sink (const std::vector<uint8_t>& preamble,
                        gr_msg_queue_sptr target_queue)
{
  return level_packet_sink_sptr (new level_packet_sink (preamble, target_queue));
}

level_packet_sink::level_packet_sink (const std::vector<uint8_t>& preamble,
					gr_msg_queue_sptr target_queue)
  	: gr_sync_block ("level_packet_sink",
		   gr_make_io_signature (1, 1, sizeof(float)),
		   gr_make_io_signature (0, 0, 0)),
    d_target_queue(target_queue)
{
  // store preamble vector in uint32_t
  d_preamble = 0;
  for(int i = 0; i < 4; i++){
    d_preamble <<= 8;
    d_preamble |= preamble[i];
  }

  if ( VERBOSE )
    fprintf(stderr, "preamble: %s\n", binary_fmt(d_preamble, tmp)), fflush(stderr);

  d_sync = 0xD391; // TODO: pass as argument
  enter_search();
}

level_packet_sink::~level_packet_sink () {}

int
level_packet_sink::work (int noutput_items,
          gr_vector_const_void_star &input_items,
          gr_vector_void_star &output_items)
{
  float *inbuf = (float *) input_items[0];
  int count = 0;
  d_threshold = 1;
  
  //if (VERBOSE)
  //  fprintf(stderr, ">>> Entering state machine\n"), fflush(stderr);

  while (count < noutput_items) {
    switch(d_state) {
      
      case STATE_PREAMBLE_SEARCH:    // Look for preamble

        while (count < noutput_items) {
          if(slice(inbuf[count++]))
            d_preamble_reg = (d_preamble_reg << 1) | 1;  // Shift bits one at a time into preamble
          else
            d_preamble_reg = d_preamble_reg << 1;

          if(gr_count_bits64(d_preamble_reg ^ d_preamble) <= d_threshold) {
            //if (VERBOSE)
            //  fprintf(stderr,"FOUND PREAMBLE, incorrect bits: %d\n", err), fflush(stderr);
            enter_sync_search();
            break;
          }
        }
        break;

      case STATE_SYNC_SEARCH:
        if (VERBOSE)
          fprintf(stderr,"SYNC Search,    sync=%s\n", binary_fmt(d_sync, tmp)), fflush(stderr);

        while (count < noutput_items) {
          if(slice(inbuf[count++]))
            d_sync_reg = (d_sync_reg << 1) | 1;  // Shift bits one at a time into sync
          else
            d_sync_reg = d_sync_reg << 1;
          d_sync_len_index++;

          //if (VERBOSE)
          //  fprintf(stderr,"SYNC so far: %s\n", binary_fmt(d_sync_reg, tmp)), fflush(stderr);

          // Compute incorrect bits of alleged sync vector
          if(gr_count_bits64(d_sync_reg ^ d_sync) <= d_threshold) {
            // Found it, set up for packet decode
            if (VERBOSE)
              fprintf(stderr,"FOUND SYNC, detected=%s\n", binary_fmt(d_sync_reg, tmp)), fflush(stderr);
            enter_midamble();
            break;
          }else if(d_sync_len_index > 16){
            // wrong sync word after preamble
            if (VERBOSE)
              fprintf(stderr,"WRONG SYNC, detected=%s incorrect=%d\n", binary_fmt(d_sync_reg, tmp), gr_count_bits64(d_sync_reg ^ d_sync)), fflush(stderr);
            enter_search();
            break;
          }
        }
        break;

      // store length byte
      case STATE_LENGTH_BYTE:
        while (count < noutput_items) {
          if(slice(inbuf[count++]))
            d_mid_reg = (d_mid_reg << 1) | 1;
          else
            d_mid_reg = d_mid_reg << 1;
          
          if(d_midamble_count++ >= 7){
            if(VERBOSE)
              fprintf(stderr,"Decoded Payload Size: %s\n", binary_fmt(d_mid_reg, tmp)), fflush(stderr);
            d_packet_length = d_mid_reg;
            enter_decode_packet();
            break;
          }
        }
        break;

      case STATE_DECODE_PACKET:

        while (count < noutput_items) {   // shift bits into bytes of packet one at a time
          if(slice(inbuf[count++]))
            d_packet_byte = (d_packet_byte << 1) | 1;
          else
            d_packet_byte = d_packet_byte << 1;

          if (d_packet_byte_index++ >= 7) {     // byte is full so move to next byte
            d_packet[d_packetlen_cnt++] = d_packet_byte;
            d_packet_byte = 0;
            d_payload_cnt++;
            d_packet_byte_index = 0;

            if (d_payload_cnt >= d_packet_length){  // packet is filled
              // build a message
              gr_message_sptr msg = gr_make_message(0, 0, 0, d_packetlen_cnt);        
              memcpy(msg->msg(), d_packet, d_packetlen_cnt);

              d_target_queue->insert_tail(msg);   // send it
              msg.reset();                        // free it up
              enter_search();
              break;
            }
          }
        }
        break;
    }
  }

  return noutput_items;
}
