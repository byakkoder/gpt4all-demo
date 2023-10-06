extends Control

var max_scroll = 0

onready var scrollbar = $CanvasLayer/ScrollContainer.get_v_scrollbar()


func _ready():
	scrollbar.connect("changed", self, "scroll_to_bottom")
	max_scroll = scrollbar.max_value


func scroll_to_bottom(): 
	if max_scroll != scrollbar.max_value:
		max_scroll = scrollbar.max_value
		$CanvasLayer/ScrollContainer.scroll_vertical = scrollbar.max_value


func build_service_info(command):
	var service_info = ChatServiceInfo.new()
	
	service_info.source = 'client'
	service_info.target = 'brain'
	service_info.content = command
	
	return service_info


func _on_WebSocketClient_on_data_received(data):
	var receivedObj = JsonSerializer.new().deserialize(data)
	
	if receivedObj.target != 'client':
		return
	
	$CanvasLayer/ScrollContainer/InteractionDisplay.text = $CanvasLayer/ScrollContainer/InteractionDisplay.text + receivedObj.content


func _on_SendButton_pressed():
	var service_info = build_service_info($CanvasLayer/UserMessageText.text)
	var data = JsonSerializer.new().serialize(service_info)	

	$WebSocketClient.send_data(data)
	$CanvasLayer/ScrollContainer/InteractionDisplay.text = '[User]: ' + $CanvasLayer/UserMessageText.text + '\r\n[A.I.]: '
	$CanvasLayer/UserMessageText.text = ''
	$CanvasLayer/ScrollContainer.set_v_scroll($CanvasLayer/ScrollContainer.get_v_scrollbar().max_value)
