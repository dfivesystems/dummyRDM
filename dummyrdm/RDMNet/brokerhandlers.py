"""RDMNet Broker Handlers.

A selection of handlers for E1.33 RDMNet broker protocol. Currently
the only handlers implemented are broker_null and connect_reply, as
these are the minimum required for a device.

Todo:
    * Implement Broker redirect vectors
    * Implement Dynamic UIDs maybe?

"""

from RDMNet import vectors

def handle(self, data):
    """Main handler for E1.33 RDMnet Broker PDUs.
    Switches the handler based on the broker vector
    as defined in RDMNet.vectors.

    """

    #Check broker vector
    if data[26:28] == vectors.vector_broker_connect:
        #Ignore - we won't receive this
        pass
    elif data[26:28] == vectors.vector_broker_connect_reply:
        broker_connect_reply(self, data)
    elif data[26:28] == vectors.vector_broker_client_entry_update:
        #Ignore - we shouldn't see this
        pass
    elif data[26:28] == vectors.vector_broker_redirect_v4:
        #TODO: Implement broker redirect v4
        pass
    elif data[26:28] == vectors.vector_broker_redirect_v6:
        #TODO: Implement broker redirect v6
        pass
    elif data[26:28] == vectors.vector_broker_fetch_client_list:
        #Ignore
        pass
    elif data[26:28] == vectors.vector_broker_connected_client_list:
        #Ignore
        pass
    elif data[26:28] == vectors.vector_broker_client_add:
        #Ignore
        pass
    elif data[26:28] == vectors.vector_broker_client_remove:
        #Ignore
        pass
    elif data[26:28] == vectors.vector_broker_client_entry_change:
        #Ignore
        pass
    elif data[26:28] == vectors.vector_broker_request_dynamic_uids:
        #Ignore
        pass
    elif data[26:28] == vectors.vector_broker_assigned_dynamic_uids:
        #Ignore
        pass
    elif data[26:28] == vectors.vector_broker_fetch_dynamic_uid_list:
        #Ignore
        pass
    elif data[26:28] == vectors.vector_broker_disconnect:
        #TODO: Implement Broker Disconnect
        pass
    elif data[26:28] == vectors.vector_broker_null:
        broker_null(self, data)
    else:
        print("Unrecognised Broker Vector")

def broker_connect_reply(self, data):
    """Handles the broker_connect_reply vector.

    Todo:
        * Report the broker details

    """

    print("Broker Connected")
    #IDEA: Does this need a handler?

def broker_null(self, data):
    """Handles the broker_null (heartbeat) vector.

    Todo:
        * Reset the heatbeat timer for the connection.

    """

    print("Heartbeat")
    #TODO: Reset heartbeat timer or something like that
