class_name JsonSerializer

func to_dict(obj):
	var property_dictionary = {}
	var properties = obj.get_property_list()
	for property in properties:
		if property.name != "Reference" and property.name != "script" and property.name != "Script Variables":
			print(property.name)
			property_dictionary[property.name] = obj[property.name]
			
	return property_dictionary

func serialize_dict(dictionary):
	return JSON.print(dictionary)

func serialize(obj):
	var obj_dict = to_dict(obj)
	
	return JSON.print(obj_dict)

func deserialize(text):
	return JSON.parse(text).result
