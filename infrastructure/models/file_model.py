from tortoise import fields, models



class FileModel(models.Model):

    class Meta:
        table = "files"

    id = fields.IntField(primary_key=True)
    filename = fields.CharField(max_length=255, unique=True)
    content = fields.BinaryField(null=True)