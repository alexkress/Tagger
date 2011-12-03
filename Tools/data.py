class Data:

    @classmethod
    def reserve_worker(cls):
        """Returns worker class for a worker ready to receive a message, until reply is received the
        worker should be removed from the pool"""
        return (1,"4163453434")

    @classmethod
    def mark_message_as_sent(cls, worker_phone_number, message_id):
        """Tells the system that a particular message has been sent to a worker"""
        pass

    @classmethod
    def release_worker(cls, worker_phone_number):
        """Release the worker back to the pool, should only be done once reply is received"""
        pass

    @classmethod
    def get_worker_by_phone(cls, worker_phone_number):
        """Returns a worker given phone number"""
        pass

    @classmethod
    def get_message(cls):
        """Returns a message to be sent out"""
        pass


    @classmethod
    def submit_tagged_text(cls, text_hash, worker_phone_number):
        """Receives a map containing words and corresponding tags"""
        pass

