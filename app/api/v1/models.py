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
    },
    {
        "id": 4,
        "createdOn": "28-11-2018 09:57",
        "createdBy": 4,
        "type": "Red Flag Report",
        "location": "4,4",
        "status": "Draft",
        "comment": "Not too urgent!"
    }
]
total_red_flags_ever = 4

class RedFlagsModel():
    def __init__(self):
        self.db = red_flags

    def get_all(self):
        return self.db

    def get_specific(self, red_flag_id):
        correct_red_flag = next(filter(lambda x: x["id"] == int(red_flag_id), self.db), None)
        return correct_red_flag

    def save(self, new_red_flag):
        self.db.append(new_red_flag)

    def edit(self, red_flag, new_data):
        red_flag.update(new_data)

    def delete(self, red_flag_id):
        self.db = list(filter(lambda x: x["id"] != int(red_flag_id), self.db))
