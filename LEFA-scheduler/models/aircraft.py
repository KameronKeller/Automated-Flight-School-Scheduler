class Aircraft:
	def __init__(self, name, model, block_type, schedule_blocks, soloable=True):
		"""
		:param name: The name of the aircraft, string
		:param model: The model of the aircraft, string
		:param block_type: The block type of the aircraft, string
		:param schedule_blocks: The blocks that the aircraft can fly in, list of ints
		:param soloable: Whether the aircraft can be soloed, boolean
		"""
		self.name = name
		self.model = model
		self.block_type = block_type # odd or even
		self.schedule_blocks = schedule_blocks
		self.soloable = soloable
