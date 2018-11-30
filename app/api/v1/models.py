red_flags = [
    {
        "id": 1,
        "createdOn": "25-11-2018 09:57",
        "createdBy": 1,
        "type": "Red Flag Report",
        "location": "1,1",
        "status": "Resolved",
        "comment": "Act quickly"
    },
    {
        "id": 2,
        "createdOn": "26-11-2018 09:57",
        "createdBy": 2,
        "type": "Red Flag Report",
        "location": "2,2",
        "status": "Under investigation",
        "comment": "Don't let them get away with it"
    },
    {
        "id": 3,
        "createdOn": "27-11-2018 09:57",
        "createdBy": 3,
        "type": "Red Flag Report",
        "location": "3,3",
        "status": "Rejected",
        "comment": "Hurry!"
    }
]
total_red_flags_ever = 3

class RedFlagsModel():
    def __init__(self):
        self.db = red_flags

    def get(self):
        return self.db

    def save(self, new_red_flag):
        self.db.append(new_red_flag)

    def remove(self, red_flag_id):
        self.db = list(filter(lambda x: x["id"] != int(red_flag_id), self.db))
