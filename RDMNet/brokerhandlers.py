from RDMNet import vectors

def handle(self, data):
    #Check broker vector
    if data[42:44] == vectors.vector_broker_connect:
        #Ignore - we won't receive this
        pass
    elif data[42:44] == vectors.vector_broker_connect_reply:
        broker_connect_reply(self, data)
    elif data[42:44] == vectors.vector_broker_client_entry_update:
        #Ignore - we shouldn't see this
        pass
    elif data[42:44] == vectors.vector_broker_redirect_v4:
        #TODO: Implement broker redirect v4
        pass
    elif data[42:44] == vectors.vector_broker_redirect_v6:
        #TODO: Implement broker redirect v6
        pass
    elif data[42:44] == vectors.vector_broker_fetch_client_list:
        #Ignore
        pass
    elif data[42:44] == vectors.vector_broker_connected_client_list:
        #Ignore
        pass
    elif data[42:44] == vectors.vector_broker_client_add:
        #Ignore
        pass
    elif data[42:44] == vectors.vector_broker_client_remove:
        #Ignore
        pass
    elif data[42:44] == vectors.vector_broker_client_entry_change:
        #Ignore
        pass
    elif data[42:44] == vectors.vector_broker_request_dynamic_uids:
        #Ignore
        pass
    elif data[42:44] == vectors.vector_broker_assigned_dynamic_uids:
        #Ignore
        pass
    elif data[42:44] == vectors.vector_broker_fetch_dynamic_uid_list:
        #Ignore
        pass
    elif data[42:44] == vectors.vector_broker_disconnect:
        #TODO: Implement Broker Disconnect
        pass
    elif data[42:44] == vectors.vector_broker_null:
        broker_null(self, data)
    else:
        print("Unrecognised Broker Vector")

def broker_connect_reply(self, data):
    print("Broker Connected")
    #IDEA: Does this need a handler?

def broker_null(self, data):
    print("Heartbeat")
    #TODO: Reset heartbeat timer or something like that
