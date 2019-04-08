import mongoengine as me

class User(me.Document):
	mail = me.StringField(required=True)
	password = me.StringField(required=True)

class Item(me.Document):
	user = me.ReferenceField(User, required=True)
	text = me.StringField(required=True)