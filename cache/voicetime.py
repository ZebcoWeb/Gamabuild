import rom

from datetime import datetime

class VoiceTime(rom.Model):
    member_id = rom.Integer(required=True, unique=True, index=True)
    join_time = rom.DateTime()

    def save(self, *args, **kwargs):
        if not self.join_time:
            self.join_time = datetime.now()
        return super(VoiceTime, self).save(*args, **kwargs)