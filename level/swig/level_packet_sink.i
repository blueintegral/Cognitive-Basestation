/* -*- c++ -*- */

GR_SWIG_BLOCK_MAGIC(level, packet_sink);

level_packet_sink_sptr 
level_make_packet_sink (const std::vector<unsigned char>& preamble, gr_msg_queue_sptr target_queue);

class level_packet_sink : public gr_sync_block
{
private:
  level_packet_sink ();
};