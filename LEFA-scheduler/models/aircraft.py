class Aircraft:

	def __init__(self, name, model, block_type, schedule_blocks):
		self.name = name
		self.model = model
		self.block_type = block_type # odd or even
		self.schedule_blocks = schedule_blocks
