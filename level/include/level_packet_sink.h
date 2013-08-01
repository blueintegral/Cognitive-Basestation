#ifndef INCLUDED_LEVEL_PACKET_SINK
#define INCLUDED_LEVEL_PACKET_SINK

#include <stdint.h>
#include <gr_sync_block.h>
#include <gr_msg_queue.h>

#define FMT_BUF_SIZE (CHAR_BIT*sizeof(uintmax_t)+1)

class level_packet_sink;

typedef boost::shared_ptr<level_packet_sink> level_packet_sink_sptr;

level_packet_sink_sptr level_make_packet_sink (const std::vector<uint8_t>& preamble,
			   gr_msg_queue_sptr target_queue);

class level_packet_sink : public gr_sync_block
{
private:
 	friend level_packet_sink_sptr level_make_packet_sink (const std::vector<uint8_t>& preamble,
			   gr_msg_queue_sptr target_queue);	
 	
 	level_packet_sink();   // private constructor	
 	
 	enum state_t {STATE_PREAMBLE_SEARCH, STATE_SYNC_SEARCH, STATE_LENGTH_BYTE, STATE_DECODE_PACKET};	
 	
 	static const int MSG_LEN_POS = 8+1;        			  	// 8 byte sos header, 1 byte AM type
 	static const int MAX_PKT_LEN = 128 - MSG_LEN_POS - 1;	// remove header and CRC	
 	
 	gr_msg_queue_sptr    d_target_queue;					// where to send the packet when received
 	uint32_t		     d_preamble;						// 32 bit preamble to locate start of packet
 	uint32_t		     d_threshold;						// how many bits may be wrong in preamble
 	uint16_t		     d_sync;							// sync word
				  	  
 	state_t              d_state;				  	
				  	  
 	uint32_t		     d_preamble_reg;					// used to look for preamble
 	uint16_t		     d_sync_reg;						// used to look for sync word
 	uint8_t				 d_sync_len_index;					// track length of sync word
 	uint32_t			 d_mid_reg;							// store midamble
 	uint8_t				 d_midamble_count;					// track length of midamble
  
 	uint8_t				 d_packet[MAX_PKT_LEN];				// assembled payload
 	uint8_t			     d_packet_byte;						// byte being assembled
 	uint32_t     	     d_packet_byte_index;				// which bit of d_packet_byte we're working on
 	uint32_t	         d_packet_length;					// length of packet
 	uint32_t     	     d_packetlen_cnt;					// how many so far
 	uint32_t     	     d_payload_cnt;						// how many bytes in payload
  
protected:
 	level_packet_sink(const std::vector<uint8_t>& preamble, 
		       gr_msg_queue_sptr target_queue);
 	
 	void enter_search();
 	void enter_sync_search();
 	void enter_midamble();
 	void enter_decode_packet();

 	int slice(float x) { return x > 0 ? 1 : 0; }

 	// just for debug printing
 	char *binary_fmt(uintmax_t x, char buf[FMT_BUF_SIZE])
 	{
	    char *s = buf + FMT_BUF_SIZE;
	    *--s = 0;
	    if (!x) *--s = '0';
	    for(; x; x/=2) *--s = '0' + x%2;
	    return s;
	}

 public:
 	~level_packet_sink ();  // public destructor	
 	
 	// Where all the action really happens	
 	int work(int noutput_items,
	   gr_vector_const_void_star &input_items,
	   gr_vector_void_star &output_items);
 	
 	// return true if we detect carrier
 	bool carrier_sensed() const
 	{
 	  return d_state != STATE_PREAMBLE_SEARCH;
 	}
};

#endif /* INCLUDED_LEVEL_PACKET_SINK */