from gnuradio import gr, fft, gru
import math, json, sys
import zmq, numpy

class zmq_fft_sink_c(gr.hier_block2):
	"""
	An fft block with real/complex inputs and a zmq publisher
	"""

	def __init__(
		self,
		baseband_freq =0,
		ref_scale = 2.0, 
		y_per_div = 10,
		y_divs = 8,
		ref_level = 50,
		sample_rate = 1,
		fft_size = 512,
		fft_rate = 20,
		average = False,
		avg_alpha = None,
		title = '',
		size = (600, 300),
		peak_hold = False,
		win = None,
		use_persistence = False,
		persist_alpha = None,
		**kwargs
	):
		#ensure avg alpha
		if avg_alpha is None: 
			avg_alpha = 2.0 / fft_rate
		
		#ensure analog alpha
		if persist_alpha is None:
			actual_fft_rate = float(sample_rate / fft_size) / float(max(1, int(float((sample_rate / fft_size) / fft_rate))))
			#print "requested_fft_rate ",fft_rate
			#print "actual_fft_rate    ",actual_fft_rate
			analog_cutoff_freq = 0.5 # Hertz
			#calculate alpha from wanted cutoff freq
			persist_alpha = 1.0 - math.exp(-2.0*math.pi*analog_cutoff_freq/actual_fft_rate)

		#init
		gr.hier_block2.__init__(
			self,
			"zmq_fft_sink",
			gr.io_signature(1, 1, gr.sizeof_gr_complex),
			gr.io_signature(0, 0, 0),
		)

		#blocks
		fft_0 = fft.logpwrfft_c(
			sample_rate = sample_rate,
			fft_size = fft_size,
			frame_rate = fft_rate,
			ref_scale = ref_scale,
			avg_alpha = avg_alpha,
			average = average,
			win = win,
		)

		msgq = gr.msg_queue(2)
		sink = gr.message_sink(gr.sizeof_float*fft_size, msgq, True)

		#controller
		#self.controller = pubsub()
		#self.controller.subscribe(AVERAGE_KEY, fft_0.set_average)
		#self.controller.publish(AVERAGE_KEY, fft_0.average)
		#self.controller.subscribe(AVG_ALPHA_KEY, fft_0.set_avg_alpha)
		#self.controller.publish(AVG_ALPHA_KEY, fft_0.avg_alpha)
		#self.controller.subscribe(SAMPLE_RATE_KEY, fft_0.set_sample_rate)
		#self.controller.publish(SAMPLE_RATE_KEY, fft_0.sample_rate)
		#start input watcher
		input_watcher(msgq)

		#connect
		self.connect(self, fft_0, sink)

class input_watcher(gru.msgq_runner):
	"""
	Input watcher thread runs forever.
	Read messages from the message queue.
	Forward messages to the message handler.
	"""
	def __init__ (self, msgq):
		self.count = 0
		self.context = zmq.Context()
		self.publisher = self.context.socket(zmq.PUB)
		self.publisher.bind("tcp://*:5555")
		gru.msgq_runner.__init__(self, msgq, self.handle_msg)

	def handle_msg(self, msg):
		self.count += 1
		#convert to floating point numbers
		print "test0"
		try:
			samples = numpy.fromstring(msg, numpy.float32)[:512] #only take first frame
		except:
			print sys.exc_info()
		arr = map(ord, msg.to_string())
		js = json.dumps({ 'fft': arr })
		self.publisher.send(js)
		#print "sent message", self.count


# ----------------------------------------------------------------
# Standalone test app
# ----------------------------------------------------------------

class test_app_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "FFT Sink Test")

        fft_size = 256

        # build our flow graph
        input_rate = 2048.0e3

        #Generate some noise
        noise = gr.noise_source_c(gr.GR_UNIFORM, 1.0/10)

        # Generate a complex sinusoid
        src1 = gr.sig_source_c (input_rate, gr.GR_SIN_WAVE, 2e3, 1)
        #src1 = gr.sig_source_c(input_rate, gr.GR_CONST_WAVE, 57.50e3, 1)

        # We add these throttle blocks so that this demo doesn't
        # suck down all the CPU available.  Normally you wouldn't use these.
        thr1 = gr.throttle(gr.sizeof_gr_complex, input_rate)

        test_fft = zmq_fft_sink_c(title="Complex Data", fft_size=fft_size,
                            sample_rate=input_rate, baseband_freq=100e3,
                            ref_level=0, y_per_div=20, y_divs=10)

        combine1 = gr.add_cc()
        #self.connect(src1, (combine1, 0))
        #self.connect(noise,(combine1, 1))
        self.connect(src1, thr1, test_fft)

def main ():
    app = test_app_block()
    app.run()

if __name__ == '__main__':
    main ()
