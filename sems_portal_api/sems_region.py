
region = "au"

def set_region(new_region: str):
	global region
	region = new_region

def get_region() -> str:
	global region
	return region

