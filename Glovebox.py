from glovebox.app.Application import Application

behone = None
behtwo = None

if __name__ == '__main__':
	app = Application()
	# app.options['shake_menu_item_size'] = 32
	# app.options['shake_menu_homing_time'] = 1
	
	# @app.event
	# def on_new_object(object):
	# 	global behone, behtwo
	# 	if not behone:
	# 		behone = app.behavior_loader.behaviors["alpha_object"].class_obj()
	# 		object.attach_behavior(behone)
	# 	elif not behtwo:
	# 		behtwo = app.behavior_loader.behaviors["maracas"].class_obj()
	# 		object.attach_behavior(behtwo)
	# 		# behone.redirect_audio_to_behavior(behtwo)
	# 	else:
	# 		behthree = app.behavior_loader.behaviors["simple_delay"].class_obj()
	# 		object.attach_behavior(behthree)
	# 		# behtwo.object.attach_behavior(Behavior())
	# 
	app.run()