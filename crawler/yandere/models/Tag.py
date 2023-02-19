from pykson import JsonObject, IntegerField, StringField, BooleanField


class Tag(JsonObject):
    id = IntegerField()
    name = StringField()
    count = IntegerField()
    type = IntegerField()
    ambiguous = BooleanField()
    created_at = StringField()
    updated_at = StringField()
    note = StringField()

    def info(self):
        return f"Tag: id={self.id} name={self.name} count={self.count} type={self.type} ambiguous={self.ambiguous} created_at={self.created_at} updated_at={self.updated_at} note={self.note}"

    def to_list_1(self):
        return [str(self.id), self.name, str(self.count), str(self.type)]
